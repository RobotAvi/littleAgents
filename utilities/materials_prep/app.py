"""
Утилита для подготовки материалов
Сбор документов, презентаций и других материалов для проектов.
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
        "Подготовка материалов", 
        "Сбор и организация документов, презентаций и других материалов"
    )
    
    # Боковая панель с настройками
    with st.sidebar:
        st.header("⚙️ Настройки")
        
        # Тип проекта
        project_type = st.selectbox(
            "Тип проекта:",
            ["Веб-разработка", "Мобильная разработка", "Исследование", "Презентация"],
            index=0
        )
        
        # Целевая аудитория
        audience = st.selectbox(
            "Целевая аудитория:",
            ["Техническая команда", "Менеджмент", "Клиенты", "Инвесторы"],
            index=0
        )
        
        if st.button("🔄 Обновить", type="primary"):
            st.rerun()
    
    # Основное содержимое
    tab1, tab2, tab3, tab4 = st.tabs([
        "📁 Материалы", "📊 Презентации", "📄 Документы", "🤖 ИИ Генератор"
    ])
    
    with tab1:
        st.subheader("📁 Управление материалами")
        
        # Загрузка файлов
        st.subheader("⬆️ Загрузка материалов")
        
        uploaded_files = st.file_uploader(
            "Выберите файлы:",
            accept_multiple_files=True,
            type=['pdf', 'pptx', 'docx', 'txt', 'md', 'jpg', 'png']
        )
        
        if uploaded_files:
            st.success(f"Загружено файлов: {len(uploaded_files)}")
            
            for file in uploaded_files:
                st.markdown(f"- 📄 {file.name} ({file.type})")
        
        # Каталог материалов
        st.subheader("📚 Каталог материалов")
        
        materials = [
            {"name": "Техническая архитектура", "type": "Диаграмма", "status": "Готов"},
            {"name": "User Stories", "type": "Документ", "status": "В работе"},
            {"name": "Дизайн макеты", "type": "Изображения", "status": "Готов"},
            {"name": "API документация", "type": "Документ", "status": "Готов"}
        ]
        
        for material in materials:
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                st.write(f"📄 **{material['name']}**")
            with col2:
                st.write(material['type'])
            with col3:
                if material['status'] == 'Готов':
                    st.success("✅")
                else:
                    st.warning("⏳")
            with col4:
                if st.button("📥", key=f"download_{material['name']}"):
                    st.info("Скачивание...")
    
    with tab2:
        st.subheader("📊 Создание презентаций")
        
        # Конструктор презентаций
        with st.form("presentation_builder"):
            st.subheader("🎨 Конструктор презентации")
            
            pres_title = st.text_input("Название презентации:")
            pres_sections = st.text_area(
                "Разделы (по одному на строку):",
                value="Введение\nОбзор проекта\nТехнические детали\nРезультаты\nВыводы"
            )
            pres_style = st.selectbox("Стиль:", ["Корпоративный", "Современный", "Минимализм"])
            
            if st.form_submit_button("🎯 Создать структуру"):
                if pres_title:
                    st.success("Структура презентации создана!")
                    
                    sections = pres_sections.strip().split('\n')
                    for i, section in enumerate(sections, 1):
                        st.markdown(f"{i}. **{section}**")
        
        # Шаблоны слайдов
        st.subheader("📑 Шаблоны слайдов")
        
        templates = [
            "🎯 Титульный слайд",
            "📊 Слайд с графиками", 
            "📋 Слайд со списком",
            "🖼️ Слайд с изображением",
            "💬 Слайд с цитатой"
        ]
        
        selected_template = st.selectbox("Выберите шаблон:", templates)
        
        if st.button("➕ Добавить слайд"):
            st.success(f"Добавлен: {selected_template}")
    
    with tab3:
        st.subheader("📄 Создание документов")
        
        # Типы документов
        doc_types = {
            "Техническое задание": ["Описание проекта", "Требования", "Ограничения", "Критерии приемки"],
            "Отчет по проекту": ["Резюме", "Достигнутые результаты", "Проблемы", "Рекомендации"],
            "Руководство пользователя": ["Введение", "Установка", "Использование", "FAQ"]
        }
        
        selected_doc_type = st.selectbox("Тип документа:", list(doc_types.keys()))
        
        if st.button("📝 Создать документ"):
            st.subheader(f"📄 Структура: {selected_doc_type}")
            
            sections = doc_types[selected_doc_type]
            for i, section in enumerate(sections, 1):
                st.markdown(f"{i}. **{section}**")
                st.text_area(f"Содержание раздела {i}:", key=f"section_{i}", height=100)
        
        # Генерация документа
        if st.button("🤖 Автогенерация содержимого"):
            st.info("Здесь будет автоматическая генерация содержимого документа на основе ИИ")
    
    with tab4:
        st.subheader("🤖 ИИ Генератор контента")
        
        # Генерация текста
        st.subheader("✍️ Генерация текста")
        
        with st.form("text_generator"):
            text_topic = st.text_input("Тема:")
            text_type = st.selectbox("Тип контента:", ["Описание", "Инструкция", "Обзор", "Заключение"])
            text_length = st.selectbox("Длина:", ["Короткий", "Средний", "Подробный"])
            
            if st.form_submit_button("🤖 Сгенерировать"):
                if text_topic:
                    with st.spinner("Генерация текста..."):
                        
                        @async_to_sync
                        async def generate_text():
                            prompt = f"Создай {text_type.lower()} на тему '{text_topic}'. Длина: {text_length.lower()}."
                            return await llm_client.analyze_text("", prompt)
                        
                        generated_text = generate_text()
                        
                        st.subheader("📝 Сгенерированный текст")
                        st.markdown(generated_text)
                        
                        if st.button("💾 Сохранить текст"):
                            st.success("Текст сохранен!")
        
        # Анализ материалов
        st.subheader("🔍 Анализ материалов")
        
        if st.button("📊 Анализировать собранные материалы"):
            with st.spinner("Анализ материалов..."):
                analysis_text = """
                Анализ собранных материалов:
                
                📊 **Статистика:**
                - Всего материалов: 4
                - Готовых: 3
                - В работе: 1
                
                💡 **Рекомендации:**
                - Добавить больше визуальных элементов
                - Создать единый стиль оформления  
                - Подготовить резервные материалы
                """
                
                st.markdown(analysis_text)

if __name__ == "__main__":
    main()