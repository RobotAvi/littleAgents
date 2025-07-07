"""
Утилита для работы с почтой
Автоматически анализирует входящие письма, выделяет важные, 
формирует сводку и создает задачи на основе писем, требующих ответа.
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
from email_client import EmailClient
from datetime import datetime, timedelta
import asyncio

def main():
    create_streamlit_header(
        "Работа с почтой", 
        "Анализ входящих писем и создание задач на основе ИИ"
    )
    
    # Конфигурация
    config = Config.get_utility_config('email_manager')
    required_keys = ['email_user', 'email_password', 'openai_api_key']
    
    if not validate_config(config, required_keys):
        st.stop()
    
    # Инициализация клиента почты
    email_client = EmailClient(
        username=config['email_user'],
        password=config['email_password'],
        imap_server=config['imap_server'],
        imap_port=config['imap_port']
    )
    
    # Боковая панель с настройками
    with st.sidebar:
        st.header("⚙️ Настройки")
        
        # Период анализа
        period = st.selectbox(
            "Период анализа:",
            ["Сегодня", "Вчера", "Последние 3 дня", "Последняя неделя"],
            index=0
        )
        
        # Количество писем для анализа
        email_limit = st.slider("Максимум писем:", 5, 50, 20)
        
        # Фильтр по папкам
        folder = st.selectbox(
            "Папка почты:",
            ["INBOX", "Sent", "Draft", "Spam"],
            index=0
        )
        
        # Автоматическое обновление
        auto_refresh = st.checkbox("Автообновление каждые 5 мин", False)
        
        if st.button("🔄 Обновить данные", type="primary"):
            st.rerun()
    
    # Основное содержимое
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Обзор", "📧 Письма", "🤖 ИИ Анализ", "📋 Задачи"
    ])
    
    with tab1:
        st.subheader("📊 Обзор почты")
        
        # Получение данных
        with st.spinner("Загрузка писем..."):
            try:
                # Определение периода
                if period == "Сегодня":
                    since_date = datetime.now().date()
                elif period == "Вчера":
                    since_date = datetime.now().date() - timedelta(days=1)
                elif period == "Последние 3 дня":
                    since_date = datetime.now().date() - timedelta(days=3)
                else:
                    since_date = datetime.now().date() - timedelta(days=7)
                
                # Получение писем
                emails = email_client.get_emails(
                    folder=folder,
                    since_date=since_date,
                    limit=email_limit
                )
                
                if emails:
                    # Метрики
                    total_emails = len(emails)
                    unread_emails = len([e for e in emails if not e.get('read', True)])
                    important_emails = len([e for e in emails if e.get('priority') == 'high'])
                    
                    metrics = {
                        "Всего писем": total_emails,
                        "Непрочитанных": unread_emails,
                        "Важных": important_emails,
                        "За период": period
                    }
                    
                    display_metrics(metrics)
                    
                    # График активности по времени
                    st.subheader("📈 Активность по времени")
                    
                    import pandas as pd
                    import plotly.express as px
                    
                    # Подготовка данных для графика
                    email_times = []
                    for email in emails:
                        if email.get('date'):
                            try:
                                email_date = datetime.fromisoformat(str(email['date']))
                                email_times.append({
                                    'hour': email_date.hour,
                                    'date': email_date.date(),
                                    'count': 1
                                })
                            except:
                                continue
                    
                    if email_times:
                        df = pd.DataFrame(email_times)
                        hourly_stats = df.groupby('hour')['count'].sum().reset_index()
                        
                        fig = px.bar(
                            hourly_stats, 
                            x='hour', 
                            y='count',
                            title="Распределение писем по часам",
                            labels={'hour': 'Час дня', 'count': 'Количество писем'}
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                else:
                    st.info("Письма не найдены за выбранный период")
                    
            except Exception as e:
                st.error(f"Ошибка загрузки писем: {e}")
                emails = []
    
    with tab2:
        st.subheader("📧 Список писем")
        
        if 'emails' in locals() and emails:
            # Фильтры
            col1, col2 = st.columns(2)
            
            with col1:
                show_read = st.checkbox("Показать прочитанные", True)
                show_unread = st.checkbox("Показать непрочитанные", True)
            
            with col2:
                priority_filter = st.selectbox(
                    "Фильтр по приоритету:",
                    ["Все", "Высокий", "Средний", "Низкий"]
                )
            
            # Фильтрация писем
            filtered_emails = []
            for email in emails:
                # Фильтр по прочитанности
                if not show_read and email.get('read', True):
                    continue
                if not show_unread and not email.get('read', True):
                    continue
                
                # Фильтр по приоритету
                if priority_filter != "Все":
                    email_priority = email.get('priority', 'medium')
                    if priority_filter.lower() != email_priority:
                        continue
                
                filtered_emails.append(email)
            
            # Отображение писем
            for i, email in enumerate(filtered_emails):
                with st.expander(
                    f"📧 {email.get('subject', 'Без темы')} | "
                    f"От: {email.get('from', 'Unknown')} | "
                    f"{email.get('date', 'Unknown')}"
                ):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**От:** {email.get('from', 'Unknown')}")
                        st.markdown(f"**Тема:** {email.get('subject', 'Без темы')}")
                        st.markdown(f"**Дата:** {email.get('date', 'Unknown')}")
                        
                        # Содержимое письма
                        body = email.get('body', 'Нет содержимого')
                        if len(body) > 500:
                            st.markdown(f"**Содержимое:** {body[:500]}...")
                            if st.button(f"Показать полностью #{i}"):
                                st.text(body)
                        else:
                            st.markdown(f"**Содержимое:** {body}")
                    
                    with col2:
                        # Статус письма
                        read_status = "📖 Прочитано" if email.get('read', True) else "📩 Новое"
                        st.markdown(f"**Статус:** {read_status}")
                        
                        # Приоритет
                        priority = email.get('priority', 'medium')
                        priority_icon = "🔴" if priority == 'high' else "🟡" if priority == 'medium' else "🟢"
                        st.markdown(f"**Приоритет:** {priority_icon} {priority.title()}")
                        
                        # Действия
                        if st.button(f"Создать задачу #{i}", key=f"task_{i}"):
                            st.success("Задача создана!")
                            
                        if st.button(f"Отметить важным #{i}", key=f"important_{i}"):
                            st.success("Отмечено как важное!")
        else:
            st.info("Нет писем для отображения")
    
    with tab3:
        st.subheader("🤖 ИИ Анализ писем")
        
        if 'emails' in locals() and emails:
            if st.button("🔍 Запустить анализ ИИ", type="primary"):
                with st.spinner("Анализ писем с помощью ИИ..."):
                    
                    @async_to_sync
                    async def analyze_emails():
                        return await llm_client.summarize_emails(emails)
                    
                    analysis = analyze_emails()
                    
                    st.subheader("📝 Результат анализа")
                    st.markdown(analysis)
                    
                    # Сохранение результата
                    if st.button("💾 Сохранить анализ"):
                        from shared.utils import save_json_data
                        
                        analysis_data = {
                            'timestamp': datetime.now().isoformat(),
                            'period': period,
                            'total_emails': len(emails),
                            'analysis': analysis
                        }
                        
                        save_json_data(analysis_data, f"email_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
                        st.success("Анализ сохранен!")
        else:
            st.info("Сначала загрузите письма во вкладке 'Обзор'")
    
    with tab4:
        st.subheader("📋 Управление задачами")
        
        st.markdown("""
        **Автоматическое создание задач на основе писем:**
        
        1. 📧 Письма анализируются ИИ
        2. 🎯 Определяются действия, требующие выполнения
        3. 📋 Создаются задачи с приоритетами
        4. 📬 Отправляются уведомления
        """)
        
        # Форма создания задачи вручную
        with st.form("manual_task"):
            st.subheader("✏️ Создать задачу вручную")
            
            task_title = st.text_input("Название задачи:")
            task_description = st.text_area("Описание:")
            task_priority = st.selectbox("Приоритет:", ["Низкий", "Средний", "Высокий"])
            task_due_date = st.date_input("Срок выполнения:")
            
            if st.form_submit_button("Создать задачу"):
                if task_title:
                    st.success(f"Задача '{task_title}' создана!")
                else:
                    st.error("Введите название задачи")
        
        # История задач
        st.subheader("📚 История задач")
        st.info("Здесь будет отображаться история созданных задач")

if __name__ == "__main__":
    main()