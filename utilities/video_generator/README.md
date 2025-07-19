# Video Generator

Утилита для генерации видео с использованием AI API (Midjourney + Kling Elements).

## Описание

Эта утилита создает видео контент путем:
1. Генерации ключевых кадров с помощью Midjourney API
2. Создания видео сегментов с помощью Kling Elements API
3. Объединения в финальное видео

## Файлы

- `video_generation_script.py` - Основной скрипт генерации
- `debug_script.py` - Отладочная версия с подробной информацией
- `demo_script.py` - Демонстрационная версия (работает без API)
- `test_api.py` - Тестирование API эндпоинтов
- `config.py` - Настройки API (не отслеживается git)
- `config.example.py` - Шаблон конфигурации
- `SETUP.md` - Инструкция по настройке
- `SECURITY.md` - Документация по безопасности

## Установка

1. Установите зависимости:
```bash
pip install requests pillow
```

2. Настройте API ключ:
```bash
cp config.example.py config.py
# Отредактируйте config.py и вставьте ваш API ключ
```

## Использование

### Основной скрипт
```bash
python3 video_generation_script.py
```

### Отладочная версия
```bash
python3 debug_script.py
```

### Демонстрационная версия
```bash
python3 demo_script.py
```

### Тестирование API
```bash
python3 test_api.py
```

## Конфигурация

Скопируйте `config.example.py` в `config.py` и настройте:
- `API_KEY` - ваш API ключ для GenAPI
- `MJ_URL` - эндпоинт для Midjourney
- `KL_URL` - эндпоинт для Kling Elements

## Безопасность

- Файл `config.py` добавлен в `.gitignore`
- API ключи не хранятся в исходном коде
- Безопасно для публикации в репозитории

## Требования

- Python 3.7+
- requests
- Pillow (PIL)
- Доступ к GenAPI сервису

## Статус

- ✅ Логика скрипта готова
- ✅ Безопасность настроена
- ⚠️ API сервис временно недоступен
- 🔄 Готов к работе при восстановлении API