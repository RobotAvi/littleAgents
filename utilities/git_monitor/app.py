"""
Утилита для контроля разработки
Мониторинг изменений в Git репозиториях, анализ коммитов и код-ревью.
"""

import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from shared.llm_client import llm_client
from shared.config import Config
from shared.utils import (
    create_streamlit_header, display_metrics, 
    display_data_table, send_notification, 
    validate_config, async_to_sync
)
from datetime import datetime, timedelta
import subprocess

def main():
    create_streamlit_header(
        "Контроль разработки", 
        "Мониторинг Git репозиториев и анализ изменений"
    )
    
    # Конфигурация
    config = Config.get_utility_config('git_monitor')
    
    # Боковая панель с настройками
    with st.sidebar:
        st.header("⚙️ Настройки")
        
        # Репозитории для мониторинга
        repo_paths = st.text_area(
            "Пути к репозиториям (по одному на строку):",
            value="/workspace\n/home/user/project1"
        ).strip().split('\n')
        
        # Период анализа
        period = st.selectbox(
            "Период анализа:",
            ["Сегодня", "Вчера", "Последние 3 дня", "Неделя"],
            index=0
        )
        
        # Авторы для фильтрации
        author_filter = st.text_input("Фильтр по автору (опционально):")
        
        if st.button("🔄 Обновить данные", type="primary"):
            st.rerun()
    
    # Основное содержимое
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Обзор", "📝 Коммиты", "🔍 Анализ кода", "📈 Статистика"
    ])
    
    with tab1:
        st.subheader("📊 Обзор разработки")
        
        with st.spinner("Анализ репозиториев..."):
            commits_data = []
            
            for repo_path in repo_paths:
                if repo_path.strip() and os.path.exists(repo_path.strip()):
                    try:
                        # Получение последних коммитов
                        os.chdir(repo_path.strip())
                        
                        # Определение периода для git log
                        if period == "Сегодня":
                            since = "1.day.ago"
                        elif period == "Вчера":
                            since = "2.days.ago"
                        elif period == "Последние 3 дня":
                            since = "3.days.ago"
                        else:
                            since = "1.week.ago"
                        
                        cmd = ["git", "log", f"--since={since}", "--oneline", "--pretty=format:%H|%an|%ad|%s", "--date=short"]
                        result = subprocess.run(cmd, capture_output=True, text=True)
                        
                        for line in result.stdout.strip().split('\n'):
                            if line:
                                parts = line.split('|', 3)
                                if len(parts) >= 4:
                                    commits_data.append({
                                        'repo': os.path.basename(repo_path.strip()),
                                        'hash': parts[0][:8],
                                        'author': parts[1],
                                        'date': parts[2],
                                        'message': parts[3]
                                    })
                    except Exception as e:
                        st.warning(f"Ошибка при анализе {repo_path}: {e}")
            
            if commits_data:
                # Метрики
                total_commits = len(commits_data)
                unique_authors = len(set(c['author'] for c in commits_data))
                unique_repos = len(set(c['repo'] for c in commits_data))
                
                metrics = {
                    "Всего коммитов": total_commits,
                    "Авторов": unique_authors,
                    "Репозиториев": unique_repos,
                    "За период": period
                }
                
                display_metrics(metrics)
                
                # График активности по авторам
                import pandas as pd
                import plotly.express as px
                
                df = pd.DataFrame(commits_data)
                author_stats = df['author'].value_counts().reset_index()
                author_stats.columns = ['author', 'commits']
                
                fig = px.bar(
                    author_stats, 
                    x='author', 
                    y='commits',
                    title="Активность по авторам"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Коммиты не найдены за выбранный период")
    
    with tab2:
        st.subheader("📝 Последние коммиты")
        
        if 'commits_data' in locals() and commits_data:
            # Фильтрация по автору
            if author_filter:
                filtered_commits = [c for c in commits_data if author_filter.lower() in c['author'].lower()]
            else:
                filtered_commits = commits_data
            
            for commit in filtered_commits[:20]:  # Показываем последние 20
                with st.expander(f"📝 {commit['hash']} | {commit['author']} | {commit['date']}"):
                    st.markdown(f"**Репозиторий:** {commit['repo']}")
                    st.markdown(f"**Автор:** {commit['author']}")
                    st.markdown(f"**Дата:** {commit['date']}")
                    st.markdown(f"**Сообщение:** {commit['message']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"Просмотр изменений", key=f"diff_{commit['hash']}"):
                            st.info("Здесь будет показан diff коммита")
                    
                    with col2:
                        if st.button(f"Анализ ИИ", key=f"ai_{commit['hash']}"):
                            st.info("ИИ анализ изменений в коммите")
        else:
            st.info("Нет коммитов для отображения")
    
    with tab3:
        st.subheader("🔍 Анализ кода с помощью ИИ")
        
        if st.button("🤖 Анализировать изменения", type="primary"):
            if 'commits_data' in locals() and commits_data:
                with st.spinner("Анализ изменений..."):
                    commits_text = "\n\n".join([
                        f"Репозиторий: {c['repo']}\n"
                        f"Автор: {c['author']}\n" 
                        f"Дата: {c['date']}\n"
                        f"Сообщение: {c['message']}"
                        for c in commits_data[:10]  # Анализируем последние 10
                    ])
                    
                    @async_to_sync
                    async def analyze_commits():
                        return await llm_client.analyze_text(
                            commits_text,
                            "Проанализируй изменения в коде на основе коммитов. "
                            "Выдели основные направления разработки, качество коммитов, "
                            "потенциальные проблемы и рекомендации."
                        )
                    
                    analysis = analyze_commits()
                    
                    st.subheader("📝 Результат анализа")
                    st.markdown(analysis)
            else:
                st.warning("Сначала загрузите данные о коммитах")
    
    with tab4:
        st.subheader("📈 Статистика разработки")
        
        if 'commits_data' in locals() and commits_data:
            import pandas as pd
            import plotly.express as px
            
            df = pd.DataFrame(commits_data)
            
            # График по дням
            daily_stats = df.groupby('date').size().reset_index()
            daily_stats.columns = ['date', 'commits']
            
            fig = px.line(
                daily_stats,
                x='date',
                y='commits', 
                title="Коммиты по дням"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Топ авторов
            st.subheader("🏆 Топ авторов")
            author_stats = df['author'].value_counts().head(10)
            st.bar_chart(author_stats)
            
            # Активность по репозиториям
            st.subheader("📁 Активность по репозиториям")
            repo_stats = df['repo'].value_counts()
            st.bar_chart(repo_stats)
        else:
            st.info("Загрузите данные для просмотра статистики")

if __name__ == "__main__":
    main()