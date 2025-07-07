"""
Утилита для ведения встреч
Протоколирование встреч, создание задач и рассылка итогов.
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
from datetime import datetime

def main():
    create_streamlit_header(
        "Ведение встреч", 
        "Протоколирование встреч и создание итоговых отчетов"
    )
    
    # Боковая панель с настройками
    with st.sidebar:
        st.header("⚙️ Настройки")
        
        # Активная встреча
        active_meeting = st.selectbox(
            "Активная встреча:",
            ["Планерка команды", "1:1 с менеджером", "Демо клиенту", "Новая встреча"],
            index=0
        )
        
        # Автосохранение
        auto_save = st.checkbox("Автосохранение заметок", True)
        
        # Шаблон протокола
        protocol_template = st.selectbox(
            "Шаблон протокола:",
            ["Стандартный", "Agile", "Корпоративный"],
            index=0
        )
        
        if st.button("🔄 Обновить", type="primary"):
            st.rerun()
    
    # Основное содержимое
    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Протокол", "✅ Решения", "📋 Задачи", "📧 Рассылка"
    ])
    
    with tab1:
        st.subheader("📝 Протокол встречи")
        
        # Информация о встрече
        col1, col2 = st.columns(2)
        
        with col1:
            meeting_date = st.date_input("Дата встречи:", datetime.now().date())
            meeting_time = st.time_input("Время:", datetime.now().time())
        
        with col2:
            meeting_duration = st.number_input("Длительность (мин):", min_value=15, value=60)
            meeting_type = st.selectbox("Тип встречи:", ["Планерка", "1:1", "Демо", "Ретроспектива"])
        
        # Участники
        st.subheader("👥 Участники")
        participants = st.text_area(
            "Участники (по одному на строку):",
            value="Иван Иванов (ведущий)\nПетр Петров\nМария Сидорова"
        )
        
        # Повестка дня
        st.subheader("📋 Повестка дня")
        agenda = st.text_area(
            "Основные вопросы:",
            value="1. Обзор прогресса по задачам\n2. Обсуждение блокеров\n3. Планирование на следующую неделю",
            height=150
        )
        
        # Заметки
        st.subheader("📝 Заметки встречи")
        meeting_notes = st.text_area(
            "Записи в ходе встречи:",
            placeholder="Введите заметки здесь...",
            height=200
        )
        
        # Кнопки действий
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Сохранить протокол"):
                st.success("Протокол сохранен!")
        
        with col2:
            if st.button("📤 Экспорт в PDF"):
                st.info("Экспорт в PDF...")
        
        with col3:
            if st.button("📋 Создать шаблон"):
                st.success("Шаблон создан!")
    
    with tab2:
        st.subheader("✅ Принятые решения")
        
        # Добавление решения
        with st.form("add_decision"):
            st.subheader("➕ Добавить решение")
            
            decision_text = st.text_area("Описание решения:")
            decision_owner = st.text_input("Ответственный:")
            decision_deadline = st.date_input("Срок исполнения:")
            decision_priority = st.selectbox("Приоритет:", ["Высокий", "Средний", "Низкий"])
            
            if st.form_submit_button("Добавить решение"):
                if decision_text:
                    st.success("Решение добавлено!")
        
        # Список решений
        st.subheader("📋 Список решений")
        
        decisions = [
            {
                "text": "Изменить архитектуру базы данных",
                "owner": "Разработчик А",
                "deadline": "2024-01-15",
                "priority": "Высокий",
                "status": "В работе"
            },
            {
                "text": "Провести код-ревью",
                "owner": "Тимлид",
                "deadline": "2024-01-10",
                "priority": "Средний", 
                "status": "Завершено"
            }
        ]
        
        for i, decision in enumerate(decisions):
            with st.expander(f"✅ Решение {i+1}: {decision['text'][:50]}..."):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Описание:** {decision['text']}")
                    st.markdown(f"**Ответственный:** {decision['owner']}")
                    st.markdown(f"**Срок:** {decision['deadline']}")
                
                with col2:
                    priority_color = {"Высокий": "🔴", "Средний": "🟡", "Низкий": "🟢"}
                    st.markdown(f"**Приоритет:** {priority_color[decision['priority']]} {decision['priority']}")
                    
                    if decision['status'] == 'Завершено':
                        st.success("✅ Завершено")
                    else:
                        st.warning("⏳ В работе")
    
    with tab3:
        st.subheader("📋 Задачи из встречи")
        
        # Автоматическое создание задач
        if st.button("🤖 Создать задачи из заметок", type="primary"):
            if 'meeting_notes' in locals() and meeting_notes:
                with st.spinner("Анализ заметок и создание задач..."):
                    
                    @async_to_sync
                    async def create_tasks():
                        return await llm_client.create_action_items(meeting_notes)
                    
                    action_items = create_tasks()
                    
                    st.subheader("📝 Предлагаемые задачи")
                    st.markdown(action_items)
                    
                    if st.button("✅ Подтвердить создание задач"):
                        st.success("Задачи созданы и добавлены в трекер!")
            else:
                st.warning("Сначала добавьте заметки встречи")
        
        # Ручное добавление задач
        with st.form("add_task"):
            st.subheader("➕ Добавить задачу вручную")
            
            task_title = st.text_input("Название задачи:")
            task_description = st.text_area("Описание:")
            task_assignee = st.text_input("Исполнитель:")
            task_due_date = st.date_input("Срок выполнения:")
            
            if st.form_submit_button("Создать задачу"):
                if task_title:
                    st.success(f"Задача '{task_title}' создана!")
        
        # Список задач
        st.subheader("📚 Задачи из встречи")
        
        tasks = [
            {"title": "Исправить баг в авторизации", "assignee": "Dev A", "status": "Открыта"},
            {"title": "Обновить документацию", "assignee": "Dev B", "status": "В работе"}
        ]
        
        for task in tasks:
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"📋 **{task['title']}**")
            with col2:
                st.write(task['assignee'])
            with col3:
                if task['status'] == 'Открыта':
                    st.info("📋 Открыта")
                else:
                    st.warning("⏳ В работе")
    
    with tab4:
        st.subheader("📧 Рассылка итогов")
        
        # Автоматическая генерация отчета
        if st.button("📝 Сгенерировать отчет о встрече", type="primary"):
            with st.spinner("Создание отчета..."):
                
                # Подготовка данных
                meeting_summary = f"""
                Встреча: {active_meeting}
                Дата: {datetime.now().strftime('%d.%m.%Y')}
                Участники: {participants if 'participants' in locals() else 'Не указаны'}
                
                Основные вопросы:
                {agenda if 'agenda' in locals() else 'Не указаны'}
                
                Заметки:
                {meeting_notes if 'meeting_notes' in locals() and meeting_notes else 'Нет заметок'}
                """
                
                @async_to_sync
                async def generate_summary():
                    return await llm_client.analyze_text(
                        meeting_summary,
                        "Создай структурированный отчет о встрече. "
                        "Выдели ключевые моменты, решения и следующие шаги."
                    )
                
                summary = generate_summary()
                
                st.subheader("📄 Отчет о встрече")
                st.markdown(summary)
        
        # Настройки рассылки
        st.subheader("📮 Настройки рассылки")
        
        with st.form("email_settings"):
            email_recipients = st.text_area(
                "Получатели (email через запятую):",
                value="team@company.com, manager@company.com"
            )
            email_subject = st.text_input(
                "Тема письма:",
                value=f"Итоги встречи: {active_meeting}"
            )
            include_attachments = st.checkbox("Включить протокол как приложение", True)
            
            if st.form_submit_button("📤 Отправить отчет"):
                st.success("Отчет отправлен всем участникам!")

if __name__ == "__main__":
    main()