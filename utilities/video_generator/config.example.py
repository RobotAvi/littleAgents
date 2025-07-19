# ====== Настройки API ======
# Скопируйте этот файл как config.py и вставьте ваш API ключ
API_KEY = "your-api-key-here"

# ====== API URLs ======
MJ_URL = "https://gen-api.ru/api/midjourney/generate"
KL_URL = "https://gen-api.ru/api/kling-elements/generate"

# ====== Headers ======
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}