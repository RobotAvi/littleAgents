"""
Клиент для работы с электронной почтой
"""

import imaplib
import email
from email.header import decode_header
from typing import List, Dict, Any, Optional
from datetime import datetime, date
import logging
import ssl
import re

logger = logging.getLogger(__name__)

class EmailClient:
    def __init__(self, username: str, password: str, imap_server: str = "imap.gmail.com", imap_port: int = 993):
        self.username = username
        self.password = password
        self.imap_server = imap_server
        self.imap_port = imap_port
        self.connection = None
    
    def connect(self) -> bool:
        """Подключение к почтовому серверу"""
        try:
            # Создание SSL контекста
            context = ssl.create_default_context()
            
            # Подключение к IMAP серверу
            self.connection = imaplib.IMAP4_SSL(self.imap_server, self.imap_port, ssl_context=context)
            
            # Авторизация
            self.connection.login(self.username, self.password)
            logger.info(f"Успешное подключение к {self.imap_server}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка подключения к почтовому серверу: {e}")
            return False
    
    def disconnect(self):
        """Отключение от почтового сервера"""
        if self.connection:
            try:
                self.connection.close()
                self.connection.logout()
                logger.info("Отключение от почтового сервера")
            except Exception as e:
                logger.error(f"Ошибка при отключении: {e}")
    
    def get_emails(self, folder: str = "INBOX", since_date: Optional[date] = None, limit: int = 20) -> List[Dict[str, Any]]:
        """Получение списка писем"""
        if not self.connect():
            return []
        
        try:
            # Выбор папки
            self.connection.select(folder)
            
            # Формирование критерия поиска
            search_criteria = "ALL"
            if since_date:
                date_str = since_date.strftime("%d-%b-%Y")
                search_criteria = f'SINCE {date_str}'
            
            # Поиск писем
            status, message_ids = self.connection.search(None, search_criteria)
            
            if status != 'OK':
                logger.error("Ошибка поиска писем")
                return []
            
            # Получение ID писем
            email_ids = message_ids[0].split()
            
            # Ограничение количества писем
            if limit:
                email_ids = email_ids[-limit:]
            
            emails = []
            
            for email_id in email_ids:
                try:
                    # Получение письма
                    status, message_data = self.connection.fetch(email_id, '(RFC822)')
                    
                    if status != 'OK':
                        continue
                    
                    # Парсинг письма
                    email_message = email.message_from_bytes(message_data[0][1])
                    
                    # Извлечение данных
                    email_data = self._parse_email(email_message, email_id.decode())
                    emails.append(email_data)
                    
                except Exception as e:
                    logger.error(f"Ошибка обработки письма {email_id}: {e}")
                    continue
            
            return emails
            
        except Exception as e:
            logger.error(f"Ошибка получения писем: {e}")
            return []
        
        finally:
            self.disconnect()
    
    def _parse_email(self, email_message: email.message.EmailMessage, email_id: str) -> Dict[str, Any]:
        """Парсинг одного письма"""
        
        # Декодирование заголовков
        def decode_email_header(header):
            if header:
                decoded_header = decode_header(header)[0]
                if decoded_header[1]:
                    return decoded_header[0].decode(decoded_header[1])
                else:
                    return str(decoded_header[0])
            return ""
        
        # Извлечение основных данных
        subject = decode_email_header(email_message.get("Subject", ""))
        from_address = decode_email_header(email_message.get("From", ""))
        to_address = decode_email_header(email_message.get("To", ""))
        date_str = email_message.get("Date", "")
        
        # Парсинг даты
        email_date = None
        if date_str:
            try:
                email_date = email.utils.parsedate_to_datetime(date_str)
            except Exception as e:
                logger.warning(f"Ошибка парсинга даты {date_str}: {e}")
        
        # Извлечение содержимого письма
        body = self._extract_email_body(email_message)
        
        # Определение приоритета
        priority = self._determine_priority(email_message, subject, body)
        
        # Проверка статуса прочтения
        read_status = self._check_read_status(email_message)
        
        return {
            'id': email_id,
            'subject': subject,
            'from': from_address,
            'to': to_address,
            'date': email_date.isoformat() if email_date else date_str,
            'body': body,
            'priority': priority,
            'read': read_status,
            'attachments': self._get_attachments(email_message)
        }
    
    def _extract_email_body(self, email_message: email.message.EmailMessage) -> str:
        """Извлечение текста письма"""
        body = ""
        
        try:
            if email_message.is_multipart():
                # Обработка многочастного письма
                for part in email_message.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition", ""))
                    
                    # Пропуск вложений
                    if "attachment" in content_disposition:
                        continue
                    
                    if content_type == "text/plain":
                        charset = part.get_content_charset() or 'utf-8'
                        body = part.get_payload(decode=True).decode(charset, errors='ignore')
                        break
                    elif content_type == "text/html" and not body:
                        charset = part.get_content_charset() or 'utf-8'
                        html_body = part.get_payload(decode=True).decode(charset, errors='ignore')
                        # Простое удаление HTML тегов
                        body = re.sub('<[^<]+?>', '', html_body)
            else:
                # Обработка простого письма
                charset = email_message.get_content_charset() or 'utf-8'
                body = email_message.get_payload(decode=True).decode(charset, errors='ignore')
        
        except Exception as e:
            logger.error(f"Ошибка извлечения содержимого письма: {e}")
            body = "Ошибка чтения содержимого письма"
        
        return body.strip()
    
    def _determine_priority(self, email_message: email.message.EmailMessage, subject: str, body: str) -> str:
        """Определение приоритета письма"""
        
        # Проверка заголовков приоритета
        priority_header = email_message.get("X-Priority", "").lower()
        importance_header = email_message.get("Importance", "").lower()
        
        if priority_header in ["1", "2"] or importance_header == "high":
            return "high"
        
        # Ключевые слова высокого приоритета
        high_priority_keywords = [
            "срочно", "urgent", "важно", "important", "критично", "critical",
            "немедленно", "asap", "emergency", "экстренно"
        ]
        
        # Ключевые слова среднего приоритета  
        medium_priority_keywords = [
            "встреча", "meeting", "созвон", "call", "задача", "task",
            "проект", "project", "отчет", "report"
        ]
        
        text_to_check = (subject + " " + body).lower()
        
        for keyword in high_priority_keywords:
            if keyword in text_to_check:
                return "high"
        
        for keyword in medium_priority_keywords:
            if keyword in text_to_check:
                return "medium"
        
        return "low"
    
    def _check_read_status(self, email_message: email.message.EmailMessage) -> bool:
        """Проверка статуса прочтения письма"""
        # В IMAP это сложнее определить без дополнительных запросов
        # Пока возвращаем False (непрочитано) для демонстрации
        return False
    
    def _get_attachments(self, email_message: email.message.EmailMessage) -> List[str]:
        """Получение списка вложений"""
        attachments = []
        
        try:
            for part in email_message.walk():
                content_disposition = str(part.get("Content-Disposition", ""))
                
                if "attachment" in content_disposition:
                    filename = part.get_filename()
                    if filename:
                        # Декодирование имени файла
                        decoded_filename = decode_header(filename)[0]
                        if decoded_filename[1]:
                            filename = decoded_filename[0].decode(decoded_filename[1])
                        else:
                            filename = str(decoded_filename[0])
                        
                        attachments.append(filename)
        
        except Exception as e:
            logger.error(f"Ошибка получения вложений: {e}")
        
        return attachments
    
    def mark_as_read(self, email_id: str, folder: str = "INBOX") -> bool:
        """Отметить письмо как прочитанное"""
        if not self.connect():
            return False
        
        try:
            self.connection.select(folder)
            self.connection.store(email_id, '+FLAGS', '\\Seen')
            return True
        
        except Exception as e:
            logger.error(f"Ошибка отметки письма как прочитанного: {e}")
            return False
        
        finally:
            self.disconnect()
    
    def delete_email(self, email_id: str, folder: str = "INBOX") -> bool:
        """Удаление письма"""
        if not self.connect():
            return False
        
        try:
            self.connection.select(folder)
            self.connection.store(email_id, '+FLAGS', '\\Deleted')
            self.connection.expunge()
            return True
        
        except Exception as e:
            logger.error(f"Ошибка удаления письма: {e}")
            return False
        
        finally:
            self.disconnect()