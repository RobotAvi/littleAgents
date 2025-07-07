"""
Утилита для управления календарем и встречами
Проверка календаря, формирование сводной, отправка в Телеграм
"""

import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from shared.llm_client import llm_client
from shared.config import Config
from shared.utils import (
    create_streamlit_header, display_metrics, 
    display_data_table, send_notification, 
    validate_config, async_to_sync
)
from datetime import datetime, timedelta
import json

def main():
    create_streamlit_header(
        "Календарь и встречи", 
        "Анализ календаря и автоматическая подготовка к встречам"
    )
    
    # Конфигурация
    config = Config.get_utility_config('calendar_manager')
    required_keys = ['openai_api_key']
    
    if not validate_config(config, required_keys):
        st.stop()
    
    # Боковая панель с настройками
    with st.sidebar:
        st.header("⚙️ Настройки")
        
        # Период анализа
        period = st.selectbox(
            "Период анализа:",
            ["Сегодня", "Завтра", "Эта неделя", "Следующая неделя", "Этот месяц"],
            index=0
        )
        
        # Тип событий
        event_type = st.multiselect(
            "Типы событий:",
            ["Встречи", "Созвоны", "Презентации", "Интервью", "Личные"],
            default=["Встречи", "Созвоны"]
        )
        
        # Календари
        calendars = st.multiselect(
            "Календари:",
            ["Рабочий", "Личный", "Проекты", "Командный"],
            default=["Рабочий"]
        )
        
        # Автообновление
        auto_refresh = st.checkbox("Автообновление каждые 10 мин", False)
        
        if st.button("🔄 Обновить данные", type="primary"):
            st.rerun()
    
    # Основное содержимое
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Обзор", "📅 События", "🤖 ИИ Анализ", "📋 Подготовка"
    ])
    
    with tab1:
        st.subheader("📊 Обзор календаря")
        
        # Получение событий (демо данные)
        with st.spinner("Загрузка событий календаря..."):
            events = get_demo_events(period)
            
            if events:
                # Фильтрация по типам
                filtered_events = [e for e in events if e.get('type', 'Встречи') in event_type]
                
                # Метрики
                total_events = len(filtered_events)
                today_events = len([e for e in filtered_events if is_today(e.get('start_time'))])
                upcoming_events = len([e for e in filtered_events if is_upcoming(e.get('start_time'))])
                
                metrics = {
                    "Всего событий": total_events,
                    "Сегодня": today_events,
                    "Предстоящих": upcoming_events,
                    "Свободное время": calculate_free_time(filtered_events)
                }
                
                display_metrics(metrics)
                
                # График загруженности
                st.subheader("📈 Загруженность по дням")
                
                import pandas as pd
                import plotly.express as px
                
                # Подготовка данных для графика
                daily_stats = {}
                for event in filtered_events:
                    if event.get('start_time'):
                        try:
                            event_date = datetime.fromisoformat(event['start_time']).date()
                            date_str = event_date.strftime('%Y-%m-%d')
                            
                            if date_str not in daily_stats:
                                daily_stats[date_str] = {
                                    'date': date_str,
                                    'events': 0,
                                    'hours': 0
                                }
                            
                            daily_stats[date_str]['events'] += 1
                            daily_stats[date_str]['hours'] += event.get('duration', 1)
                        except:
                            continue
                
                if daily_stats:
                    df = pd.DataFrame(list(daily_stats.values()))
                    
                    fig = px.bar(
                        df, 
                        x='date', 
                        y='events',
                        title="Количество событий по дням",
                        labels={'date': 'Дата', 'events': 'Количество событий'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # График по часам
                    fig2 = px.bar(
                        df, 
                        x='date', 
                        y='hours',
                        title="Загруженность по часам",
                        labels={'date': 'Дата', 'hours': 'Часы'}
                    )
                    st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("События не найдены за выбранный период")
    
    with tab2:
        st.subheader("📅 Список событий")
        
        if 'events' in locals() and events:
            # Сортировка событий по времени
            sorted_events = sorted(events, key=lambda x: x.get('start_time', ''))
            
            for i, event in enumerate(sorted_events):
                with st.expander(
                    f"📅 {event.get('title', 'Без названия')} | "
                    f"{format_event_time(event)} | "
                    f"👥 {len(event.get('participants', []))} участников"
                ):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Название:** {event.get('title', 'Без названия')}")
                        st.markdown(f"**Время:** {format_event_time(event)}")
                        st.markdown(f"**Длительность:** {event.get('duration', 1)} час(а)")
                        
                        # Участники
                        participants = event.get('participants', [])
                        if participants:
                            st.markdown(f"**Участники:** {', '.join(participants)}")
                        
                        # Описание
                        description = event.get('description', 'Нет описания')
                        st.markdown(f"**Описание:** {description}")
                        
                        # Место проведения
                        location = event.get('location', 'Не указано')
                        st.markdown(f"**Место:** {location}")
                    
                    with col2:
                        # Тип события
                        event_type_badge = get_event_type_badge(event.get('type', 'Встречи'))
                        st.markdown(f"**Тип:** {event_type_badge}", unsafe_allow_html=True)
                        
                        # Приоритет
                        priority = event.get('priority', 'medium')
                        priority_icon = "🔴" if priority == 'high' else "🟡" if priority == 'medium' else "🟢"
                        st.markdown(f"**Приоритет:** {priority_icon} {priority.title()}")
                        
                        # Статус подготовки
                        prepared = event.get('prepared', False)
                        prep_status = "✅ Готово" if prepared else "⏳ Требует подготовки"
                        st.markdown(f"**Подготовка:** {prep_status}")
                        
                        # Действия
                        if st.button(f"📋 Подготовить #{i}", key=f"prep_{i}"):
                            st.success("Подготовка запущена!")
                            
                        if st.button(f"📝 Заметки #{i}", key=f"notes_{i}"):
                            st.info("Открыть заметки к встрече")
        else:
            st.info("Нет событий для отображения")
    
    with tab3:
        st.subheader("🤖 ИИ Анализ календаря")
        
        if 'events' in locals() and events:
            if st.button("🔍 Запустить анализ календаря", type="primary"):
                with st.spinner("Анализ календаря с помощью ИИ..."):
                    
                    @async_to_sync
                    async def analyze_calendar():
                        return await llm_client.analyze_calendar_events(events)
                    
                    analysis = analyze_calendar()
                    
                    st.subheader("📝 Результат анализа")
                    st.markdown(analysis)
                    
                    # Дополнительные рекомендации
                    st.subheader("💡 Рекомендации")
                    
                    recommendations = generate_recommendations(events)
                    for rec in recommendations:
                        st.info(rec)
                    
                    # Сохранение результата
                    if st.button("💾 Сохранить анализ"):
                        from shared.utils import save_json_data
                        
                        analysis_data = {
                            'timestamp': datetime.now().isoformat(),
                            'period': period,
                            'total_events': len(events),
                            'analysis': analysis,
                            'recommendations': recommendations
                        }
                        
                        save_json_data(analysis_data, f"calendar_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
                        st.success("Анализ сохранен!")
        else:
            st.info("Сначала загрузите события календаря")
    
    with tab4:
        st.subheader("📋 Подготовка к встречам")
        
        st.markdown("""
        **Автоматическая подготовка к встречам:**
        
        1. 📅 Анализ предстоящих событий
        2. 📚 Сбор необходимых материалов
        3. 📝 Создание повестки дня
        4. 👥 Уведомление участников
        """)
        
        # Список встреч, требующих подготовки
        if 'events' in locals() and events:
            unprepared_events = [e for e in events if not e.get('prepared', False)]
            
            if unprepared_events:
                st.subheader("⏳ Требуют подготовки")
                
                for i, event in enumerate(unprepared_events):
                    with st.container():
                        col1, col2, col3 = st.columns([3, 1, 1])
                        
                        with col1:
                            st.markdown(f"**{event.get('title', 'Без названия')}**")
                            st.caption(f"{format_event_time(event)} | {len(event.get('participants', []))} участников")
                        
                        with col2:
                            if st.button(f"📋 Подготовить", key=f"prepare_{i}"):
                                prepare_meeting(event)
                        
                        with col3:
                            if st.button(f"📝 Повестка", key=f"agenda_{i}"):
                                create_agenda(event)
                        
                        st.divider()
            else:
                st.success("Все встречи подготовлены!")
        
        # Форма создания события
        with st.form("new_event"):
            st.subheader("➕ Создать новое событие")
            
            event_title = st.text_input("Название события:")
            event_date = st.date_input("Дата:")
            event_time = st.time_input("Время:")
            event_duration = st.slider("Длительность (часы):", 0.5, 8.0, 1.0, 0.5)
            event_participants = st.text_area("Участники (по одному на строку):")
            event_description = st.text_area("Описание:")
            
            if st.form_submit_button("Создать событие"):
                if event_title:
                    new_event = {
                        'title': event_title,
                        'start_time': datetime.combine(event_date, event_time).isoformat(),
                        'duration': event_duration,
                        'participants': event_participants.split('\n') if event_participants else [],
                        'description': event_description
                    }
                    st.success(f"Событие '{event_title}' создано!")
                else:
                    st.error("Введите название события")

def get_demo_events(period):
    """Получение демо событий календаря"""
    base_time = datetime.now()
    
    if period == "Сегодня":
        start_date = base_time.date()
        end_date = start_date
    elif period == "Завтра":
        start_date = (base_time + timedelta(days=1)).date()
        end_date = start_date
    elif period == "Эта неделя":
        start_date = base_time.date()
        end_date = start_date + timedelta(days=7)
    elif period == "Следующая неделя":
        start_date = (base_time + timedelta(days=7)).date()
        end_date = start_date + timedelta(days=7)
    else:  # Этот месяц
        start_date = base_time.date()
        end_date = start_date + timedelta(days=30)
    
    # Демо события
    demo_events = [
        {
            'title': 'Планерка команды',
            'start_time': (datetime.combine(start_date, datetime.min.time()) + timedelta(hours=9)).isoformat(),
            'duration': 1,
            'participants': ['Иван Иванов', 'Петр Петров', 'Анна Сидорова'],
            'description': 'Еженедельная планерка команды разработки',
            'location': 'Конференц-зал А',
            'type': 'Встречи',
            'priority': 'medium',
            'prepared': True
        },
        {
            'title': 'Презентация проекта клиенту',
            'start_time': (datetime.combine(start_date, datetime.min.time()) + timedelta(hours=14)).isoformat(),
            'duration': 2,
            'participants': ['Директор', 'Менеджер проекта', 'Клиент'],
            'description': 'Презентация результатов первого этапа проекта',
            'location': 'Online (Zoom)',
            'type': 'Презентации',
            'priority': 'high',
            'prepared': False
        },
        {
            'title': 'Интервью с кандидатом',
            'start_time': (datetime.combine(start_date + timedelta(days=1), datetime.min.time()) + timedelta(hours=11)).isoformat(),
            'duration': 1.5,
            'participants': ['HR менеджер', 'Тимлид'],
            'description': 'Техническое интервью на позицию Senior Developer',
            'location': 'Офис, переговорная 2',
            'type': 'Интервью',
            'priority': 'medium',
            'prepared': False
        }
    ]
    
    return demo_events

def is_today(timestamp):
    """Проверка, является ли событие сегодняшним"""
    if not timestamp:
        return False
    try:
        event_date = datetime.fromisoformat(timestamp).date()
        return event_date == datetime.now().date()
    except:
        return False

def is_upcoming(timestamp):
    """Проверка, является ли событие предстоящим"""
    if not timestamp:
        return False
    try:
        event_time = datetime.fromisoformat(timestamp)
        return event_time > datetime.now()
    except:
        return False

def calculate_free_time(events):
    """Расчет свободного времени"""
    total_hours = sum(event.get('duration', 1) for event in events)
    work_hours = 8  # Рабочий день
    return f"{work_hours - min(total_hours, work_hours):.1f}ч"

def format_event_time(event):
    """Форматирование времени события"""
    start_time = event.get('start_time')
    if start_time:
        try:
            dt = datetime.fromisoformat(start_time)
            return dt.strftime("%d.%m.%Y %H:%M")
        except:
            return start_time
    return "Время не указано"

def get_event_type_badge(event_type):
    """Создание бейджа типа события"""
    colors = {
        'Встречи': '#28a745',
        'Созвоны': '#17a2b8',
        'Презентации': '#ffc107',
        'Интервью': '#dc3545',
        'Личные': '#6c757d'
    }
    
    color = colors.get(event_type, '#6c757d')
    return f'<span style="background-color: {color}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px;">{event_type}</span>'

def generate_recommendations(events):
    """Генерация рекомендаций на основе календаря"""
    recommendations = []
    
    # Проверка загруженности
    daily_events = {}
    for event in events:
        if event.get('start_time'):
            try:
                date = datetime.fromisoformat(event['start_time']).date()
                daily_events[date] = daily_events.get(date, 0) + 1
            except:
                continue
    
    # Слишком много встреч в день
    for date, count in daily_events.items():
        if count > 5:
            recommendations.append(f"⚠️ {date.strftime('%d.%m.%Y')}: Слишком много встреч ({count}). Рассмотрите возможность переноса.")
    
    # Проверка подготовки
    unprepared = len([e for e in events if not e.get('prepared', False)])
    if unprepared > 0:
        recommendations.append(f"📋 {unprepared} встреч требуют подготовки. Запланируйте время для подготовки материалов.")
    
    # Проверка времени между встречами
    sorted_events = sorted(events, key=lambda x: x.get('start_time', ''))
    for i in range(len(sorted_events) - 1):
        try:
            current_end = datetime.fromisoformat(sorted_events[i]['start_time']) + timedelta(hours=sorted_events[i].get('duration', 1))
            next_start = datetime.fromisoformat(sorted_events[i+1]['start_time'])
            
            gap = (next_start - current_end).total_seconds() / 60  # в минутах
            
            if gap < 15:
                recommendations.append(f"⏰ Между встречами '{sorted_events[i]['title']}' и '{sorted_events[i+1]['title']}' только {gap:.0f} минут. Возможна задержка.")
        except:
            continue
    
    if not recommendations:
        recommendations.append("✅ Календарь хорошо организован, рекомендаций нет.")
    
    return recommendations

def prepare_meeting(event):
    """Подготовка к встрече"""
    st.success(f"Начата подготовка к встрече: {event.get('title')}")
    
    # Здесь можно добавить логику подготовки:
    # - Сбор материалов
    # - Создание повестки
    # - Отправка уведомлений
    
def create_agenda(event):
    """Создание повестки дня"""
    st.info(f"Создание повестки для: {event.get('title')}")
    
    # Здесь можно добавить ИИ генерацию повестки
    # на основе информации о встрече

if __name__ == "__main__":
    main()