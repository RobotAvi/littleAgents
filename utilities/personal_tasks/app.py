"""
Утилита для личных поручений
Управление персональными задачами, напоминаниями и личной продуктивностью.
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
        "Личные поручения", 
        "Управление персональными задачами и повышение продуктивности"
    )
    
    # Боковая панель с настройками
    with st.sidebar:
        st.header("⚙️ Настройки")
        
        # Категории задач
        task_categories = st.multiselect(
            "Категории задач:",
            ["Работа", "Личное", "Обучение", "Здоровье", "Финансы", "Хобби"],
            default=["Работа", "Личное"]
        )
        
        # Приоритет
        priority_filter = st.selectbox(
            "Показать приоритет:",
            ["Все", "Высокий", "Средний", "Низкий"],
            index=0
        )
        
        # Статус
        status_filter = st.selectbox(
            "Статус задач:",
            ["Все", "Активные", "Завершенные", "Отложенные"],
            index=1
        )
        
        if st.button("🔄 Обновить", type="primary"):
            st.rerun()
    
    # Основное содержимое
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Задачи", "⏰ Календарь", "📊 Продуктивность", "🤖 ИИ Помощник"
    ])
    
    with tab1:
        st.subheader("📋 Управление задачами")
        
        # Быстрое добавление задачи
        with st.form("quick_task"):
            st.subheader("➕ Быстро добавить задачу")
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                task_text = st.text_input("Что нужно сделать?", placeholder="Например: Купить продукты")
            
            with col2:
                if st.form_submit_button("Добавить", use_container_width=True):
                    if task_text:
                        st.success(f"Задача добавлена: {task_text}")
        
        # Список задач на сегодня
        st.subheader("📅 Задачи на сегодня")
        
        today_tasks = [
            {"id": 1, "text": "Встреча с командой", "time": "10:00", "priority": "Высокий", "category": "Работа", "done": False},
            {"id": 2, "text": "Купить продукты", "time": "18:00", "priority": "Средний", "category": "Личное", "done": False},
            {"id": 3, "text": "Прочитать статью по ML", "time": "20:00", "priority": "Низкий", "category": "Обучение", "done": True}
        ]
        
        for task in today_tasks:
            col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
            
            with col1:
                done = st.checkbox("", value=task["done"], key=f"task_{task['id']}")
                if done != task["done"]:
                    st.success("Задача обновлена!")
            
            with col2:
                if task["done"]:
                    st.markdown(f"~~{task['text']}~~")
                else:
                    st.markdown(f"**{task['text']}**")
                st.caption(f"{task['time']} | {task['category']}")
            
            with col3:
                priority_color = {"Высокий": "🔴", "Средний": "🟡", "Низкий": "🟢"}
                st.write(f"{priority_color[task['priority']]}")
            
            with col4:
                if st.button("✏️", key=f"edit_{task['id']}"):
                    st.info("Редактирование задачи...")
        
        # Детальное добавление задачи
        with st.expander("📝 Добавить подробную задачу"):
            with st.form("detailed_task"):
                col1, col2 = st.columns(2)
                
                with col1:
                    detailed_task_text = st.text_input("Название задачи:")
                    task_category = st.selectbox("Категория:", ["Работа", "Личное", "Обучение", "Здоровье", "Финансы", "Хобби"])
                    task_priority = st.selectbox("Приоритет:", ["Высокий", "Средний", "Низкий"])
                
                with col2:
                    task_due_date = st.date_input("Срок выполнения:")
                    task_due_time = st.time_input("Время:")
                    task_reminder = st.selectbox("Напоминание:", ["Нет", "За 15 мин", "За час", "За день"])
                
                task_description = st.text_area("Описание/заметки:")
                task_tags = st.text_input("Теги (через запятую):")
                
                if st.form_submit_button("Создать задачу"):
                    if detailed_task_text:
                        st.success(f"Подробная задача '{detailed_task_text}' создана!")
    
    with tab2:
        st.subheader("⏰ Календарь и планирование")
        
        # Выбор даты
        selected_date = st.date_input("Выберите дату:", datetime.now().date())
        
        # События на выбранную дату
        st.subheader(f"📅 План на {selected_date.strftime('%d.%m.%Y')}")
        
        daily_events = [
            {"time": "09:00", "event": "Утренняя зарядка", "type": "Здоровье", "duration": "30 мин"},
            {"time": "10:00", "event": "Встреча с командой", "type": "Работа", "duration": "1 час"},
            {"time": "14:00", "event": "Обед", "type": "Личное", "duration": "1 час"},
            {"time": "16:00", "event": "Код-ревью", "type": "Работа", "duration": "2 часа"},
            {"time": "19:00", "event": "Изучение Python", "type": "Обучение", "duration": "1 час"}
        ]
        
        for event in daily_events:
            col1, col2, col3 = st.columns([1, 3, 1])
            
            with col1:
                st.write(f"**{event['time']}**")
            with col2:
                st.write(f"📌 {event['event']}")
                st.caption(f"{event['type']} • {event['duration']}")
            with col3:
                if st.button("✏️", key=f"edit_event_{event['time']}"):
                    st.info("Редактирование события...")
        
        # Добавление события
        with st.expander("➕ Добавить событие"):
            with st.form("add_event"):
                col1, col2 = st.columns(2)
                
                with col1:
                    event_name = st.text_input("Название события:")
                    event_date = st.date_input("Дата:")
                    event_time = st.time_input("Время:")
                
                with col2:
                    event_duration = st.number_input("Длительность (мин):", min_value=15, value=60)
                    event_type = st.selectbox("Тип:", ["Работа", "Личное", "Обучение", "Здоровье"])
                    event_reminder = st.checkbox("Установить напоминание")
                
                if st.form_submit_button("Добавить событие"):
                    if event_name:
                        st.success(f"Событие '{event_name}' добавлено!")
    
    with tab3:
        st.subheader("📊 Анализ продуктивности")
        
        # Метрики продуктивности
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Задач сегодня", "8", "2")
        with col2:
            st.metric("Выполнено", "5", "1")
        with col3:
            st.metric("% выполнения", "63%", "12%")
        with col4:
            st.metric("Продуктивное время", "6.5ч", "0.5ч")
        
        # График продуктивности
        st.subheader("📈 Динамика продуктивности")
        
        import pandas as pd
        import plotly.express as px
        
        # Симуляция данных продуктивности
        days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
        productivity_data = pd.DataFrame({
            'День': days,
            'Выполнено задач': [8, 6, 9, 7, 5, 3, 4],
            'Запланировано': [10, 8, 11, 9, 8, 5, 6]
        })
        
        fig = px.bar(productivity_data, x='День', y=['Выполнено задач', 'Запланировано'],
                    title="Выполнение задач по дням недели", barmode='group')
        st.plotly_chart(fig, use_container_width=True)
        
        # Анализ времени по категориям
        st.subheader("⏰ Распределение времени")
        
        time_distribution = pd.DataFrame({
            'Категория': ['Работа', 'Личное', 'Обучение', 'Здоровье', 'Отдых'],
            'Время (часы)': [8, 2, 1.5, 1, 3]
        })
        
        fig_pie = px.pie(time_distribution, values='Время (часы)', names='Категория',
                        title="Как проводится время")
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Еженедельная статистика
        st.subheader("📊 Статистика недели")
        
        weekly_stats = {
            "Всего задач": 52,
            "Выполнено": 38,
            "Просрочено": 3,
            "Отложено": 11,
            "Средняя оценка дня": 7.8,
            "Самый продуктивный день": "Среда",
            "Основная категория": "Работа (65%)"
        }
        
        for key, value in weekly_stats.items():
            st.markdown(f"**{key}:** {value}")
    
    with tab4:
        st.subheader("🤖 ИИ Помощник по продуктивности")
        
        # Анализ продуктивности
        if st.button("📊 Анализ моей продуктивности", type="primary"):
            with st.spinner("Анализ паттернов продуктивности..."):
                
                productivity_data = """
                Данные о продуктивности за неделю:
                
                Выполнено задач: 38 из 52 (73%)
                Просрочено: 3 задачи
                Средняя оценка дня: 7.8/10
                
                Распределение времени:
                - Работа: 8 часов (53%)
                - Личное: 2 часа (13%)
                - Обучение: 1.5 часа (10%)
                - Здоровье: 1 час (7%)
                - Отдых: 3 часа (20%)
                
                Самые продуктивные дни: Среда, Понедельник
                Проблемные области: Просроченные задачи, мало времени на обучение
                """
                
                @async_to_sync
                async def analyze_productivity():
                    return await llm_client.analyze_text(
                        productivity_data,
                        "Проанализируй продуктивность пользователя. "
                        "Выдели сильные стороны, проблемы и дай рекомендации по улучшению."
                    )
                
                analysis = analyze_productivity()
                
                st.subheader("📝 Анализ продуктивности")
                st.markdown(analysis)
        
        # Генерация плана дня
        st.subheader("📅 Планирование дня")
        
        with st.form("generate_plan"):
            col1, col2 = st.columns(2)
            
            with col1:
                plan_date = st.date_input("Дата планирования:")
                work_hours = st.number_input("Рабочих часов:", min_value=1, max_value=12, value=8)
                
            with col2:
                energy_level = st.selectbox("Уровень энергии:", ["Высокий", "Средний", "Низкий"])
                focus_areas = st.multiselect("Приоритетные области:", ["Работа", "Личное", "Обучение", "Здоровье"])
            
            if st.form_submit_button("🤖 Сгенерировать план дня"):
                st.success("План дня создан!")
                
                sample_plan = f"""
                **План на {plan_date.strftime('%d.%m.%Y')}**
                
                🌅 **Утро (9:00-12:00)**
                - Самые важные рабочие задачи (высокая концентрация)
                - Приоритетные проекты
                
                🌞 **День (12:00-15:00)**  
                - Встречи и коммуникация
                - Менее сложные задачи
                
                🌆 **Вечер (15:00-18:00)**
                - Завершение текущих дел
                - Планирование на завтра
                - Обучение или личные задачи
                """
                
                st.markdown(sample_plan)

if __name__ == "__main__":
    main()