import requests
import json

# Импортируем настройки из отдельного файла
try:
    from config import API_KEY, HEADERS
except ImportError:
    print("Ошибка: Файл config.py не найден!")
    print("Скопируйте config.example.py в config.py и вставьте ваш API ключ")
    exit(1)

# Тестируем различные эндпоинты
endpoints = [
    "https://api.gen-api.ru/api/v1/networks/midjourney",
    "https://api.gen-api.ru/api/v1/networks/kling-elements",
    "https://gen-api.ru/api/midjourney/generate",
    "https://gen-api.ru/api/kling-elements/generate"
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
        payload = {"prompt": "test", "width": 1024, "height": 1024}
        r = requests.post(url, headers=HEADERS, json=payload)
        print(f"POST {url}: {r.status_code}")
        if r.status_code not in [404, 502, 503]:
            print(f"Ответ: {r.text[:200]}...")
        elif r.status_code in [502, 503]:
            print(f"⚠️  Сервис временно недоступен ({r.status_code})")
            
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