# Настройка проекта

## Установка зависимостей

```bash
pip install requests pillow
```

## Настройка API ключа

1. Скопируйте файл конфигурации:
```bash
cp config.example.py config.py
```

2. Откройте `config.py` и замените `your-api-key-here` на ваш реальный API ключ:
```python
API_KEY = "sk-your-actual-api-key-here"
```

## Структура файлов

- `video_generation_script.py` - Основной скрипт для генерации видео
- `debug_script.py` - Отладочная версия с подробной информацией
- `demo_script.py` - Демонстрационная версия (работает без API)
- `config.py` - Файл с настройками API (не отслеживается в git)
- `config.example.py` - Пример конфигурации

## Запуск

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

## Безопасность

- Файл `config.py` добавлен в `.gitignore` и не будет загружен в репозиторий
- Никогда не коммитьте реальные API ключи в git
- Используйте `config.example.py` как шаблон для настройки

## Устранение неполадок

Если вы видите ошибку "Файл config.py не найден":
1. Убедитесь, что вы скопировали `config.example.py` в `config.py`
2. Проверьте, что в `config.py` указан правильный API ключ
3. Убедитесь, что файл находится в той же папке, что и скрипты