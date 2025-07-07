"""
Утилита для организации мероприятий
Планирование и координация корпоративных событий, конференций и встреч.
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
        "Организация мероприятий", 
        "Планирование корпоративных событий и управление мероприятиями"
    )
    
    # Боковая панель с настройками
    with st.sidebar:
        st.header("⚙️ Настройки")
        
        # Тип мероприятия
        event_type = st.selectbox(
            "Тип мероприятия:",
            ["Конференция", "Семинар", "Корпоратив", "Тимбилдинг", "Презентация"],
            index=0
        )
        
        # Бюджет
        budget_range = st.selectbox(
            "Бюджет:",
            ["До $1,000", "$1,000-$5,000", "$5,000-$10,000", "Свыше $10,000"],
            index=1
        )
        
        # Количество участников
        attendees_count = st.number_input("Ожидаемое количество участников:", min_value=1, value=50)
        
        if st.button("🔄 Обновить", type="primary"):
            st.rerun()
    
    # Основное содержимое
    tab1, tab2, tab3, tab4 = st.tabs([
        "📅 Планирование", "👥 Участники", "📋 Задачи", "📊 Аналитика"
    ])
    
    with tab1:
        st.subheader("📅 Планирование мероприятия")
        
        # Создание нового мероприятия
        with st.expander("➕ Создать новое мероприятие"):
            with st.form("new_event"):
                col1, col2 = st.columns(2)
                
                with col1:
                    event_name = st.text_input("Название мероприятия:")
                    event_date = st.date_input("Дата проведения:")
                    event_time = st.time_input("Время начала:")
                    event_duration = st.number_input("Длительность (часы):", min_value=0.5, value=2.0, step=0.5)
                
                with col2:
                    event_location = st.text_input("Место проведения:")
                    event_budget = st.number_input("Бюджет ($):", min_value=0.0, value=2000.0)
                    event_format = st.selectbox("Формат:", ["Очно", "Онлайн", "Гибридный"])
                    event_capacity = st.number_input("Вместимость:", min_value=1, value=100)
                
                event_description = st.text_area("Описание мероприятия:")
                event_goals = st.text_area("Цели и задачи:")
                
                if st.form_submit_button("Создать мероприятие"):
                    if event_name and event_date:
                        st.success(f"Мероприятие '{event_name}' создано!")
        
        # Предстоящие мероприятия
        st.subheader("📆 Предстоящие мероприятия")
        
        upcoming_events = [
            {
                "name": "Tech Conference 2024",
                "date": "2024-02-15",
                "time": "10:00",
                "location": "Конференц-зал А",
                "attendees": 120,
                "status": "Планирование"
            },
            {
                "name": "Quarterly Review",
                "date": "2024-02-20",
                "time": "14:00",
                "location": "Офис, переговорная",
                "attendees": 25,
                "status": "Готово"
            }
        ]
        
        for event in upcoming_events:
            with st.expander(f"🎯 {event['name']} - {event['date']}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Дата:** {event['date']} в {event['time']}")
                    st.markdown(f"**Место:** {event['location']}")
                    st.markdown(f"**Участников:** {event['attendees']}")
                    st.markdown(f"**Статус:** {event['status']}")
                
                with col2:
                    if st.button(f"Редактировать", key=f"edit_{event['name']}"):
                        st.info("Редактирование мероприятия...")
                    if st.button(f"Детали", key=f"details_{event['name']}"):
                        st.info("Просмотр деталей...")
        
        # Шаблоны мероприятий
        st.subheader("📋 Шаблоны мероприятий")
        
        templates = {
            "Конференция": {
                "duration": "8 часов",
                "tasks": ["Бронирование зала", "Приглашение спикеров", "Регистрация участников", "Кейтеринг"],
                "budget": "$5,000-$15,000"
            },
            "Семинар": {
                "duration": "3-4 часа", 
                "tasks": ["Подготовка материалов", "Бронирование переговорной", "Кофе-брейк"],
                "budget": "$500-$2,000"
            },
            "Корпоратив": {
                "duration": "4-6 часов",
                "tasks": ["Выбор ресторана", "Развлекательная программа", "Транспорт", "Подарки"],
                "budget": "$3,000-$10,000"
            }
        }
        
        selected_template = st.selectbox("Выберите шаблон:", list(templates.keys()))
        
        if st.button("📝 Применить шаблон"):
            template = templates[selected_template]
            st.success(f"Шаблон '{selected_template}' применен!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Длительность:** {template['duration']}")
                st.markdown(f"**Бюджет:** {template['budget']}")
            
            with col2:
                st.markdown("**Типовые задачи:**")
                for task in template['tasks']:
                    st.markdown(f"- {task}")
    
    with tab2:
        st.subheader("👥 Управление участниками")
        
        # Статистика участников
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Приглашено", "150", "25")
        with col2:
            st.metric("Подтвердили", "85", "15")
        with col3:
            st.metric("Отказались", "12", "3")
        with col4:
            st.metric("Ожидают ответа", "53", "7")
        
        # Приглашение участников
        with st.expander("📧 Массовое приглашение"):
            with st.form("mass_invite"):
                email_list = st.text_area("Email адреса (по одному на строку):")
                invite_template = st.selectbox("Шаблон приглашения:", ["Официальный", "Дружелюбный", "Краткий"])
                send_date = st.date_input("Дата отправки:")
                
                st.subheader("Предварительный просмотр:")
                preview_text = """
                Тема: Приглашение на Tech Conference 2024
                
                Уважаемый коллега,
                
                Приглашаем Вас принять участие в Tech Conference 2024.
                Дата: 15 февраля 2024
                Время: 10:00-18:00
                Место: Конференц-зал А
                
                Для подтверждения участия перейдите по ссылке...
                """
                st.text(preview_text)
                
                if st.form_submit_button("📤 Отправить приглашения"):
                    st.success("Приглашения отправлены!")
        
        # Список участников
        st.subheader("📋 Список участников")
        
        participants = [
            {"name": "Анна Иванова", "email": "anna@company.com", "status": "Подтвердил", "role": "Спикер"},
            {"name": "Петр Петров", "email": "petr@company.com", "status": "Ожидает", "role": "Участник"},
            {"name": "Мария Сидорова", "email": "maria@company.com", "status": "Отказался", "role": "Участник"}
        ]
        
        for participant in participants:
            col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
            
            with col1:
                st.write(f"👤 **{participant['name']}**")
            with col2:
                st.write(participant['email'])
            with col3:
                if participant['status'] == 'Подтвердил':
                    st.success("✅")
                elif participant['status'] == 'Отказался':
                    st.error("❌")
                else:
                    st.warning("⏳")
            with col4:
                st.write(participant['role'])
        
        # Регистрация на месте
        st.subheader("📝 Быстрая регистрация")
        
        with st.form("quick_registration"):
            col1, col2 = st.columns(2)
            
            with col1:
                reg_name = st.text_input("Имя участника:")
                reg_email = st.text_input("Email:")
            
            with col2:
                reg_company = st.text_input("Компания:")
                reg_role = st.selectbox("Роль:", ["Участник", "Спикер", "Партнер", "Пресса"])
            
            if st.form_submit_button("Зарегистрировать"):
                if reg_name and reg_email:
                    st.success(f"Участник {reg_name} зарегистрирован!")
    
    with tab3:
        st.subheader("📋 Управление задачами")
        
        # Создание задачи
        with st.expander("➕ Создать задачу"):
            with st.form("create_task"):
                col1, col2 = st.columns(2)
                
                with col1:
                    task_title = st.text_input("Название задачи:")
                    task_assignee = st.text_input("Ответственный:")
                    task_priority = st.selectbox("Приоритет:", ["Высокий", "Средний", "Низкий"])
                
                with col2:
                    task_due_date = st.date_input("Срок выполнения:")
                    task_category = st.selectbox("Категория:", ["Подготовка", "Логистика", "Техника", "Кейтеринг"])
                    task_budget = st.number_input("Бюджет ($):", min_value=0.0, value=0.0)
                
                task_description = st.text_area("Описание задачи:")
                
                if st.form_submit_button("Создать задачу"):
                    if task_title:
                        st.success(f"Задача '{task_title}' создана!")
        
        # Список задач
        st.subheader("📚 Список задач")
        
        tasks = [
            {"title": "Бронирование конференц-зала", "assignee": "Анна И.", "due": "2024-01-20", "status": "Выполнена", "priority": "Высокий"},
            {"title": "Заказ кейтеринга", "assignee": "Петр П.", "due": "2024-01-25", "status": "В работе", "priority": "Средний"},
            {"title": "Настройка АВ оборудования", "assignee": "Иван С.", "due": "2024-02-10", "status": "Ожидает", "priority": "Высокий"},
            {"title": "Печать материалов", "assignee": "Мария К.", "due": "2024-02-12", "status": "Ожидает", "priority": "Низкий"}
        ]
        
        # Фильтры
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_filter = st.selectbox("Статус:", ["Все", "Ожидает", "В работе", "Выполнена"])
        with col2:
            priority_filter = st.selectbox("Приоритет:", ["Все", "Высокий", "Средний", "Низкий"])
        with col3:
            assignee_filter = st.text_input("Ответственный:")
        
        for task in tasks:
            with st.expander(f"📋 {task['title']} | {task['due']}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Ответственный:** {task['assignee']}")
                    st.markdown(f"**Срок:** {task['due']}")
                    st.markdown(f"**Приоритет:** {task['priority']}")
                
                with col2:
                    if task['status'] == 'Выполнена':
                        st.success("✅ Выполнена")
                    elif task['status'] == 'В работе':
                        st.warning("⏳ В работе")
                    else:
                        st.info("📋 Ожидает")
                    
                    if st.button("Изменить статус", key=f"status_{task['title']}"):
                        st.success("Статус обновлен!")
    
    with tab4:
        st.subheader("📊 Аналитика мероприятий")
        
        # Генерация отчета с ИИ
        if st.button("🤖 Анализ эффективности", type="primary"):
            with st.spinner("Анализ данных мероприятий..."):
                
                event_data = f"""
                Статистика по мероприятиям:
                
                Проведено мероприятий: 12 за квартал
                Общее количество участников: 850
                Средняя посещаемость: 78%
                Общий бюджет: $45,000
                Средний бюджет на участника: $53
                
                Типы мероприятий:
                - Конференции: 4 (350 участников)
                - Семинары: 6 (280 участников)
                - Корпоративы: 2 (220 участников)
                
                Показатели эффективности:
                - Satisfaction Score: 8.3/10
                - NPS: 72
                - Повторная посещаемость: 65%
                """
                
                @async_to_sync
                async def analyze_events():
                    return await llm_client.analyze_text(
                        event_data,
                        "Проанализируй эффективность проведенных мероприятий. "
                        "Выдели успешные практики, проблемы и рекомендации по улучшению."
                    )
                
                analysis = analyze_events()
                
                st.subheader("📝 Анализ эффективности")
                st.markdown(analysis)
        
        # Статистика и метрики
        st.subheader("📈 Ключевые метрики")
        
        import pandas as pd
        import plotly.express as px
        
        # График посещаемости
        months = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн']
        attendance_data = pd.DataFrame({
            'Месяц': months,
            'Запланировано': [100, 80, 120, 90, 110, 95],
            'Фактически': [85, 75, 95, 78, 88, 82]
        })
        
        fig = px.bar(attendance_data, x='Месяц', y=['Запланировано', 'Фактически'],
                    title="Посещаемость мероприятий", barmode='group')
        st.plotly_chart(fig, use_container_width=True)
        
        # Отчеты
        st.subheader("📄 Отчеты")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Отчет по бюджету"):
                st.success("Финансовый отчет сгенерирован!")
        
        with col2:
            if st.button("👥 Отчет по участникам"):
                st.success("Отчет по участникам готов!")
        
        with col3:
            if st.button("📈 Сводная аналитика"):
                st.success("Аналитический отчет создан!")

if __name__ == "__main__":
    main()