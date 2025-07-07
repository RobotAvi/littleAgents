"""
Общие настройки для всех утилит
"""

import os
from decouple import config
from typing import Dict, Any

class Config:
    """Класс конфигурации для всех утилит"""
    
    # API ключи
    OPENAI_API_KEY = config('OPENAI_API_KEY', default='')
    OPENAI_MODEL = config('OPENAI_MODEL', default='gpt-3.5-turbo')
    
    # Telegram
    TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN', default='')
    TELEGRAM_CHAT_ID = config('TELEGRAM_CHAT_ID', default='')
    
    # Email
    EMAIL_USER = config('EMAIL_USER', default='')
    EMAIL_PASSWORD = config('EMAIL_PASSWORD', default='')
    EMAIL_IMAP_SERVER = config('EMAIL_IMAP_SERVER', default='imap.gmail.com')
    EMAIL_IMAP_PORT = config('EMAIL_IMAP_PORT', default=993, cast=int)
    
    # YouTrack
    YOUTRACK_URL = config('YOUTRACK_URL', default='')
    YOUTRACK_TOKEN = config('YOUTRACK_TOKEN', default='')
    
    # Git
    GIT_REPOS_PATH = config('GIT_REPOS_PATH', default='')
    GITHUB_TOKEN = config('GITHUB_TOKEN', default='')
    
    # Grafana
    GRAFANA_URL = config('GRAFANA_URL', default='')
    GRAFANA_API_KEY = config('GRAFANA_API_KEY', default='')
    
    # Calendar (Google Calendar)
    GOOGLE_CALENDAR_CREDENTIALS = config('GOOGLE_CALENDAR_CREDENTIALS', default='')
    GOOGLE_CALENDAR_ID = config('GOOGLE_CALENDAR_ID', default='primary')
    
    # Database
    DATABASE_URL = config('DATABASE_URL', default='sqlite:///utilities.db')
    
    # Redis
    REDIS_URL = config('REDIS_URL', default='redis://localhost:6379')
    
    # Logging
    LOG_LEVEL = config('LOG_LEVEL', default='INFO')
    LOG_FILE = config('LOG_FILE', default='utilities.log')
    
    # Streamlit
    STREAMLIT_PORT = config('STREAMLIT_PORT', default=8501, cast=int)
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    UTILITIES_DIR = os.path.join(BASE_DIR, 'utilities')
    SHARED_DIR = os.path.join(BASE_DIR, 'shared')
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    LOGS_DIR = os.path.join(BASE_DIR, 'logs')
    
    @classmethod
    def get_utility_config(cls, utility_name: str) -> Dict[str, Any]:
        """Получить конфигурацию для конкретной утилиты"""
        base_config = {
            'openai_api_key': cls.OPENAI_API_KEY,
            'openai_model': cls.OPENAI_MODEL,
            'telegram_bot_token': cls.TELEGRAM_BOT_TOKEN,
            'telegram_chat_id': cls.TELEGRAM_CHAT_ID,
            'database_url': cls.DATABASE_URL,
            'redis_url': cls.REDIS_URL,
            'log_level': cls.LOG_LEVEL,
            'log_file': cls.LOG_FILE
        }
        
        # Специфичные настройки для каждой утилиты
        utility_specific = {
            'email_manager': {
                'email_user': cls.EMAIL_USER,
                'email_password': cls.EMAIL_PASSWORD,
                'imap_server': cls.EMAIL_IMAP_SERVER,
                'imap_port': cls.EMAIL_IMAP_PORT
            },
            'task_manager': {
                'youtrack_url': cls.YOUTRACK_URL,
                'youtrack_token': cls.YOUTRACK_TOKEN
            },
            'git_monitor': {
                'git_repos_path': cls.GIT_REPOS_PATH,
                'github_token': cls.GITHUB_TOKEN
            },
            'infrastructure_monitor': {
                'grafana_url': cls.GRAFANA_URL,
                'grafana_api_key': cls.GRAFANA_API_KEY
            },
            'calendar_manager': {
                'google_calendar_credentials': cls.GOOGLE_CALENDAR_CREDENTIALS,
                'google_calendar_id': cls.GOOGLE_CALENDAR_ID
            }
        }
        
        config_dict = base_config.copy()
        if utility_name in utility_specific:
            config_dict.update(utility_specific[utility_name])
        
        return config_dict
    
    @classmethod
    def create_directories(cls):
        """Создать необходимые директории"""
        directories = [cls.DATA_DIR, cls.LOGS_DIR]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

# Инициализация конфигурации
app_config = Config()
app_config.create_directories()