"""
Утилита для финансов и администрирования
Управление расходами, бюджетирование и финансовые отчеты.
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
        "Финансы и администрирование", 
        "Управление расходами и финансовая отчетность"
    )
    
    # Боковая панель с настройками
    with st.sidebar:
        st.header("⚙️ Настройки")
        
        # Период отчета
        report_period = st.selectbox(
            "Период отчета:",
            ["Текущий месяц", "Квартал", "Полугодие", "Год"],
            index=0
        )
        
        # Валюта
        currency = st.selectbox(
            "Валюта:",
            ["USD", "RUB", "EUR"],
            index=0
        )
        
        # Категория расходов
        expense_categories = st.multiselect(
            "Категории расходов:",
            ["Зарплаты", "Аренда", "ИТ", "Маркетинг", "Командировки", "Обучение"],
            default=["Зарплаты", "Аренда", "ИТ"]
        )
        
        if st.button("🔄 Обновить данные", type="primary"):
            st.rerun()
    
    # Основное содержимое
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Дашборд", "💰 Расходы", "📈 Бюджет", "📋 Отчеты"
    ])
    
    with tab1:
        st.subheader("📊 Финансовый обзор")
        
        # Ключевые метрики
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Общий бюджет", f"$120,000", "")
        with col2:
            st.metric("Потрачено", f"$85,500", "+$5,200")
        with col3:
            st.metric("Остаток", f"$34,500", "-$5,200")
        with col4:
            st.metric("% исполнения", "71%", "+4%")
        
        # График расходов
        st.subheader("📈 Динамика расходов")
        
        import pandas as pd
        import plotly.express as px
        
        # Симуляция данных расходов
        months = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн']
        expenses_data = pd.DataFrame({
            'Месяц': months,
            'Зарплаты': [45000, 47000, 46000, 48000, 49000, 47500],
            'Аренда': [12000, 12000, 12000, 12000, 12000, 12000],
            'ИТ': [8000, 9500, 7500, 8200, 9000, 8800],
            'Маркетинг': [5000, 6000, 4500, 7000, 6500, 5500]
        })
        
        fig = px.line(expenses_data, x='Месяц', y=['Зарплаты', 'Аренда', 'ИТ', 'Маркетинг'],
                     title="Расходы по категориям")
        st.plotly_chart(fig, use_container_width=True)
        
        # Распределение бюджета
        st.subheader("🥧 Распределение бюджета")
        
        budget_distribution = pd.DataFrame({
            'Категория': ['Зарплаты', 'Аренда', 'ИТ', 'Маркетинг', 'Командировки', 'Прочее'],
            'Сумма': [47500, 12000, 8800, 5500, 4200, 7000]
        })
        
        fig_pie = px.pie(budget_distribution, values='Сумма', names='Категория',
                        title="Структура расходов")
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with tab2:
        st.subheader("💰 Управление расходами")
        
        # Добавление нового расхода
        with st.expander("➕ Добавить расход"):
            with st.form("add_expense"):
                col1, col2 = st.columns(2)
                
                with col1:
                    expense_category = st.selectbox("Категория:", ["Зарплаты", "Аренда", "ИТ", "Маркетинг", "Командировки", "Обучение", "Прочее"])
                    expense_amount = st.number_input(f"Сумма ({currency}):", min_value=0.0, value=0.0)
                    expense_date = st.date_input("Дата расхода:")
                
                with col2:
                    expense_description = st.text_area("Описание:")
                    expense_project = st.text_input("Проект (опционально):")
                    expense_approved = st.checkbox("Подтверждено")
                
                receipt_file = st.file_uploader("Документ/чек:", type=['pdf', 'jpg', 'png', 'xlsx'])
                
                if st.form_submit_button("Добавить расход"):
                    if expense_amount > 0:
                        st.success(f"Расход {expense_amount} {currency} добавлен!")
        
        # Последние расходы
        st.subheader("📊 Последние расходы")
        
        recent_expenses = [
            {"date": "2024-01-15", "category": "ИТ", "amount": 2500, "description": "Лицензии ПО", "status": "Одобрено"},
            {"date": "2024-01-14", "category": "Маркетинг", "amount": 1200, "description": "Реклама в соцсетях", "status": "Ожидает"},
            {"date": "2024-01-13", "category": "Командировки", "amount": 800, "description": "Поездка в СПб", "status": "Одобрено"},
            {"date": "2024-01-12", "category": "Обучение", "amount": 500, "description": "Курс по DevOps", "status": "Одобрено"}
        ]
        
        for expense in recent_expenses:
            col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 2, 1])
            
            with col1:
                st.write(expense['date'])
            with col2:
                st.write(expense['category'])
            with col3:
                st.write(f"${expense['amount']}")
            with col4:
                st.write(expense['description'])
            with col5:
                if expense['status'] == 'Одобрено':
                    st.success("✅")
                else:
                    st.warning("⏳")
        
        # Фильтры и поиск
        st.subheader("🔍 Поиск расходов")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_category = st.selectbox("Категория:", ["Все"] + ["Зарплаты", "Аренда", "ИТ", "Маркетинг"])
        with col2:
            search_period = st.selectbox("Период:", ["Все", "Этот месяц", "Прошлый месяц", "Квартал"])
        with col3:
            search_status = st.selectbox("Статус:", ["Все", "Одобрено", "Ожидает", "Отклонено"])
        
        if st.button("🔍 Найти"):
            st.info("Поиск расходов по заданным критериям...")
    
    with tab3:
        st.subheader("📈 Бюджетирование")
        
        # Планирование бюджета
        st.subheader("📋 План бюджета на год")
        
        budget_plan = [
            {"category": "Зарплаты", "planned": 570000, "actual": 285000, "remaining": 285000},
            {"category": "Аренда", "planned": 144000, "actual": 72000, "remaining": 72000},
            {"category": "ИТ", "planned": 100000, "actual": 52800, "remaining": 47200},
            {"category": "Маркетинг", "planned": 72000, "actual": 34000, "remaining": 38000}
        ]
        
        for budget in budget_plan:
            with st.expander(f"💼 {budget['category']} - ${budget['planned']:,}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Запланировано", f"${budget['planned']:,}")
                with col2:
                    st.metric("Потрачено", f"${budget['actual']:,}")
                with col3:
                    st.metric("Остаток", f"${budget['remaining']:,}")
                
                # Прогресс бар
                progress = budget['actual'] / budget['planned']
                st.progress(progress)
                st.write(f"Исполнение: {progress:.1%}")
                
                if progress > 0.8:
                    st.warning("⚠️ Близко к лимиту бюджета!")
        
        # Прогнозирование расходов
        st.subheader("🔮 Прогноз расходов")
        
        if st.button("📊 Сгенерировать прогноз"):
            st.info("Анализ трендов и создание прогноза...")
            
            # Симуляция прогноза
            forecast_data = {
                "Следующий месяц": "$28,500",
                "До конца квартала": "$85,200", 
                "До конца года": "$156,000"
            }
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Следующий месяц", forecast_data["Следующий месяц"])
            with col2:
                st.metric("До конца квартала", forecast_data["До конца квартала"])
            with col3:
                st.metric("До конца года", forecast_data["До конца года"])
    
    with tab4:
        st.subheader("📋 Финансовые отчеты")
        
        # Генерация отчета с ИИ
        if st.button("🤖 Сгенерировать финансовый анализ", type="primary"):
            with st.spinner("Анализ финансовых данных..."):
                
                financial_data = f"""
                Финансовые показатели за {report_period}:
                
                Общий бюджет: $120,000
                Потрачено: $85,500 (71%)
                Остаток: $34,500
                
                Расходы по категориям:
                - Зарплаты: $47,500 (56%)
                - Аренда: $12,000 (14%)
                - ИТ: $8,800 (10%)
                - Маркетинг: $5,500 (6%)
                - Командировки: $4,200 (5%)
                - Прочее: $7,000 (8%)
                
                Тренды:
                - Рост расходов на ИТ на 15%
                - Сокращение маркетингового бюджета на 8%
                - Стабильные расходы на аренду
                """
                
                @async_to_sync
                async def analyze_finances():
                    return await llm_client.analyze_text(
                        financial_data,
                        "Проанализируй финансовое состояние компании. "
                        "Выдели основные тренды, риски и рекомендации по оптимизации бюджета."
                    )
                
                analysis = analyze_finances()
                
                st.subheader("📝 Финансовый анализ")
                st.markdown(analysis)
        
        # Типы отчетов
        st.subheader("📊 Стандартные отчеты")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📈 P&L отчет"):
                st.success("Отчет о прибылях и убытках сгенерирован!")
            
            if st.button("💰 Cash Flow"):
                st.success("Отчет о движении денежных средств сгенерирован!")
        
        with col2:
            if st.button("📊 Бюджет vs Факт"):
                st.success("Сравнительный анализ бюджета готов!")
            
            if st.button("🏢 Расходы по проектам"):
                st.success("Отчет по проектам сгенерирован!")
        
        with col3:
            if st.button("📋 Налоговый отчет"):
                st.success("Налоговая отчетность подготовлена!")
            
            if st.button("📧 Отправить CFO"):
                st.success("Отчеты отправлены CFO!")
        
        # Экспорт данных
        st.subheader("📤 Экспорт данных")
        
        export_format = st.selectbox("Формат экспорта:", ["Excel", "PDF", "CSV"])
        export_period = st.selectbox("Период данных:", ["Текущий месяц", "Квартал", "Год"])
        
        if st.button("📥 Экспортировать"):
            st.success(f"Данные экспортированы в формате {export_format}!")

if __name__ == "__main__":
    main()