"""
Утилита для управления проектами
Актуализация планов MS Project и синхронизация с системами управления задачами.
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
        "Управление проектами", 
        "Актуализация планов MS Project и управление ресурсами"
    )
    
    # Боковая панель с настройками
    with st.sidebar:
        st.header("⚙️ Настройки")
        
        # Проект
        selected_project = st.selectbox(
            "Текущий проект:",
            ["Проект A", "Проект B", "Проект C", "Новый проект"],
            index=0
        )
        
        # Методология
        methodology = st.selectbox(
            "Методология:",
            ["Agile", "Waterfall", "Kanban", "Scrum"],
            index=0
        )
        
        # Период отчета
        report_period = st.selectbox(
            "Период отчета:",
            ["Текущая неделя", "Текущий месяц", "Квартал"],
            index=0
        )
        
        if st.button("🔄 Синхронизировать", type="primary"):
            st.rerun()
    
    # Основное содержимое
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Дашборд", "📋 Задачи", "👥 Ресурсы", "📈 Отчеты"
    ])
    
    with tab1:
        st.subheader("📊 Обзор проекта")
        
        # Ключевые метрики
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Прогресс", "67%", "5%")
        with col2:
            st.metric("Задач выполнено", "34/51", "3")
        with col3:
            st.metric("Дней до дедлайна", "23", "-2")
        with col4:
            st.metric("Бюджет", "85%", "-5%")
        
        # Статус проекта
        st.subheader("🎯 Статус проекта")
        
        project_info = {
            "Название": selected_project,
            "Статус": "В работе",
            "Начало": "01.01.2024",
            "Окончание": "31.03.2024",
            "Команда": "8 человек",
            "Бюджет": "$50,000"
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            for key, value in list(project_info.items())[:3]:
                st.markdown(f"**{key}:** {value}")
        
        with col2:
            for key, value in list(project_info.items())[3:]:
                st.markdown(f"**{key}:** {value}")
        
        # Диаграмма Ганта (имитация)
        st.subheader("📅 Временная шкала")
        
        import pandas as pd
        
        tasks_timeline = [
            {"Задача": "Планирование", "Начало": "2024-01-01", "Конец": "2024-01-15", "Прогресс": 100},
            {"Задача": "Разработка", "Начало": "2024-01-16", "Конец": "2024-02-28", "Прогресс": 70},
            {"Задача": "Тестирование", "Начало": "2024-02-15", "Конец": "2024-03-15", "Прогресс": 30},
            {"Задача": "Деплой", "Начало": "2024-03-16", "Конец": "2024-03-31", "Прогресс": 0}
        ]
        
        df = pd.DataFrame(tasks_timeline)
        st.dataframe(df, use_container_width=True)
    
    with tab2:
        st.subheader("📋 Управление задачами")
        
        # Фильтры
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_filter = st.selectbox("Статус:", ["Все", "Открыта", "В работе", "Завершена"])
        with col2:
            priority_filter = st.selectbox("Приоритет:", ["Все", "Высокий", "Средний", "Низкий"])
        with col3:
            assignee_filter = st.text_input("Исполнитель:")
        
        # Создание задачи
        with st.expander("➕ Создать новую задачу"):
            with st.form("new_task"):
                task_name = st.text_input("Название задачи:")
                task_description = st.text_area("Описание:")
                task_assignee = st.selectbox("Исполнитель:", ["Dev A", "Dev B", "QA Engineer", "Designer"])
                task_priority = st.selectbox("Приоритет:", ["Высокий", "Средний", "Низкий"])
                task_due_date = st.date_input("Срок:")
                
                if st.form_submit_button("Создать задачу"):
                    if task_name:
                        st.success(f"Задача '{task_name}' создана!")
        
        # Список задач
        st.subheader("📚 Список задач")
        
        tasks = [
            {"id": "PROJ-1", "name": "Настройка CI/CD", "assignee": "Dev A", "status": "В работе", "priority": "Высокий"},
            {"id": "PROJ-2", "name": "Создание API", "assignee": "Dev B", "status": "Завершена", "priority": "Высокий"},
            {"id": "PROJ-3", "name": "Дизайн UI", "assignee": "Designer", "status": "Открыта", "priority": "Средний"}
        ]
        
        for task in tasks:
            with st.expander(f"📋 {task['id']}: {task['name']}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Исполнитель:** {task['assignee']}")
                    st.markdown(f"**Приоритет:** {task['priority']}")
                    st.markdown(f"**Статус:** {task['status']}")
                
                with col2:
                    if st.button(f"Редактировать", key=f"edit_{task['id']}"):
                        st.info("Редактирование...")
                    if st.button(f"Комментарий", key=f"comment_{task['id']}"):
                        st.info("Добавить комментарий...")
    
    with tab3:
        st.subheader("👥 Управление ресурсами")
        
        # Команда проекта
        st.subheader("👥 Команда проекта")
        
        team_members = [
            {"name": "Иван Иванов", "role": "Team Lead", "workload": "90%", "tasks": 5},
            {"name": "Петр Петров", "role": "Developer", "workload": "75%", "tasks": 3},
            {"name": "Анна Сидорова", "role": "QA Engineer", "workload": "60%", "tasks": 4},
            {"name": "Мария Козлова", "role": "Designer", "workload": "40%", "tasks": 2}
        ]
        
        for member in team_members:
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                st.write(f"👤 **{member['name']}**")
                st.write(f"_{member['role']}_")
            with col2:
                workload = int(member['workload'].rstrip('%'))
                if workload > 80:
                    st.error(f"🔴 {member['workload']}")
                elif workload > 60:
                    st.warning(f"🟡 {member['workload']}")
                else:
                    st.success(f"🟢 {member['workload']}")
            with col3:
                st.write(f"📋 {member['tasks']} задач")
            with col4:
                if st.button("📊", key=f"details_{member['name']}"):
                    st.info(f"Детали по {member['name']}")
        
        # Планирование ресурсов
        st.subheader("📅 Планирование ресурсов")
        
        if st.button("🎯 Оптимизировать распределение"):
            st.success("Ресурсы перераспределены для оптимальной загрузки!")
    
    with tab4:
        st.subheader("📈 Отчеты по проекту")
        
        # Генерация отчета
        if st.button("📊 Сгенерировать отчет", type="primary"):
            with st.spinner("Создание отчета..."):
                
                project_data = f"""
                Проект: {selected_project}
                Методология: {methodology}
                Период: {report_period}
                
                Прогресс: 67%
                Выполнено задач: 34 из 51
                Команда: 4 человека
                Бюджет использован: 85%
                """
                
                @async_to_sync
                async def generate_report():
                    return await llm_client.analyze_text(
                        project_data,
                        "Создай подробный отчет по состоянию проекта. "
                        "Включи анализ прогресса, рисков, рекомендации по улучшению."
                    )
                
                report = generate_report()
                
                st.subheader("📄 Отчет по проекту")
                st.markdown(report)
        
        # Экспорт отчетов
        st.subheader("📤 Экспорт отчетов")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Excel отчет"):
                st.success("Excel отчет сгенерирован!")
        
        with col2:
            if st.button("📄 PDF отчет"):
                st.success("PDF отчет сгенерирован!")
        
        with col3:
            if st.button("📧 Отправить email"):
                st.success("Отчет отправлен по email!")

if __name__ == "__main__":
    main()