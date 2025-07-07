"""
Утилита для базы контактов и CRM
Управление контактами, клиентами и взаимоотношениями с помощью ИИ.
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
        "База контактов и CRM", 
        "Управление клиентами и контактами с ИИ аналитикой"
    )
    
    # Боковая панель с настройками
    with st.sidebar:
        st.header("⚙️ Настройки")
        
        # Тип контактов
        contact_type = st.selectbox(
            "Тип контактов:",
            ["Все", "Клиенты", "Партнеры", "Поставщики", "Коллеги"],
            index=0
        )
        
        # Статус
        contact_status = st.selectbox(
            "Статус:",
            ["Все", "Активные", "Потенциальные", "Неактивные"],
            index=0
        )
        
        # Регион
        region_filter = st.selectbox(
            "Регион:",
            ["Все", "Москва", "СПб", "Регионы", "Международные"],
            index=0
        )
        
        if st.button("🔄 Обновить данные", type="primary"):
            st.rerun()
    
    # Основное содержимое
    tab1, tab2, tab3, tab4 = st.tabs([
        "👥 Контакты", "💼 Сделки", "📊 Аналитика", "🤖 ИИ Помощник"
    ])
    
    with tab1:
        st.subheader("👥 Управление контактами")
        
        # Статистика
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Всего контактов", "1,247", "45")
        with col2:
            st.metric("Активных клиентов", "356", "12")
        with col3:
            st.metric("Новых за месяц", "28", "8")
        with col4:
            st.metric("Конверсия", "23%", "3%")
        
        # Поиск контактов
        st.subheader("🔍 Поиск контактов")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_query = st.text_input("Поиск по имени, компании или email:")
        
        with col2:
            if st.button("🔍 Найти", use_container_width=True):
                if search_query:
                    st.success(f"Поиск: {search_query}")
        
        # Добавление контакта
        with st.expander("➕ Добавить новый контакт"):
            with st.form("add_contact"):
                col1, col2 = st.columns(2)
                
                with col1:
                    contact_name = st.text_input("Имя:")
                    contact_company = st.text_input("Компания:")
                    contact_position = st.text_input("Должность:")
                    contact_email = st.text_input("Email:")
                
                with col2:
                    contact_phone = st.text_input("Телефон:")
                    contact_type_new = st.selectbox("Тип:", ["Клиент", "Партнер", "Поставщик", "Коллега"])
                    contact_status_new = st.selectbox("Статус:", ["Активный", "Потенциальный", "Неактивный"])
                    contact_region = st.selectbox("Регион:", ["Москва", "СПб", "Регионы", "Международный"])
                
                contact_notes = st.text_area("Заметки:")
                contact_tags = st.text_input("Теги (через запятую):")
                
                if st.form_submit_button("Добавить контакт"):
                    if contact_name and contact_email:
                        st.success(f"Контакт '{contact_name}' добавлен!")
        
        # Список контактов
        st.subheader("📋 Список контактов")
        
        contacts = [
            {
                "name": "Анна Иванова",
                "company": "ООО Ромашка", 
                "position": "Директор",
                "email": "anna@romashka.ru",
                "phone": "+7-495-123-45-67",
                "type": "Клиент",
                "status": "Активный",
                "last_contact": "3 дня назад"
            },
            {
                "name": "Петр Петров",
                "company": "ИП Петров",
                "position": "Предприниматель", 
                "email": "petr@petrov.com",
                "phone": "+7-916-234-56-78",
                "type": "Партнер",
                "status": "Потенциальный",
                "last_contact": "1 неделя назад"
            },
            {
                "name": "Мария Сидорова",
                "company": "TechCorp",
                "position": "Менеджер",
                "email": "maria@techcorp.io",
                "phone": "+7-812-345-67-89",
                "type": "Клиент", 
                "status": "Активный",
                "last_contact": "Вчера"
            }
        ]
        
        for contact in contacts:
            with st.expander(f"👤 {contact['name']} | {contact['company']}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Компания:** {contact['company']}")
                    st.markdown(f"**Должность:** {contact['position']}")
                    st.markdown(f"**Email:** {contact['email']}")
                    st.markdown(f"**Телефон:** {contact['phone']}")
                    st.markdown(f"**Последний контакт:** {contact['last_contact']}")
                
                with col2:
                    st.markdown(f"**Тип:** {contact['type']}")
                    
                    if contact['status'] == 'Активный':
                        st.success("✅ Активный")
                    elif contact['status'] == 'Потенциальный':
                        st.warning("⏳ Потенциальный")
                    else:
                        st.error("❌ Неактивный")
                    
                    if st.button("Связаться", key=f"contact_{contact['name']}"):
                        st.info("Создан напоминание о звонке")
                    
                    if st.button("Редактировать", key=f"edit_{contact['name']}"):
                        st.info("Режим редактирования")
    
    with tab2:
        st.subheader("💼 Управление сделками")
        
        # Воронка продаж
        st.subheader("🏆 Воронка продаж")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Лиды", "45", "8")
        with col2:
            st.metric("Квалифицированные", "23", "3")
        with col3:
            st.metric("Переговоры", "12", "1")
        with col4:
            st.metric("Закрытые", "8", "2")
        
        # График воронки
        import pandas as pd
        import plotly.express as px
        
        funnel_data = pd.DataFrame({
            'Этап': ['Лиды', 'Квалифицированные', 'Переговоры', 'Закрытые'],
            'Количество': [45, 23, 12, 8],
            'Конверсия': [100, 51, 27, 18]
        })
        
        fig = px.funnel(funnel_data, x='Количество', y='Этап',
                       title="Воронка продаж")
        st.plotly_chart(fig, use_container_width=True)
        
        # Активные сделки
        st.subheader("📋 Активные сделки")
        
        deals = [
            {
                "title": "Внедрение CRM системы",
                "client": "ООО Ромашка",
                "amount": "$15,000",
                "stage": "Переговоры",
                "probability": 70,
                "close_date": "2024-02-28"
            },
            {
                "title": "Консалтинговые услуги",
                "client": "TechCorp",
                "amount": "$8,500",
                "stage": "Квалификация",
                "probability": 40,
                "close_date": "2024-03-15"
            }
        ]
        
        for deal in deals:
            with st.expander(f"💼 {deal['title']} | {deal['amount']}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Клиент:** {deal['client']}")
                    st.markdown(f"**Сумма:** {deal['amount']}")
                    st.markdown(f"**Этап:** {deal['stage']}")
                    st.markdown(f"**Дата закрытия:** {deal['close_date']}")
                    
                    st.markdown("**Вероятность закрытия:**")
                    st.progress(deal['probability'] / 100)
                
                with col2:
                    if deal['probability'] > 60:
                        st.success("🟢 Высокая")
                    elif deal['probability'] > 30:
                        st.warning("🟡 Средняя")
                    else:
                        st.error("🔴 Низкая")
                    
                    if st.button("Обновить", key=f"update_{deal['title']}"):
                        st.success("Сделка обновлена!")
        
        # Создание сделки
        with st.expander("➕ Создать новую сделку"):
            with st.form("new_deal"):
                col1, col2 = st.columns(2)
                
                with col1:
                    deal_title = st.text_input("Название сделки:")
                    deal_client = st.selectbox("Клиент:", ["ООО Ромашка", "TechCorp", "ИП Петров"])
                    deal_amount = st.number_input("Сумма ($):", min_value=0.0, value=5000.0)
                
                with col2:
                    deal_stage = st.selectbox("Этап:", ["Лид", "Квалификация", "Переговоры", "Предложение"])
                    deal_probability = st.slider("Вероятность (%):", 0, 100, 50)
                    deal_close_date = st.date_input("Планируемая дата закрытия:")
                
                deal_description = st.text_area("Описание сделки:")
                
                if st.form_submit_button("Создать сделку"):
                    if deal_title and deal_client:
                        st.success(f"Сделка '{deal_title}' создана!")
    
    with tab3:
        st.subheader("📊 Аналитика CRM")
        
        # Ключевые показатели
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Выручка за месяц", "$45,300", "$8,200")
        with col2:
            st.metric("Средний чек", "$2,850", "$150")
        with col3:
            st.metric("LTV клиента", "$12,500", "$1,200")
        with col4:
            st.metric("Churn Rate", "5.2%", "-1.1%")
        
        # График продаж
        st.subheader("📈 Динамика продаж")
        
        months = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн']
        sales_data = pd.DataFrame({
            'Месяц': months,
            'Выручка': [35000, 42000, 38000, 45000, 52000, 48000],
            'Количество сделок': [18, 21, 19, 23, 26, 24]
        })
        
        fig = px.line(sales_data, x='Месяц', y=['Выручка'],
                     title="Выручка по месяцам")
        st.plotly_chart(fig, use_container_width=True)
        
        # Анализ клиентов
        st.subheader("👥 Сегментация клиентов")
        
        segments = pd.DataFrame({
            'Сегмент': ['Крупные клиенты', 'Средний бизнес', 'Малый бизнес', 'Стартапы'],
            'Количество': [15, 45, 120, 85],
            'Выручка': [25000, 15000, 8000, 3000]
        })
        
        fig_segments = px.bar(segments, x='Сегмент', y=['Количество', 'Выручка'],
                             title="Клиенты по сегментам", barmode='group')
        st.plotly_chart(fig_segments, use_container_width=True)
        
        # Топ клиенты
        st.subheader("🏆 Топ клиенты")
        
        top_clients = [
            {"name": "ООО Ромашка", "revenue": "$25,000", "deals": 8, "growth": "+15%"},
            {"name": "TechCorp", "revenue": "$18,500", "deals": 5, "growth": "+22%"},
            {"name": "StartupXYZ", "revenue": "$12,300", "deals": 12, "growth": "-5%"}
        ]
        
        for client in top_clients:
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                st.write(f"🏢 **{client['name']}**")
            with col2:
                st.write(f"💰 {client['revenue']}")
            with col3:
                st.write(f"📊 {client['deals']} сделок")
            with col4:
                growth = client['growth']
                if '+' in growth:
                    st.success(f"📈 {growth}")
                else:
                    st.error(f"📉 {growth}")
    
    with tab4:
        st.subheader("🤖 ИИ Помощник CRM")
        
        # Анализ клиентской базы
        if st.button("📊 Анализ клиентской базы", type="primary"):
            with st.spinner("Анализ данных CRM..."):
                
                crm_data = """
                Данные CRM за последний месяц:
                
                Клиентская база:
                - Всего контактов: 1,247
                - Активных клиентов: 356
                - Новых клиентов: 28
                - Churn rate: 5.2%
                
                Продажи:
                - Выручка: $45,300
                - Средний чек: $2,850
                - Количество сделок: 24
                - Конверсия: 23%
                
                Воронка продаж:
                - Лиды: 45
                - Квалифицированные: 23 (51%)
                - Переговоры: 12 (27%)
                - Закрытые: 8 (18%)
                
                Топ сегменты:
                - Крупные клиенты: 15 (высокая маржа)
                - Средний бизнес: 45 (стабильный рост)
                - Малый бизнес: 120 (большой объем)
                """
                
                @async_to_sync
                async def analyze_crm():
                    return await llm_client.analyze_text(
                        crm_data,
                        "Проанализируй данные CRM. Выдели ключевые тренды, "
                        "проблемы в воронке продаж, возможности роста и рекомендации."
                    )
                
                analysis = analyze_crm()
                
                st.subheader("📝 Анализ CRM")
                st.markdown(analysis)
        
        # Рекомендации по клиентам
        st.subheader("💡 Умные рекомендации")
        
        recommendations = [
            {
                "type": "Риск оттока",
                "client": "StartupXYZ",
                "action": "Связаться в течение 3 дней",
                "reason": "Снижение активности на 30%"
            },
            {
                "type": "Возможность допродажи",
                "client": "ООО Ромашка", 
                "action": "Предложить дополнительные услуги",
                "reason": "Высокая удовлетворенность (9/10)"
            },
            {
                "type": "Горячий лид",
                "client": "NewTech Ltd",
                "action": "Запланировать встречу",
                "reason": "Активное взаимодействие с сайтом"
            }
        ]
        
        for rec in recommendations:
            with st.expander(f"💡 {rec['type']}: {rec['client']}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Рекомендация:** {rec['action']}")
                    st.markdown(f"**Причина:** {rec['reason']}")
                
                with col2:
                    if rec['type'] == 'Риск оттока':
                        st.error("🚨 Высокий риск")
                    elif rec['type'] == 'Возможность допродажи':
                        st.success("💰 Возможность")
                    else:
                        st.info("🔥 Горячий лид")
                    
                    if st.button("Выполнить", key=f"action_{rec['client']}"):
                        st.success("Действие запланировано!")
        
        # Прогнозирование
        st.subheader("🔮 Прогнозы")
        
        if st.button("📈 Создать прогноз продаж"):
            st.info("Генерация прогноза на основе исторических данных...")
            
            forecast_data = {
                "Следующий месяц": "$52,000",
                "Квартал": "$165,000",
                "Год": "$720,000"
            }
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Следующий месяц", forecast_data["Следующий месяц"], "+14%")
            with col2:
                st.metric("Квартал", forecast_data["Квартал"], "+18%")
            with col3:
                st.metric("Год", forecast_data["Год"], "+22%")

if __name__ == "__main__":
    main()