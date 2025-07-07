"""
Утилита для оптимизации процессов
Анализ и улучшение рутинных процессов, автоматизация повторяющихся задач.
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
        "Оптимизация процессов", 
        "Анализ и улучшение рутинных процессов с помощью ИИ"
    )
    
    # Боковая панель с настройками
    with st.sidebar:
        st.header("⚙️ Настройки")
        
        # Тип процесса
        process_type = st.selectbox(
            "Тип процесса:",
            ["Все", "Административный", "Технический", "HR", "Финансовый"],
            index=0
        )
        
        # Период анализа
        analysis_period = st.selectbox(
            "Период анализа:",
            ["Последняя неделя", "Месяц", "Квартал", "Год"],
            index=1
        )
        
        # Критерий оптимизации
        optimization_criteria = st.selectbox(
            "Приоритет оптимизации:",
            ["Время", "Стоимость", "Качество", "Автоматизация"],
            index=0
        )
        
        if st.button("🔄 Обновить анализ", type="primary"):
            st.rerun()
    
    # Основное содержимое
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Обзор", "🔍 Анализ", "⚡ Оптимизация", "🤖 Автоматизация"
    ])
    
    with tab1:
        st.subheader("📊 Обзор процессов")
        
        # Ключевые метрики
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Процессов", "24", "3")
        with col2:
            st.metric("Среднее время", "2.3ч", "-0.5ч")
        with col3:
            st.metric("Эффективность", "76%", "8%")
        with col4:
            st.metric("Автоматизировано", "35%", "12%")
        
        # Список процессов
        st.subheader("📋 Активные процессы")
        
        processes = [
            {"name": "Обработка входящих писем", "frequency": "Ежедневно", "time": "45 мин", "efficiency": 60, "automation": 30},
            {"name": "Создание отчетов", "frequency": "Еженедельно", "time": "3 часа", "efficiency": 80, "automation": 70},
            {"name": "Одобрение расходов", "frequency": "По запросу", "time": "20 мин", "efficiency": 45, "automation": 10},
            {"name": "Планирование встреч", "frequency": "Ежедневно", "time": "30 мин", "efficiency": 70, "automation": 80}
        ]
        
        for process in processes:
            with st.expander(f"⚙️ {process['name']} | {process['frequency']}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Частота:** {process['frequency']}")
                    st.markdown(f"**Время выполнения:** {process['time']}")
                    
                    # Прогресс бары
                    st.markdown("**Эффективность:**")
                    st.progress(process['efficiency'] / 100)
                    
                    st.markdown("**Автоматизация:**")
                    st.progress(process['automation'] / 100)
                
                with col2:
                    if process['efficiency'] < 60:
                        st.error("🔴 Низкая эффективность")
                    elif process['efficiency'] < 80:
                        st.warning("🟡 Средняя эффективность")
                    else:
                        st.success("🟢 Высокая эффективность")
                    
                    if st.button("Анализировать", key=f"analyze_{process['name']}"):
                        st.info("Запущен детальный анализ процесса")
        
        # Общая эффективность
        st.subheader("📈 Тренды эффективности")
        
        import pandas as pd
        import plotly.express as px
        
        # График эффективности
        weeks = ['Нед 1', 'Нед 2', 'Нед 3', 'Нед 4']
        efficiency_data = pd.DataFrame({
            'Неделя': weeks,
            'Эффективность': [68, 72, 74, 76],
            'Автоматизация': [25, 28, 32, 35]
        })
        
        fig = px.line(efficiency_data, x='Неделя', y=['Эффективность', 'Автоматизация'],
                     title="Динамика показателей")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("🔍 Анализ процессов")
        
        # Выбор процесса для анализа
        selected_process = st.selectbox(
            "Выберите процесс для анализа:",
            ["Обработка входящих писем", "Создание отчетов", "Одобрение расходов", "Планирование встреч"]
        )
        
        if st.button("🔍 Провести анализ", type="primary"):
            with st.spinner("Анализ процесса..."):
                
                # Симуляция анализа процесса
                st.subheader(f"📊 Анализ: {selected_process}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**🕒 Временные затраты:**")
                    time_breakdown = [
                        "Получение данных: 15 мин",
                        "Обработка: 20 мин", 
                        "Проверка: 8 мин",
                        "Отправка: 2 мин"
                    ]
                    for item in time_breakdown:
                        st.markdown(f"- {item}")
                
                with col2:
                    st.markdown("**⚠️ Узкие места:**")
                    bottlenecks = [
                        "Ручная обработка данных",
                        "Ожидание подтверждений",
                        "Поиск информации",
                        "Дублирование действий"
                    ]
                    for item in bottlenecks:
                        st.markdown(f"- {item}")
                
                # Детальный анализ
                st.subheader("📈 Детальная статистика")
                
                analysis_metrics = {
                    "Общее время выполнения": "45 минут",
                    "Время ожидания": "12 минут (27%)",
                    "Время ручной работы": "28 минут (62%)",
                    "Время автоматической обработки": "5 минут (11%)",
                    "Количество шагов": "8",
                    "Количество переключений контекста": "4",
                    "Уровень ошибок": "3%"
                }
                
                for metric, value in analysis_metrics.items():
                    st.markdown(f"**{metric}:** {value}")
        
        # Сравнение с бенчмарками
        st.subheader("📊 Бенчмарки")
        
        benchmark_data = [
            {"metric": "Время выполнения", "current": "45 мин", "industry": "30 мин", "best": "20 мин"},
            {"metric": "Уровень автоматизации", "current": "30%", "industry": "55%", "best": "80%"},
            {"metric": "Удовлетворенность", "current": "7.2/10", "industry": "8.1/10", "best": "9.2/10"}
        ]
        
        for item in benchmark_data:
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                st.write(f"**{item['metric']}**")
            with col2:
                st.write(f"Текущий: {item['current']}")
            with col3:
                st.write(f"Среднее: {item['industry']}")
            with col4:
                st.write(f"Лучший: {item['best']}")
    
    with tab3:
        st.subheader("⚡ Рекомендации по оптимизации")
        
        # Анализ с ИИ
        if st.button("🤖 Получить рекомендации ИИ", type="primary"):
            with st.spinner("Генерация рекомендаций..."):
                
                process_data = f"""
                Анализ процесса "{selected_process if 'selected_process' in locals() else 'Обработка входящих писем'}":
                
                Текущие показатели:
                - Время выполнения: 45 минут
                - Эффективность: 60%
                - Автоматизация: 30%
                - Уровень ошибок: 3%
                
                Узкие места:
                - Ручная обработка данных (20 мин)
                - Ожидание подтверждений (12 мин)
                - Поиск информации (8 мин)
                - Дублирование действий (5 мин)
                
                Сравнение с индустрией:
                - Время: 45 мин vs 30 мин (среднее)
                - Автоматизация: 30% vs 55% (среднее)
                """
                
                @async_to_sync
                async def generate_recommendations():
                    return await llm_client.analyze_text(
                        process_data,
                        "Проанализируй процесс и предложи конкретные рекомендации по оптимизации. "
                        "Укажи приоритетные области улучшения, потенциальную экономию времени и ресурсов."
                    )
                
                recommendations = generate_recommendations()
                
                st.subheader("💡 Рекомендации по улучшению")
                st.markdown(recommendations)
        
        # Готовые рекомендации
        st.subheader("🎯 Приоритетные улучшения")
        
        improvements = [
            {
                "title": "Автоматизация обработки данных",
                "impact": "Высокий",
                "effort": "Средний", 
                "time_save": "15 мин",
                "cost": "$2,000"
            },
            {
                "title": "Внедрение шаблонов ответов",
                "impact": "Средний",
                "effort": "Низкий",
                "time_save": "8 мин", 
                "cost": "$200"
            },
            {
                "title": "Настройка уведомлений",
                "impact": "Средний",
                "effort": "Низкий",
                "time_save": "5 мин",
                "cost": "$100"
            }
        ]
        
        for improvement in improvements:
            with st.expander(f"💡 {improvement['title']} | Экономия: {improvement['time_save']}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Влияние:** {improvement['impact']}")
                    st.markdown(f"**Сложность:** {improvement['effort']}")
                    st.markdown(f"**Экономия времени:** {improvement['time_save']}")
                    st.markdown(f"**Стоимость внедрения:** {improvement['cost']}")
                
                with col2:
                    if st.button("Запланировать", key=f"plan_{improvement['title']}"):
                        st.success("Улучшение добавлено в план!")
                    
                    if st.button("Подробнее", key=f"details_{improvement['title']}"):
                        st.info("Показать детальный план внедрения")
    
    with tab4:
        st.subheader("🤖 Автоматизация процессов")
        
        # Кандидаты на автоматизацию
        st.subheader("🎯 Кандидаты на автоматизацию")
        
        automation_candidates = [
            {"process": "Отправка напоминаний", "automation_score": 95, "roi": "300%", "implementation": "1 день"},
            {"process": "Создание еженедельных отчетов", "automation_score": 85, "roi": "250%", "implementation": "3 дня"},
            {"process": "Обновление статусов задач", "automation_score": 90, "roi": "200%", "implementation": "2 дня"},
            {"process": "Архивирование документов", "automation_score": 80, "roi": "150%", "implementation": "1 день"}
        ]
        
        for candidate in automation_candidates:
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                st.write(f"🔧 **{candidate['process']}**")
                st.progress(candidate['automation_score'] / 100)
            
            with col2:
                st.write(f"ROI: {candidate['roi']}")
            
            with col3:
                st.write(f"Внедрение: {candidate['implementation']}")
            
            with col4:
                if st.button("Автоматизировать", key=f"automate_{candidate['process']}"):
                    st.success("Запущена автоматизация!")
        
        # Создание автоматизации
        st.subheader("⚙️ Создать автоматизацию")
        
        with st.form("create_automation"):
            col1, col2 = st.columns(2)
            
            with col1:
                automation_name = st.text_input("Название автоматизации:")
                trigger_type = st.selectbox("Триггер:", ["По времени", "По событию", "По условию"])
                action_type = st.selectbox("Действие:", ["Отправить email", "Создать задачу", "Обновить данные"])
            
            with col2:
                frequency = st.selectbox("Частота:", ["Ежедневно", "Еженедельно", "Ежемесячно", "По требованию"])
                notification = st.checkbox("Уведомления о выполнении")
                active = st.checkbox("Активировать сразу", True)
            
            automation_description = st.text_area("Описание процесса:")
            automation_conditions = st.text_area("Условия выполнения:")
            
            if st.form_submit_button("Создать автоматизацию"):
                if automation_name:
                    st.success(f"Автоматизация '{automation_name}' создана!")
        
        # Активные автоматизации
        st.subheader("🔄 Активные автоматизации")
        
        active_automations = [
            {"name": "Ежедневная сводка", "trigger": "09:00", "last_run": "Сегодня", "status": "Активна"},
            {"name": "Напоминания о дедлайнах", "trigger": "За 1 день", "last_run": "Вчера", "status": "Активна"},
            {"name": "Архивирование", "trigger": "Еженедельно", "last_run": "3 дня назад", "status": "Приостановлена"}
        ]
        
        for automation in active_automations:
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                st.write(f"🤖 **{automation['name']}**")
            
            with col2:
                st.write(f"Триггер: {automation['trigger']}")
            
            with col3:
                st.write(f"Выполнение: {automation['last_run']}")
            
            with col4:
                if automation['status'] == 'Активна':
                    st.success("✅ Активна")
                else:
                    st.warning("⏸️ Пауза")
        
        # Статистика автоматизации
        st.subheader("📊 Результаты автоматизации")
        
        automation_stats = {
            "Время экономии в день": "2.5 часа",
            "Всего автоматизаций": "8",
            "Успешность выполнения": "98.5%",
            "Сэкономлено за месяц": "$3,200"
        }
        
        cols = st.columns(len(automation_stats))
        for i, (key, value) in enumerate(automation_stats.items()):
            with cols[i]:
                st.metric(key, value)

if __name__ == "__main__":
    main()