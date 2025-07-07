"""
Утилита для репутации и коммуникаций
Фильтрация входящих звонков, мониторинг соцсетей и управление репутацией.
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
        "Репутация и коммуникации", 
        "Фильтрация звонков и мониторинг репутации в соцсетях"
    )
    
    # Боковая панель с настройками
    with st.sidebar:
        st.header("⚙️ Настройки")
        
        # Фильтрация звонков
        call_filter_mode = st.selectbox(
            "Режим фильтрации:",
            ["Строгий", "Умеренный", "Мягкий", "Отключен"],
            index=1
        )
        
        # Социальные сети для мониторинга
        social_networks = st.multiselect(
            "Мониторинг соцсетей:",
            ["LinkedIn", "Twitter", "Facebook", "Instagram", "YouTube"],
            default=["LinkedIn", "Twitter"]
        )
        
        # Период мониторинга
        monitoring_period = st.selectbox(
            "Период мониторинга:",
            ["Реальное время", "Последний час", "Сегодня", "Неделя"],
            index=2
        )
        
        if st.button("🔄 Обновить данные", type="primary"):
            st.rerun()
    
    # Основное содержимое
    tab1, tab2, tab3, tab4 = st.tabs([
        "📞 Звонки", "📱 Соцсети", "⭐ Репутация", "📊 Аналитика"
    ])
    
    with tab1:
        st.subheader("📞 Фильтрация звонков")
        
        # Статистика звонков
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Всего звонков", "45", "8")
        with col2:
            st.metric("Пропущено фильтром", "23", "5")
        with col3:
            st.metric("Разрешено", "22", "3")
        with col4:
            st.metric("% блокировки", "51%", "2%")
        
        # Последние звонки
        st.subheader("📋 Последние звонки")
        
        recent_calls = [
            {"time": "14:30", "number": "+7-495-123-45-67", "name": "ООО Ромашка", "action": "Разрешен", "reason": "Белый список"},
            {"time": "14:15", "number": "+7-800-555-35-35", "name": "Неизвестно", "action": "Заблокирован", "reason": "Спам номер"},
            {"time": "13:45", "number": "+7-916-234-56-78", "name": "Иван Петров", "action": "Разрешен", "reason": "Контакт"},
            {"time": "13:20", "number": "+7-495-000-00-00", "name": "Реклама", "action": "Заблокирован", "reason": "Черный список"}
        ]
        
        for call in recent_calls:
            with st.expander(f"📞 {call['time']} - {call['number']}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Номер:** {call['number']}")
                    st.markdown(f"**Имя:** {call['name']}")
                    st.markdown(f"**Причина:** {call['reason']}")
                
                with col2:
                    if call['action'] == 'Разрешен':
                        st.success("✅ Разрешен")
                    else:
                        st.error("❌ Заблокирован")
                    
                    if st.button(f"Изменить статус", key=f"change_{call['number']}"):
                        st.info("Статус изменен")
        
        # Настройки фильтрации
        st.subheader("⚙️ Настройки фильтра")
        
        with st.expander("📝 Управление списками"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("✅ Белый список")
                whitelist_number = st.text_input("Добавить номер в белый список:")
                if st.button("Добавить в белый список"):
                    if whitelist_number:
                        st.success(f"Номер {whitelist_number} добавлен в белый список")
                
                # Показать белый список
                whitelist = ["+7-495-123-45-67", "+7-916-234-56-78"]
                for number in whitelist:
                    col_num, col_del = st.columns([3, 1])
                    with col_num:
                        st.write(number)
                    with col_del:
                        if st.button("🗑️", key=f"del_white_{number}"):
                            st.warning(f"Удален из белого списка")
            
            with col2:
                st.subheader("❌ Черный список")
                blacklist_number = st.text_input("Добавить номер в черный список:")
                if st.button("Добавить в черный список"):
                    if blacklist_number:
                        st.success(f"Номер {blacklist_number} добавлен в черный список")
                
                # Показать черный список
                blacklist = ["+7-800-555-35-35", "+7-495-000-00-00"]
                for number in blacklist:
                    col_num, col_del = st.columns([3, 1])
                    with col_num:
                        st.write(number)
                    with col_del:
                        if st.button("🗑️", key=f"del_black_{number}"):
                            st.warning(f"Удален из черного списка")
    
    with tab2:
        st.subheader("📱 Мониторинг соцсетей")
        
        # Упоминания
        st.subheader("💬 Последние упоминания")
        
        mentions = [
            {"platform": "LinkedIn", "author": "Анна Иванова", "text": "Отличная работа команды!", "sentiment": "positive", "time": "2 часа назад"},
            {"platform": "Twitter", "author": "@tech_user", "text": "Есть вопросы по API", "sentiment": "neutral", "time": "4 часа назад"},
            {"platform": "Facebook", "author": "Петр Петров", "text": "Не работает функция экспорта", "sentiment": "negative", "time": "6 часов назад"}
        ]
        
        for mention in mentions:
            with st.expander(f"💬 {mention['platform']} - {mention['author']}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Автор:** {mention['author']}")
                    st.markdown(f"**Текст:** {mention['text']}")
                    st.markdown(f"**Время:** {mention['time']}")
                
                with col2:
                    if mention['sentiment'] == 'positive':
                        st.success("😊 Позитивный")
                    elif mention['sentiment'] == 'negative':
                        st.error("😞 Негативный")
                    else:
                        st.info("😐 Нейтральный")
                    
                    if st.button("Ответить", key=f"reply_{mention['author']}"):
                        st.info("Открыт редактор ответа")
        
        # Настройки мониторинга
        st.subheader("🔍 Настройки мониторинга")
        
        with st.form("monitoring_settings"):
            col1, col2 = st.columns(2)
            
            with col1:
                keywords = st.text_area("Ключевые слова (по одному на строку):", 
                                      value="название компании\nназвание продукта\nCEO имя")
                
            with col2:
                exclude_keywords = st.text_area("Исключить слова:", 
                                               value="реклама\nспам")
                notification_email = st.text_input("Email для уведомлений:")
            
            if st.form_submit_button("Сохранить настройки"):
                st.success("Настройки мониторинга сохранены!")
    
    with tab3:
        st.subheader("⭐ Управление репутацией")
        
        # Общий рейтинг репутации
        st.subheader("📊 Рейтинг репутации")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Общий рейтинг", "8.7/10", "0.2")
        with col2:
            st.metric("Упоминаний", "156", "12")
        with col3:
            st.metric("Позитивных", "89%", "3%")
        with col4:
            st.metric("Охват", "12.5K", "1.2K")
        
        # Распределение по платформам
        st.subheader("📈 Активность по платформам")
        
        import pandas as pd
        import plotly.express as px
        
        platform_data = pd.DataFrame({
            'Платформа': ['LinkedIn', 'Twitter', 'Facebook', 'Instagram'],
            'Упоминания': [45, 38, 42, 31],
            'Позитивные': [40, 28, 35, 28],
            'Негативные': [3, 8, 5, 2]
        })
        
        fig = px.bar(platform_data, x='Платформа', y=['Позитивные', 'Негативные'],
                    title="Тональность упоминаний по платформам", barmode='stack')
        st.plotly_chart(fig, use_container_width=True)
        
        # Кризисные ситуации
        st.subheader("🚨 Мониторинг кризисов")
        
        crisis_indicators = [
            {"indicator": "Резкий рост негативных отзывов", "status": "Норма", "value": "2%"},
            {"indicator": "Снижение упоминаний", "status": "Внимание", "value": "-15%"},
            {"indicator": "Критические комментарии", "status": "Норма", "value": "1"},
            {"indicator": "Вирусные негативные посты", "status": "Норма", "value": "0"}
        ]
        
        for indicator in crisis_indicators:
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"📊 {indicator['indicator']}")
            with col2:
                if indicator['status'] == 'Норма':
                    st.success("✅ Норма")
                elif indicator['status'] == 'Внимание':
                    st.warning("⚠️ Внимание")
                else:
                    st.error("🚨 Кризис")
            with col3:
                st.write(indicator['value'])
    
    with tab4:
        st.subheader("📊 Аналитика и отчеты")
        
        # Генерация отчета с ИИ
        if st.button("🤖 Анализ репутации", type="primary"):
            with st.spinner("Анализ репутационных данных..."):
                
                reputation_data = f"""
                Данные по репутации за {monitoring_period}:
                
                Общий рейтинг: 8.7/10 (рост на 0.2)
                Всего упоминаний: 156 (рост на 12)
                Позитивных отзывов: 89%
                Негативных отзывов: 8%
                Нейтральных: 3%
                
                Распределение по платформам:
                - LinkedIn: 45 упоминаний (88% позитивных)
                - Twitter: 38 упоминаний (74% позитивных)
                - Facebook: 42 упоминания (83% позитивных)
                - Instagram: 31 упоминание (90% позитивных)
                
                Проблемные области:
                - Снижение упоминаний на 15%
                - Рост негативных отзывов в Twitter
                """
                
                @async_to_sync
                async def analyze_reputation():
                    return await llm_client.analyze_text(
                        reputation_data,
                        "Проанализируй репутационную ситуацию компании. "
                        "Выдели риски, возможности и рекомендации по улучшению репутации."
                    )
                
                analysis = analyze_reputation()
                
                st.subheader("📝 Анализ репутации")
                st.markdown(analysis)
        
        # Экспорт отчетов
        st.subheader("📤 Отчеты")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Отчет по звонкам"):
                st.success("Отчет по звонкам сгенерирован!")
        
        with col2:
            if st.button("📱 Отчет по соцсетям"):
                st.success("Отчет по соцсетям готов!")
        
        with col3:
            if st.button("⭐ Сводный отчет"):
                st.success("Сводный отчет создан!")

if __name__ == "__main__":
    main()