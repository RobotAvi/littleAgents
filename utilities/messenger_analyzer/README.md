# Анализ мессенджеров

Утилита для обработки и анализа сообщений в Telegram с помощью искусственного интеллекта.

## 🚀 Возможности

- **Мониторинг сообщений** - отслеживание входящих сообщений в Telegram
- **Анализ приоритетов** - определение важности сообщений с помощью ИИ  
- **Автоматическая категоризация** - классификация по типам чатов
- **Создание задач** - генерация задач на основе важных сообщений
- **Статистика активности** - графики и метрики по сообщениям

## 📋 Функции

### 📊 Обзор сообщений
- Общая статистика сообщений
- Фильтрация по чатам (рабочие, личные, каналы)
- График активности по времени

### 💬 Список сообщений  
- Просмотр всех сообщений
- Фильтрация по приоритету
- Быстрые действия (ответить, отметить важным)

### 🤖 ИИ Анализ
- Автоматический анализ важности сообщений
- Выявление сообщений, требующих ответа
- Генерация сводок и рекомендаций

### 📋 Управление задачами
- Создание задач на основе сообщений
- Автоматические уведомления
- Интеграция с системами управления задачами

## ⚙️ Настройка

1. Получите Bot Token от @BotFather в Telegram
2. Настройте переменные окружения:
```bash
TELEGRAM_BOT_TOKEN=your_bot_token
OPENAI_API_KEY=your_openai_key
```

3. Настройте фильтры чатов в боковой панели
4. Выберите период анализа

## 🚀 Запуск

```bash
cd utilities/messenger_analyzer
streamlit run app.py
```

## 🔧 Настройки

- **Период анализа** - выбор временного интервала
- **Лимит сообщений** - максимальное количество для обработки
- **Фильтр чатов** - типы чатов для мониторинга
- **Автообновление** - периодическое обновление данных

## 📊 Интеграции

- Telegram Bot API для получения сообщений
- OpenAI GPT для анализа содержимого
- Системы управления задачами для создания действий
- Уведомления о важных сообщениях