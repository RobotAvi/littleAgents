"""
Утилита для анализа мессенджеров
Обрабатывает сообщения в Telegram, выделяет важные, создает сводки и задачи.
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
import json

def main():
    create_streamlit_header(
        "Анализ мессенджеров", 
        "Обработка и анализ сообщений в Telegram с помощью ИИ"
    )
    
    # Конфигурация
    config = Config.get_utility_config('messenger_analyzer')
    required_keys = ['telegram_bot_token', 'openai_api_key']
    
    if not validate_config(config, required_keys):
        st.stop()
    
    # Боковая панель с настройками
    with st.sidebar:
        st.header("⚙️ Настройки")
        
        # Период анализа
        period = st.selectbox(
            "Период анализа:",
            ["Последний час", "Сегодня", "Вчера", "Последние 3 дня"],
            index=1
        )
        
        # Лимит сообщений
        message_limit = st.slider("Максимум сообщений:", 10, 100, 50)
        
        # Фильтр по чатам
        chat_filter = st.multiselect(
            "Фильтр по чатам:",
            ["Рабочие группы", "Личные сообщения", "Каналы", "Боты"],
            default=["Рабочие группы", "Личные сообщения"]
        )
        
        if st.button("🔄 Обновить данные", type="primary"):
            st.rerun()
    
    # Основное содержимое
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Обзор", "💬 Сообщения", "🤖 ИИ Анализ", "📋 Задачи"
    ])
    
    with tab1:
        st.subheader("📊 Статистика сообщений")
        
        # Симуляция данных (в реальности здесь был бы API Telegram)
        with st.spinner("Загрузка сообщений..."):
            # Здесь должна быть интеграция с Telegram API
            messages = [
                {
                    'id': 1, 'from': 'Коллега 1', 'text': 'Нужно обсудить проект',
                    'timestamp': datetime.now() - timedelta(hours=1),
                    'chat_type': 'personal', 'priority': 'high'
                },
                {
                    'id': 2, 'from': 'Рабочая группа', 'text': 'Встреча перенесена на завтра',
                    'timestamp': datetime.now() - timedelta(hours=2),
                    'chat_type': 'group', 'priority': 'medium'
                }
            ]
            
            if messages:
                # Метрики
                total_messages = len(messages)
                unread_messages = len([m for m in messages if m.get('unread', True)])
                high_priority = len([m for m in messages if m.get('priority') == 'high'])
                
                metrics = {
                    "Всего сообщений": total_messages,
                    "Непрочитанных": unread_messages,
                    "Высокий приоритет": high_priority,
                    "За период": period
                }
                
                display_metrics(metrics)
                
                # График активности
                st.subheader("📈 Активность по времени")
                import pandas as pd
                import plotly.express as px
                
                df = pd.DataFrame(messages)
                hourly_stats = df.groupby(df['timestamp'].dt.hour).size().reset_index()
                hourly_stats.columns = ['hour', 'count']
                
                fig = px.bar(
                    hourly_stats, 
                    x='hour', 
                    y='count',
                    title="Сообщения по часам"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Сообщения не найдены")
    
    with tab2:
        st.subheader("💬 Список сообщений")
        
        if 'messages' in locals() and messages:
            for i, msg in enumerate(messages):
                with st.expander(
                    f"💬 {msg['from']} | {msg['timestamp'].strftime('%H:%M')} | "
                    f"{'🔴' if msg.get('priority') == 'high' else '🟡'}"
                ):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**От:** {msg['from']}")
                        st.markdown(f"**Время:** {msg['timestamp']}")
                        st.markdown(f"**Сообщение:** {msg['text']}")
                    
                    with col2:
                        if st.button(f"Ответить #{i}", key=f"reply_{i}"):
                            st.success("Ответ отправлен!")
                        
                        if st.button(f"Важное #{i}", key=f"important_{i}"):
                            st.success("Отмечено как важное!")
        else:
            st.info("Нет сообщений для отображения")
    
    with tab3:
        st.subheader("🤖 ИИ Анализ сообщений")
        
        if st.button("🔍 Анализировать сообщения", type="primary"):
            with st.spinner("Анализ сообщений..."):
                
                @async_to_sync
                async def analyze_messages():
                    return await llm_client.analyze_telegram_messages(messages if 'messages' in locals() else [])
                
                analysis = analyze_messages()
                
                st.subheader("📝 Результат анализа")
                st.markdown(analysis)
    
    with tab4:
        st.subheader("📋 Автоматические задачи")
        
        st.markdown("""
        **Создание задач на основе сообщений:**
        
        1. 💬 Анализ важных сообщений
        2. 🎯 Выявление требующих действия
        3. 📋 Автоматическое создание задач
        4. 📬 Уведомления о новых задачах
        """)

if __name__ == "__main__":
    main()