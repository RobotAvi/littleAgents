"""
Утилита для подготовки к встречам
Анализирует предстоящие встречи и составляет списки необходимых артефактов.
"""

import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from shared.llm_client import llm_client
from shared.config import Config
from shared.utils import (
    create_streamlit_header, display_metrics, 
    validate_config, async_to_sync
)
from datetime import datetime, timedelta

def main():
    create_streamlit_header(
        "Подготовка к встречам", 
        "Анализ предстоящих встреч и составление списков артефактов"
    )
    
    # Боковая панель с настройками
    with st.sidebar:
        st.header("⚙️ Настройки")
        
        # Период подготовки
        prep_period = st.selectbox(
            "Период подготовки:",
            ["Сегодня", "Завтра", "Эта неделя", "Следующая неделя"],
            index=0
        )
        
        # Типы встреч
        meeting_types = st.multiselect(
            "Типы встреч:",
            ["Планерки", "1:1", "Демо", "Ретроспективы", "Интервью"],
            default=["Планерки", "1:1"]
        )
        
        if st.button("🔄 Обновить данные", type="primary"):
            st.rerun()
    
    # Основное содержимое
    tab1, tab2, tab3, tab4 = st.tabs([
        "📅 Встречи", "📋 Подготовка", "📄 Артефакты", "🤖 ИИ Помощь"
    ])
    
    with tab1:
        st.subheader("📅 Предстоящие встречи")
        
        # Симуляция данных встреч
        meetings = [
            {
                "title": "Weekly Planning",
                "time": datetime.now() + timedelta(hours=2),
                "duration": 60,
                "participants": ["Team Lead", "Developer 1", "Developer 2"],
                "type": "Планерки"
            },
            {
                "title": "1:1 с менеджером",
                "time": datetime.now() + timedelta(days=1),
                "duration": 30,
                "participants": ["Manager"],
                "type": "1:1"
            }
        ]
        
        for i, meeting in enumerate(meetings):
            with st.expander(f"📅 {meeting['title']} | {meeting['time'].strftime('%d.%m %H:%M')}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Время:** {meeting['time'].strftime('%d.%m.%Y %H:%M')}")
                    st.markdown(f"**Длительность:** {meeting['duration']} мин")
                    st.markdown(f"**Участники:** {', '.join(meeting['participants'])}")
                    st.markdown(f"**Тип:** {meeting['type']}")
                
                with col2:
                    if st.button(f"Подготовиться", key=f"prep_{i}"):
                        st.success("Создан план подготовки!")
    
    with tab2:
        st.subheader("📋 План подготовки")
        
        if st.button("🎯 Создать план подготовки", type="primary"):
            with st.spinner("Создание плана..."):
                st.subheader("📝 Рекомендуемые действия")
                
                checklist = [
                    "📊 Подготовить статистику по проекту",
                    "📋 Проверить список задач в трекере",
                    "📈 Собрать метрики производительности",
                    "💬 Проанализировать фидбек от команды",
                    "📄 Подготовить презентацию (если нужно)"
                ]
                
                for item in checklist:
                    checked = st.checkbox(item, key=f"check_{item}")
                
                if st.button("✅ Отметить подготовку завершенной"):
                    st.success("Подготовка к встречам завершена!")
    
    with tab3:
        st.subheader("📄 Управление артефактами")
        
        # Форма для добавления артефакта
        with st.form("add_artifact"):
            st.subheader("➕ Добавить артефакт")
            
            artifact_name = st.text_input("Название:")
            artifact_type = st.selectbox("Тип:", ["Презентация", "Документ", "Таблица", "Код"])
            artifact_priority = st.selectbox("Приоритет:", ["Высокий", "Средний", "Низкий"])
            
            if st.form_submit_button("Добавить артефакт"):
                if artifact_name:
                    st.success(f"Артефакт '{artifact_name}' добавлен!")
        
        # Список артефактов
        st.subheader("📚 Список артефактов")
        artifacts = [
            {"name": "Отчет по проекту", "type": "Презентация", "status": "Готов"},
            {"name": "Технические требования", "type": "Документ", "status": "В работе"}
        ]
        
        for artifact in artifacts:
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"**{artifact['name']}**")
            with col2:
                st.write(artifact['type'])
            with col3:
                if artifact['status'] == 'Готов':
                    st.success("✅ Готов")
                else:
                    st.warning("⏳ В работе")
    
    with tab4:
        st.subheader("🤖 ИИ Помощник для встреч")
        
        # Генерация повестки встречи
        st.subheader("📝 Генерация повестки")
        
        with st.form("meeting_agenda"):
            meeting_title = st.text_input("Название встречи:")
            meeting_purpose = st.text_area("Цель встречи:")
            meeting_participants = st.text_input("Участники (через запятую):")
            meeting_duration = st.number_input("Длительность (мин):", min_value=15, max_value=240, value=60)
            
            if st.form_submit_button("🤖 Сгенерировать повестку"):
                if meeting_title and meeting_purpose:
                    with st.spinner("Генерация повестки..."):
                        meeting_info = {
                            'title': meeting_title,
                            'purpose': meeting_purpose,
                            'participants': meeting_participants.split(',') if meeting_participants else [],
                            'duration': f"{meeting_duration} минут"
                        }
                        
                        @async_to_sync
                        async def generate_agenda():
                            return await llm_client.generate_meeting_agenda(meeting_info)
                        
                        agenda = generate_agenda()
                        
                        st.subheader("📋 Повестка встречи")
                        st.markdown(agenda)

if __name__ == "__main__":
    main()