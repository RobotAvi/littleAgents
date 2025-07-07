"""
Общие утилитарные функции для всех утилит
"""

import logging
import os
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import streamlit as st
import pandas as pd
import math

def setup_logging(utility_name: str, log_level: str = "INFO"):
    """Настройка логирования для утилиты"""
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, f"{utility_name}.log")
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(utility_name)

def format_datetime(dt: datetime) -> str:
    """Форматирование даты и времени"""
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def parse_datetime(dt_str: str) -> Optional[datetime]:
    """Парсинг строки даты и времени"""
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%d.%m.%Y %H:%M",
        "%d.%m.%Y"
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(dt_str, fmt)
        except ValueError:
            continue
    
    return None

def save_json_data(data: Dict[str, Any], filename: str) -> None:
    """Сохранение данных в JSON файл"""
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    filepath = os.path.join(data_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)

def load_json_data(filename: str) -> Optional[Dict[str, Any]]:
    """Загрузка данных из JSON файла"""
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    filepath = os.path.join(data_dir, filename)
    
    if not os.path.exists(filepath):
        return None
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logging.error(f"Ошибка загрузки данных из {filename}: {e}")
        return None

def create_streamlit_header(title: str, description: str = ""):
    """Создание заголовка для Streamlit приложения"""
    st.set_page_config(
        page_title=title,
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title(f"🤖 {title}")
    if description:
        st.markdown(f"*{description}*")
    st.divider()

def display_metrics(metrics: Dict[str, Any]):
    """Отображение метрик в Streamlit"""
    cols = st.columns(len(metrics))
    
    for i, (label, value) in enumerate(metrics.items()):
        with cols[i]:
            if isinstance(value, dict) and 'value' in value:
                st.metric(
                    label=label,
                    value=value['value'],
                    delta=value.get('delta', None)
                )
            else:
                st.metric(label=label, value=value)

def create_status_badge(status: str) -> str:
    """Создание бейджа статуса"""
    status_colors = {
        'active': '#28a745',
        'warning': '#ffc107',
        'error': '#dc3545',
        'info': '#17a2b8',
        'success': '#28a745'
    }
    
    color = status_colors.get(status.lower(), '#6c757d')
    return f'<span style="background-color: {color}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px;">{status}</span>'

def display_data_table(data: List[Dict], title: str = "Данные"):
    """Отображение таблицы данных"""
    if not data:
        st.info("Нет данных для отображения")
        return
    
    df = pd.DataFrame(data)
    
    with st.expander(f"📊 {title} ({len(data)} элементов)"):
        st.dataframe(df, use_container_width=True)

def async_to_sync(async_func):
    """Декоратор для выполнения асинхронных функций в синхронном контексте"""
    def wrapper(*args, **kwargs):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(async_func(*args, **kwargs))
    
    return wrapper

def create_sidebar_filters(filter_options: Dict[str, List]) -> Dict[str, Any]:
    """Создание фильтров в боковой панели"""
    st.sidebar.header("🔧 Фильтры")
    
    filters = {}
    
    for filter_name, options in filter_options.items():
        if isinstance(options, list):
            filters[filter_name] = st.sidebar.selectbox(
                f"Выберите {filter_name}:",
                options
            )
        elif isinstance(options, dict):
            if options.get('type') == 'date':
                filters[filter_name] = st.sidebar.date_input(
                    f"Выберите {filter_name}:",
                    value=options.get('default', datetime.now().date())
                )
            elif options.get('type') == 'multiselect':
                filters[filter_name] = st.sidebar.multiselect(
                    f"Выберите {filter_name}:",
                    options.get('options', []),
                    default=options.get('default', [])
                )
    
    return filters

def send_notification(message: str, notification_type: str = "info"):
    """Отправка уведомления в интерфейсе"""
    if notification_type == "success":
        st.success(message)
    elif notification_type == "warning":
        st.warning(message)
    elif notification_type == "error":
        st.error(message)
    else:
        st.info(message)

def format_file_size(size_bytes: int) -> str:
    """Форматирование размера файла"""
    if size_bytes == 0:
        return "0B"
    
    size_name = ["B", "KB", "MB", "GB", "TB"]
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    
    return f"{s} {size_name[i]}"

def truncate_text(text: str, max_length: int = 100) -> str:
    """Обрезка текста с добавлением многоточия"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def validate_config(config: Dict[str, Any], required_keys: List[str]) -> bool:
    """Валидация конфигурации"""
    missing_keys = [key for key in required_keys if not config.get(key)]
    
    if missing_keys:
        st.error(f"Отсутствуют обязательные настройки: {', '.join(missing_keys)}")
        st.info("Пожалуйста, настройте переменные окружения в файле .env")
        return False
    
    return True