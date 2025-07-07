"""
Главное меню AI Assistant Utilities Suite
"""

import streamlit as st
import os
import subprocess
import sys
from datetime import datetime

def main():
    st.set_page_config(
        page_title="AI Assistant Utilities Suite",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🤖 AI Assistant Utilities Suite")
    st.markdown("*Набор умных утилит для автоматизации административных и управленческих задач*")
    st.divider()
    
    # Боковая панель с навигацией
    with st.sidebar:
        st.header("🚀 Навигация")
        
        utilities = {
            "📧 Работа с почтой": {
                "path": "utilities/email_manager",
                "description": "Анализ входящих писем и создание задач",
                "status": "ready"
            },
            "📅 Календарь и встречи": {
                "path": "utilities/calendar_manager", 
                "description": "Проверка календаря и отправка сводок",
                "status": "ready"
            },
            "💬 Мессенджеры": {
                "path": "utilities/messenger_analyzer",
                "description": "Анализ сообщений в Telegram",
                "status": "ready"
            },
            "📋 Управление задачами": {
                "path": "utilities/task_manager",
                "description": "Анализ задач в YouTrack",
                "status": "ready"
            },
            "🔧 Контроль разработки": {
                "path": "utilities/git_monitor",
                "description": "Мониторинг изменений в Git",
                "status": "ready"
            },
            "📊 Мониторинг инфраструктуры": {
                "path": "utilities/infrastructure_monitor",
                "description": "Анализ логов Grafana",
                "status": "ready"
            },
            "🎯 Подготовка к встречам": {
                "path": "utilities/meeting_prep",
                "description": "Составление списков артефактов",
                "status": "ready"
            },
            "💼 Пресейлы и проектирование": {
                "path": "utilities/presales_manager",
                "description": "Обработка пресейлов и документации",
                "status": "ready"
            },
            "📚 Подготовка материалов": {
                "path": "utilities/materials_prep",
                "description": "Сбор документов и презентаций",
                "status": "ready"
            },
            "🎤 Ведение встреч": {
                "path": "utilities/meeting_conductor",
                "description": "Протоколирование и рассылка",
                "status": "ready"
            },
            "📈 Управление проектами": {
                "path": "utilities/project_manager",
                "description": "Актуализация планов MS Project",
                "status": "ready"
            },
            "👥 HR и коммуникации": {
                "path": "utilities/hr_communications",
                "description": "Проведение 1:1 встреч",
                "status": "ready"
            },
            "✈️ Командировки и поездки": {
                "path": "utilities/travel_organizer",
                "description": "Организация поездок",
                "status": "ready"
            },
            "💰 Финансы и администрирование": {
                "path": "utilities/finance_admin",
                "description": "Отчеты по расходам",
                "status": "ready"
            },
            "🎭 Личные поручения": {
                "path": "utilities/personal_tasks",
                "description": "Выполнение личных задач",
                "status": "ready"
            },
            "📱 Репутация и коммуникации": {
                "path": "utilities/reputation_manager",
                "description": "Входящие звонки и соцсети",
                "status": "ready"
            },
            "🎉 Организация мероприятий": {
                "path": "utilities/event_organizer",
                "description": "Подготовка мероприятий",
                "status": "ready"
            },
            "⚡ Оптимизация процессов": {
                "path": "utilities/process_optimizer",
                "description": "Анализ и улучшение рутины",
                "status": "ready"
            },
            "👤 База контактов и CRM": {
                "path": "utilities/crm_manager",
                "description": "Управление контактами",
                "status": "ready"
            }
        }
        
        selected_utility = st.selectbox(
            "Выберите утилиту:",
            list(utilities.keys()),
            index=0
        )
    
    # Главное содержимое
    if selected_utility:
        utility_info = utilities[selected_utility]
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.header(selected_utility)
            st.markdown(f"**Описание:** {utility_info['description']}")
            
            # Статус утилиты
            status_color = "🟢" if utility_info['status'] == 'ready' else "🟡"
            st.markdown(f"**Статус:** {status_color} {utility_info['status'].title()}")
            
            # Кнопка запуска
            if st.button(f"🚀 Запустить {selected_utility}", type="primary"):
                utility_path = utility_info['path']
                if os.path.exists(utility_path):
                    st.success(f"Запуск {selected_utility}...")
                    st.markdown(f"**Команда для запуска:**")
                    st.code(f"cd {utility_path} && streamlit run app.py")
                    
                    try:
                        # Попытка запуска в новой вкладке браузера
                        subprocess.Popen([
                            sys.executable, "-m", "streamlit", "run", 
                            os.path.join(utility_path, "app.py")
                        ])
                        st.success("Утилита запущена в новом окне браузера!")
                    except Exception as e:
                        st.error(f"Ошибка запуска: {e}")
                        st.info("Запустите утилиту вручную командой выше")
                else:
                    st.warning("Утилита еще не создана. Используйте команду для создания:")
                    st.code(f"mkdir -p {utility_path}")
        
        with col2:
            st.subheader("📊 Статистика")
            
            # Общая статистика
            total_utilities = len(utilities)
            ready_utilities = len([u for u in utilities.values() if u['status'] == 'ready'])
            
            st.metric("Всего утилит", total_utilities)
            st.metric("Готовых утилит", ready_utilities)
            st.metric("Прогресс", f"{(ready_utilities/total_utilities)*100:.0f}%")
            
            # Последняя активность
            st.subheader("⏰ Активность")
            st.text(f"Последний запуск: {datetime.now().strftime('%H:%M:%S')}")
    
    # Нижняя часть с дополнительной информацией
    st.divider()
    
    # Разделы утилит
    st.subheader("📋 Категории утилит")
    
    categories = {
        "📧 Коммуникации": [
            "📧 Работа с почтой",
            "💬 Мессенджеры", 
            "📱 Репутация и коммуникации"
        ],
        "📅 Планирование": [
            "📅 Календарь и встречи",
            "🎯 Подготовка к встречам",
            "🎤 Ведение встреч",
            "🎉 Организация мероприятий"
        ],
        "🎯 Управление проектами": [
            "📋 Управление задачами",
            "📈 Управление проектами",
            "🔧 Контроль разработки",
            "💼 Пресейлы и проектирование"
        ],
        "🔧 Мониторинг": [
            "📊 Мониторинг инфраструктуры",
            "⚡ Оптимизация процессов"
        ],
        "👥 HR и личные задачи": [
            "👥 HR и коммуникации",
            "✈️ Командировки и поездки",
            "🎭 Личные поручения",
            "💰 Финансы и администрирование",
            "📚 Подготовка материалов",
            "👤 База контактов и CRM"
        ]
    }
    
    for category, utility_list in categories.items():
        with st.expander(category):
            for utility in utility_list:
                if utility in utilities:
                    status_icon = "🟢" if utilities[utility]['status'] == 'ready' else "🟡"
                    st.markdown(f"{status_icon} **{utility}** - {utilities[utility]['description']}")
    
    # Футер
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🤖 AI Assistant Utilities Suite | Создано для автоматизации рабочих процессов</p>
        <p>📧 Поддержка: support@ai-utilities.com | 🌐 GitHub: github.com/ai-utilities</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()