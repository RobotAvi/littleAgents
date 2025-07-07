"""
Общий клиент для работы с LLM (OpenAI GPT)
"""

import openai
from typing import List, Dict, Any, Optional
import logging
from decouple import config

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=config('OPENAI_API_KEY', default='')
        )
        self.model = config('OPENAI_MODEL', default='gpt-3.5-turbo')
        
    async def analyze_text(self, text: str, context: str = "") -> str:
        """Анализ текста с помощью LLM"""
        try:
            messages = [
                {"role": "system", "content": f"Ты - умный помощник для анализа данных. {context}"},
                {"role": "user", "content": text}
            ]
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Ошибка при анализе текста: {e}")
            return f"Ошибка анализа: {str(e)}"
    
    async def summarize_emails(self, emails: List[Dict]) -> str:
        """Создание сводки по письмам"""
        emails_text = "\n\n".join([
            f"От: {email.get('from', 'Unknown')}\n"
            f"Тема: {email.get('subject', 'No subject')}\n"
            f"Дата: {email.get('date', 'Unknown')}\n"
            f"Содержание: {email.get('body', 'No content')[:200]}..."
            for email in emails
        ])
        
        context = """
        Проанализируй входящие письма и создай краткую сводку. 
        Выдели:
        1. Самые важные письма, требующие внимания
        2. Письма, которые требуют ответа
        3. Общую статистику
        4. Рекомендации по действиям
        
        Ответь на русском языке в структурированном виде.
        """
        
        return await self.analyze_text(emails_text, context)
    
    async def analyze_calendar_events(self, events: List[Dict]) -> str:
        """Анализ событий календаря"""
        events_text = "\n\n".join([
            f"Событие: {event.get('title', 'Без названия')}\n"
            f"Время: {event.get('start_time', 'Unknown')} - {event.get('end_time', 'Unknown')}\n"
            f"Участники: {', '.join(event.get('participants', []))}\n"
            f"Описание: {event.get('description', 'Нет описания')}"
            for event in events
        ])
        
        context = """
        Проанализируй события календаря на сегодня и ближайшие дни.
        Создай краткую сводку с:
        1. Количеством встреч
        2. Самыми важными событиями
        3. Временными интервалами
        4. Рекомендациями по подготовке
        
        Ответь на русском языке.
        """
        
        return await self.analyze_text(events_text, context)
    
    async def analyze_telegram_messages(self, messages: List[Dict]) -> str:
        """Анализ сообщений Telegram"""
        messages_text = "\n\n".join([
            f"От: {msg.get('from', 'Unknown')}\n"
            f"Время: {msg.get('timestamp', 'Unknown')}\n"
            f"Сообщение: {msg.get('text', 'No text')}"
            for msg in messages
        ])
        
        context = """
        Проанализируй непрочитанные сообщения в Telegram.
        Выдели:
        1. Сообщения, требующие срочного ответа
        2. Важную информацию
        3. Статистику по отправителям
        4. Рекомендации по действиям
        
        Ответь на русском языке в структурированном виде.
        """
        
        return await self.analyze_text(messages_text, context)
    
    async def analyze_tasks(self, tasks: List[Dict]) -> str:
        """Анализ задач из YouTrack"""
        tasks_text = "\n\n".join([
            f"Задача: {task.get('title', 'Без названия')}\n"
            f"Статус: {task.get('status', 'Unknown')}\n"
            f"Приоритет: {task.get('priority', 'Normal')}\n"
            f"Исполнитель: {task.get('assignee', 'Не назначен')}\n"
            f"Дедлайн: {task.get('due_date', 'Не указан')}\n"
            f"Описание: {task.get('description', 'Нет описания')[:100]}..."
            for task in tasks
        ])
        
        context = """
        Проанализируй задачи из системы управления задачами.
        Создай отчет с:
        1. Просроченными задачами
        2. Задачами с высоким приоритетом
        3. Статистикой по статусам
        4. Рекомендациями по приоритизации
        
        Ответь на русском языке в структурированном виде.
        """
        
        return await self.analyze_text(tasks_text, context)
    
    async def generate_meeting_agenda(self, meeting_info: Dict) -> str:
        """Генерация повестки встречи"""
        meeting_text = f"""
        Название встречи: {meeting_info.get('title', 'Встреча')}
        Участники: {', '.join(meeting_info.get('participants', []))}
        Длительность: {meeting_info.get('duration', '60 минут')}
        Цель: {meeting_info.get('purpose', 'Обсуждение вопросов')}
        Контекст: {meeting_info.get('context', 'Нет дополнительного контекста')}
        """
        
        context = """
        Создай структурированную повестку встречи на основе предоставленной информации.
        Включи:
        1. Приветствие и знакомство (если нужно)
        2. Основные вопросы для обсуждения
        3. Временные рамки для каждого пункта
        4. Следующие шаги и ответственные
        5. Время для вопросов
        
        Сделай повестку практичной и четкой. Ответь на русском языке.
        """
        
        return await self.analyze_text(meeting_text, context)
    
    async def create_action_items(self, meeting_notes: str) -> str:
        """Создание задач на основе заметок встречи"""
        context = """
        На основе заметок встречи создай список конкретных задач (action items).
        Для каждой задачи укажи:
        1. Что нужно сделать
        2. Кто ответственный
        3. Срок выполнения
        4. Приоритет
        
        Задачи должны быть конкретными и выполнимыми. Ответь на русском языке.
        """
        
        return await self.analyze_text(meeting_notes, context)

# Глобальный экземпляр клиента
llm_client = LLMClient()