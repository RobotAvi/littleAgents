"""
Утилита для организации командировок и поездок
Планирование поездок, бронирование билетов и отелей, управление расходами.
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
        "Организация поездок", 
        "Планирование командировок и управление travel-расходами"
    )
    
    # Боковая панель с настройками
    with st.sidebar:
        st.header("⚙️ Настройки")
        
        # Тип поездки
        trip_type = st.selectbox(
            "Тип поездки:",
            ["Командировка", "Конференция", "Встреча с клиентом", "Обучение"],
            index=0
        )
        
        # Бюджет
        budget_limit = st.number_input("Лимит бюджета (USD):", min_value=0, value=2000)
        
        # Предпочтения
        preferences = st.multiselect(
            "Предпочтения:",
            ["Эконом класс", "Близко к центру", "Wi-Fi в отеле", "Завтрак включен"],
            default=["Эконом класс", "Wi-Fi в отеле"]
        )
        
        if st.button("🔄 Обновить", type="primary"):
            st.rerun()
    
    # Основное содержимое
    tab1, tab2, tab3, tab4 = st.tabs([
        "🗓️ Планирование", "✈️ Бронирование", "💰 Расходы", "📋 Отчеты"
    ])
    
    with tab1:
        st.subheader("🗓️ Планирование поездки")
        
        # Форма создания поездки
        with st.form("trip_planning"):
            st.subheader("➕ Новая поездка")
            
            col1, col2 = st.columns(2)
            
            with col1:
                trip_title = st.text_input("Название поездки:")
                destination = st.text_input("Место назначения:")
                departure_date = st.date_input("Дата отправления:")
                departure_time = st.time_input("Время отправления:")
                
            with col2:
                trip_purpose = st.text_area("Цель поездки:")
                return_date = st.date_input("Дата возвращения:")
                return_time = st.time_input("Время возвращения:")
                participants = st.text_input("Участники (через запятую):")
            
            # Дополнительные требования
            st.subheader("Требования к поездке")
            
            col1, col2 = st.columns(2)
            
            with col1:
                need_visa = st.checkbox("Требуется виза")
                need_insurance = st.checkbox("Требуется страховка")
                
            with col2:
                need_transfer = st.checkbox("Нужен трансфер")
                need_interpreter = st.checkbox("Нужен переводчик")
            
            if st.form_submit_button("Создать план поездки"):
                if trip_title and destination:
                    st.success(f"План поездки '{trip_title}' создан!")
        
        # Список запланированных поездок
        st.subheader("📅 Запланированные поездки")
        
        planned_trips = [
            {
                "title": "Конференция DevOps",
                "destination": "Москва",
                "dates": "15-17 Jan 2024",
                "status": "Подтверждена",
                "budget": "$1,500"
            },
            {
                "title": "Встреча с клиентом",
                "destination": "СПб",
                "dates": "25 Jan 2024",
                "status": "Планирование",
                "budget": "$800"
            }
        ]
        
        for trip in planned_trips:
            with st.expander(f"✈️ {trip['title']} - {trip['destination']}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Направление:** {trip['destination']}")
                    st.markdown(f"**Даты:** {trip['dates']}")
                    st.markdown(f"**Статус:** {trip['status']}")
                    st.markdown(f"**Бюджет:** {trip['budget']}")
                
                with col2:
                    if st.button(f"Редактировать", key=f"edit_{trip['title']}"):
                        st.info("Редактирование поездки...")
                    if st.button(f"Отменить", key=f"cancel_{trip['title']}"):
                        st.warning("Поездка отменена")
    
    with tab2:
        st.subheader("✈️ Бронирование и билеты")
        
        # Поиск авиабилетов
        st.subheader("🛫 Поиск авиабилетов")
        
        with st.form("flight_search"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                from_city = st.text_input("Откуда:", value="Москва")
                departure_date_flight = st.date_input("Дата отправления:", datetime.now().date())
                
            with col2:
                to_city = st.text_input("Куда:", value="Санкт-Петербург")
                return_date_flight = st.date_input("Дата возвращения:")
                
            with col3:
                passengers = st.number_input("Пассажиров:", min_value=1, value=1)
                class_type = st.selectbox("Класс:", ["Эконом", "Бизнес", "Первый"])
            
            if st.form_submit_button("🔍 Найти билеты"):
                st.success("Поиск билетов...")
                
                # Симуляция результатов поиска
                flight_options = [
                    {"airline": "Аэрофлот", "time": "08:30-10:15", "price": "$150", "duration": "1ч 45м"},
                    {"airline": "S7", "time": "14:20-16:05", "price": "$135", "duration": "1ч 45м"},
                    {"airline": "Победа", "time": "19:10-20:55", "price": "$89", "duration": "1ч 45м"}
                ]
                
                st.subheader("✈️ Найденные рейсы")
                
                for i, flight in enumerate(flight_options):
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                    
                    with col1:
                        st.write(f"**{flight['airline']}**")
                        st.write(f"{flight['time']}")
                    with col2:
                        st.write(flight['duration'])
                    with col3:
                        st.write(f"**{flight['price']}**")
                    with col4:
                        if st.button("Выбрать", key=f"select_flight_{i}"):
                            st.success(f"Рейс {flight['airline']} выбран!")
        
        # Поиск отелей
        st.subheader("🏨 Поиск отелей")
        
        with st.form("hotel_search"):
            col1, col2 = st.columns(2)
            
            with col1:
                hotel_city = st.text_input("Город:", value="Санкт-Петербург")
                checkin_date = st.date_input("Заезд:")
                
            with col2:
                checkout_date = st.date_input("Выезд:")
                hotel_guests = st.number_input("Гостей:", min_value=1, value=1)
            
            hotel_rating = st.selectbox("Рейтинг отеля:", ["Любой", "3 звезды+", "4 звезды+", "5 звезд"])
            
            if st.form_submit_button("🔍 Найти отели"):
                st.success("Поиск отелей...")
                
                # Симуляция результатов
                hotel_options = [
                    {"name": "Гранд Отель Европа", "rating": "⭐⭐⭐⭐⭐", "price": "$200/ночь", "location": "Центр"},
                    {"name": "Radisson Blu", "rating": "⭐⭐⭐⭐", "price": "$120/ночь", "location": "Невский проспект"},
                    {"name": "Ibis Budget", "rating": "⭐⭐⭐", "price": "$60/ночь", "location": "Московский район"}
                ]
                
                st.subheader("🏨 Найденные отели")
                
                for i, hotel in enumerate(hotel_options):
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                    
                    with col1:
                        st.write(f"**{hotel['name']}**")
                        st.write(hotel['rating'])
                    with col2:
                        st.write(hotel['location'])
                    with col3:
                        st.write(f"**{hotel['price']}**")
                    with col4:
                        if st.button("Выбрать", key=f"select_hotel_{i}"):
                            st.success(f"Отель {hotel['name']} выбран!")
    
    with tab3:
        st.subheader("💰 Управление расходами")
        
        # Бюджет поездки
        st.subheader("💳 Бюджет поездки")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Общий бюджет", "$2,000", "")
        with col2:
            st.metric("Потрачено", "$856", "+$156")
        with col3:
            st.metric("Остаток", "$1,144", "-$156")
        with col4:
            st.metric("% использования", "43%", "+8%")
        
        # Добавление расхода
        st.subheader("➕ Добавить расход")
        
        with st.form("add_expense"):
            col1, col2 = st.columns(2)
            
            with col1:
                expense_category = st.selectbox("Категория:", ["Авиабилеты", "Отель", "Питание", "Транспорт", "Прочее"])
                expense_amount = st.number_input("Сумма (USD):", min_value=0.0, value=0.0)
                
            with col2:
                expense_date = st.date_input("Дата расхода:")
                expense_description = st.text_input("Описание:")
            
            receipt_upload = st.file_uploader("Загрузить чек:", type=['jpg', 'png', 'pdf'])
            
            if st.form_submit_button("Добавить расход"):
                if expense_amount > 0:
                    st.success(f"Расход ${expense_amount} добавлен!")
        
        # История расходов
        st.subheader("📊 История расходов")
        
        expenses = [
            {"date": "2024-01-10", "category": "Авиабилеты", "amount": "$300", "description": "Рейс MOW-LED"},
            {"date": "2024-01-10", "category": "Отель", "amount": "$240", "description": "2 ночи в отеле"},
            {"date": "2024-01-11", "category": "Питание", "amount": "$45", "description": "Обед в ресторане"},
            {"date": "2024-01-11", "category": "Транспорт", "amount": "$25", "description": "Такси из аэропорта"}
        ]
        
        for expense in expenses:
            col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
            
            with col1:
                st.write(expense['date'])
            with col2:
                st.write(expense['category'])
            with col3:
                st.write(f"**{expense['amount']}**")
            with col4:
                st.write(expense['description'])
    
    with tab4:
        st.subheader("📋 Отчеты и документы")
        
        # Генерация отчета
        if st.button("📊 Сгенерировать отчет о поездке", type="primary"):
            with st.spinner("Создание отчета..."):
                
                trip_data = f"""
                Отчет о командировке:
                
                Цель: {trip_type}
                Направление: Санкт-Петербург
                Даты: 10-12 января 2024
                Бюджет: $2,000
                Потрачено: $610
                
                Основные расходы:
                - Авиабилеты: $300
                - Отель: $240  
                - Питание: $45
                - Транспорт: $25
                """
                
                @async_to_sync
                async def generate_trip_report():
                    return await llm_client.analyze_text(
                        trip_data,
                        "Создай подробный отчет о командировке. "
                        "Включи анализ расходов, достигнутые цели, рекомендации."
                    )
                
                report = generate_trip_report()
                
                st.subheader("📄 Отчет о поездке")
                st.markdown(report)
        
        # Документы
        st.subheader("📄 Документы поездки")
        
        documents = [
            {"name": "Авиабилеты", "status": "✅", "file": "tickets.pdf"},
            {"name": "Бронь отеля", "status": "✅", "file": "hotel_booking.pdf"},
            {"name": "Страховка", "status": "⏳", "file": "insurance.pdf"},
            {"name": "Отчет о расходах", "status": "📝", "file": "expenses.xlsx"}
        ]
        
        for doc in documents:
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"📄 **{doc['name']}**")
            with col2:
                st.write(doc['status'])
            with col3:
                if st.button("📥", key=f"download_{doc['name']}"):
                    st.info(f"Скачивание {doc['file']}")

if __name__ == "__main__":
    main()