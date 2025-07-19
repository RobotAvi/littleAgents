import requests
import json

# ====== Настройки API ======
API_KEY = "sk-FqTcgsrIEEKcz6g8z9mkal0I6XeW7hWly8V8GuUACi5UGcdnLaoFIfz7P3Yd"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Тестируем различные эндпоинты
endpoints = [
    "https://gen-api.ru/api/midjourney/generate",
    "https://gen-api.ru/api/kling-elements/generate",
    "https://gen-api.ru/api/v1/generate",
    "https://gen-api.ru/api/v2/generate",
    "https://gen-api.ru/api/generate",
    "https://gen-api.ru/api/midjourney",
    "https://gen-api.ru/api/kling-elements"
]

def test_endpoint(url):
    print(f"\nТестируем: {url}")
    try:
        # Сначала проверим GET запрос
        r = requests.get(url, headers=HEADERS)
        print(f"GET {url}: {r.status_code}")
        if r.status_code == 200:
            print(f"Ответ: {r.text[:200]}...")
        
        # Затем проверим POST запрос
        payload = {"model": "midjourney", "prompt": "test", "width": 1024, "height": 1024}
        r = requests.post(url, headers=HEADERS, json=payload)
        print(f"POST {url}: {r.status_code}")
        if r.status_code != 404:
            print(f"Ответ: {r.text[:200]}...")
            
    except Exception as e:
        print(f"Ошибка: {e}")

def main():
    print("Тестирование API эндпоинтов GenAPI...")
    
    for endpoint in endpoints:
        test_endpoint(endpoint)
    
    # Также проверим базовый домен
    print(f"\nПроверяем базовый домен...")
    try:
        r = requests.get("https://gen-api.ru/")
        print(f"GET https://gen-api.ru/: {r.status_code}")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()