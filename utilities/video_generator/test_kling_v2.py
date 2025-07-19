import requests
import base64
from config import KL_URL, RESULT_BASE_URL, HEADERS

def test_kling_v2_api():
    """Тестирует Kling v2 API с правильным эндпоинтом"""
    
    print("🧪 Тестирование Kling v2 API...")
    
    # Используем готовый URL изображения для тестирования
    img_url = "https://gen-api.storage.yandexcloud.net/input_files/1752894423_687b0bd7da4e8.png"
    
    payload = {
        "prompt": "все танцуют",
        "model": "standard", 
        "image_url": img_url
    }
    
    print(f"📤 Отправка запроса на {KL_URL}")
    print(f"📋 Payload: {payload}")
    
    try:
        r = requests.post(KL_URL, headers=HEADERS, json=payload, timeout=30)
        
        print(f"📊 Статус ответа: {r.status_code}")
        print(f"📄 Заголовки: {dict(r.headers)}")
        
        if r.status_code == 200:
            response_data = r.json()
            print(f"✅ Успешный ответ: {response_data}")
            
            if "request_id" in response_data:
                request_id = response_data["request_id"]
                print(f"🆔 Получен request_id: {request_id}")
                
                # Проверяем статус
                print(f"\n🔍 Проверка статуса для request_id: {request_id}")
                status_url = f"{RESULT_BASE_URL}/{request_id}"
                print(f"📡 URL статуса: {status_url}")
                
                status_r = requests.get(status_url, headers=HEADERS, timeout=30)
                print(f"📊 Статус проверки: {status_r.status_code}")
                
                if status_r.status_code == 200:
                    status_data = status_r.json()
                    print(f"📋 Данные статуса: {status_data}")
                else:
                    print(f"❌ Ошибка при проверке статуса: {status_r.text}")
            else:
                print(f"⚠️  Нет request_id в ответе")
        else:
            print(f"❌ Ошибка API: {r.status_code}")
            print(f"📄 Ответ: {r.text}")
            
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")

if __name__ == "__main__":
    test_kling_v2_api()