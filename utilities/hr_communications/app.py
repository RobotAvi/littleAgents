"""
Утилита для HR и коммуникаций
Проведение 1:1 встреч, фидбек сессий и анализ настроений команды.
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
        "HR и коммуникации", 
        "Проведение 1:1 встреч и анализ настроений команды"
    )
    
    # Боковая панель с настройками
    with st.sidebar:
        st.header("⚙️ Настройки")
        
        # Роль пользователя
        user_role = st.selectbox(
            "Ваша роль:",
            ["HR Manager", "Team Lead", "Manager", "Employee"],
            index=0
        )
        
        # Команда/отдел
        team_filter = st.selectbox(
            "Команда/отдел:",
            ["Все", "Разработка", "QA", "Дизайн", "Продукт"],
            index=0
        )
        
        # Период анализа
        analysis_period = st.selectbox(
            "Период анализа:",
            ["Последний месяц", "Квартал", "Полгода"],
            index=0
        )
        
        if st.button("🔄 Обновить данные", type="primary"):
            st.rerun()
    
    # Основное содержимое
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Обзор", "👥 1:1 Встречи", "📝 Фидбек", "📈 Аналитика"
    ])
    
    with tab1:
        st.subheader("📊 Обзор команды")
        
        # Ключевые метрики
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Сотрудников", "24", "2")
        with col2:
            st.metric("Настроение", "8.2/10", "0.3")
        with col3:
            st.metric("1:1 за месяц", "18", "3")
        with col4:
            st.metric("Обратная связь", "15", "5")
        
        # Настроение команды
        st.subheader("😊 Настроение команды")
        
        import pandas as pd
        import plotly.express as px
        
        # Симуляция данных настроения
        mood_data = pd.DataFrame({
            'date': pd.date_range(start='2024-01-01', periods=30, freq='D'),
            'mood_score': [7.5 + i*0.02 + (i % 7)*0.5 for i in range(30)]
        })
        
        fig = px.line(mood_data, x='date', y='mood_score', 
                     title="Динамика настроения команды")
        st.plotly_chart(fig, use_container_width=True)
        
        # Статус сотрудников
        st.subheader("👥 Статус сотрудников")
        
        employees = [
            {"name": "Иван Иванов", "role": "Developer", "mood": 8.5, "last_1on1": "5 дней назад"},
            {"name": "Петр Петров", "role": "QA", "mood": 7.2, "last_1on1": "2 недели назад"},
            {"name": "Анна Сидорова", "role": "Designer", "mood": 9.1, "last_1on1": "1 неделя назад"}
        ]
        
        for emp in employees:
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                st.write(f"👤 **{emp['name']}**")
                st.write(f"_{emp['role']}_")
            with col2:
                mood = emp['mood']
                if mood >= 8:
                    st.success(f"😊 {mood}")
                elif mood >= 6:
                    st.warning(f"😐 {mood}")
                else:
                    st.error(f"😞 {mood}")
            with col3:
                st.write(f"📅 {emp['last_1on1']}")
            with col4:
                if st.button("📞", key=f"schedule_{emp['name']}"):
                    st.success(f"1:1 запланирована с {emp['name']}")
    
    with tab2:
        st.subheader("👥 1:1 Встречи")
        
        # Запланированные встречи
        st.subheader("📅 Запланированные встречи")
        
        upcoming_meetings = [
            {"employee": "Иван Иванов", "date": "Завтра 14:00", "type": "Регулярная", "status": "Подтверждена"},
            {"employee": "Анна Сидорова", "date": "Пятница 10:00", "type": "Обратная связь", "status": "Ожидает"}
        ]
        
        for meeting in upcoming_meetings:
            with st.expander(f"📅 {meeting['employee']} - {meeting['date']}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Сотрудник:** {meeting['employee']}")
                    st.markdown(f"**Время:** {meeting['date']}")
                    st.markdown(f"**Тип:** {meeting['type']}")
                    st.markdown(f"**Статус:** {meeting['status']}")
                
                with col2:
                    if st.button(f"Подготовиться", key=f"prep_{meeting['employee']}"):
                        st.info("Генерация вопросов для встречи...")
                    if st.button(f"Перенести", key=f"reschedule_{meeting['employee']}"):
                        st.warning("Встреча перенесена")
        
        # Планирование новой встречи
        st.subheader("➕ Запланировать 1:1")
        
        with st.form("schedule_1on1"):
            employee_select = st.selectbox("Сотрудник:", ["Иван Иванов", "Петр Петров", "Анна Сидорова"])
            meeting_date = st.date_input("Дата:")
            meeting_time = st.time_input("Время:")
            meeting_type = st.selectbox("Тип встречи:", ["Регулярная", "Обратная связь", "Развитие карьеры", "Проблемы"])
            meeting_notes = st.text_area("Заметки/Цели:")
            
            if st.form_submit_button("Запланировать встречу"):
                st.success(f"1:1 с {employee_select} запланирована на {meeting_date} {meeting_time}")
    
    with tab3:
        st.subheader("📝 Управление фидбеком")
        
        # Сбор обратной связи
        st.subheader("📊 Сбор обратной связи")
        
        with st.form("feedback_form"):
            feedback_type = st.selectbox("Тип фидбека:", ["360 градусов", "Самооценка", "От руководителя", "Peer review"])
            feedback_employee = st.selectbox("Сотрудник:", ["Иван Иванов", "Петр Петров", "Анна Сидорова"])
            feedback_period = st.selectbox("Период:", ["Квартал", "Полгода", "Год"])
            
            # Критерии оценки
            st.subheader("Критерии оценки (1-10):")
            
            technical_skills = st.slider("Технические навыки:", 1, 10, 7)
            communication = st.slider("Коммуникация:", 1, 10, 8)
            teamwork = st.slider("Работа в команде:", 1, 10, 8)
            initiative = st.slider("Инициативность:", 1, 10, 6)
            problem_solving = st.slider("Решение проблем:", 1, 10, 7)
            
            feedback_comments = st.text_area("Комментарии:")
            
            if st.form_submit_button("Сохранить фидбек"):
                st.success("Обратная связь сохранена!")
        
        # История фидбека
        st.subheader("📚 История обратной связи")
        
        feedback_history = [
            {"employee": "Иван Иванов", "date": "01.12.2023", "type": "Квартальная оценка", "score": 8.2},
            {"employee": "Петр Петров", "date": "15.11.2023", "type": "360 градусов", "score": 7.5}
        ]
        
        for feedback in feedback_history:
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                st.write(f"👤 {feedback['employee']}")
            with col2:
                st.write(feedback['date'])
            with col3:
                st.write(feedback['type'])
            with col4:
                score = feedback['score']
                if score >= 8:
                    st.success(f"⭐ {score}")
                elif score >= 6:
                    st.warning(f"⚡ {score}")
                else:
                    st.error(f"⚠️ {score}")
    
    with tab4:
        st.subheader("📈 HR Аналитика")
        
        # Анализ настроений с помощью ИИ
        if st.button("🤖 Анализ настроений команды", type="primary"):
            with st.spinner("Анализ данных..."):
                
                team_data = """
                Данные по команде за последний месяц:
                
                Настроение команды: 8.2/10 (улучшение на 0.3)
                Проведено 1:1 встреч: 18
                Собрано отзывов: 15
                
                Ключевые показатели:
                - Технические навыки: средний балл 7.5
                - Коммуникация: средний балл 8.1
                - Работа в команде: средний балл 8.3
                - Инициативность: средний балл 6.8
                
                Проблемные области:
                - 2 сотрудника не проводили 1:1 более 2 недель
                - Низкие оценки по инициативности
                """
                
                @async_to_sync
                async def analyze_team():
                    return await llm_client.analyze_text(
                        team_data,
                        "Проанализируй состояние команды с точки зрения HR. "
                        "Выдели проблемы, риски и рекомендации по улучшению."
                    )
                
                analysis = analyze_team()
                
                st.subheader("📝 Анализ команды")
                st.markdown(analysis)
        
        # Отчеты
        st.subheader("📊 Отчеты")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📈 Отчет по настроениям"):
                st.info("Генерация отчета по настроениям команды...")
        
        with col2:
            if st.button("👥 Отчет по 1:1"):
                st.info("Генерация отчета по проведенным 1:1...")
        
        with col3:
            if st.button("📝 Отчет по фидбеку"):
                st.info("Генерация отчета по обратной связи...")

if __name__ == "__main__":
    main()