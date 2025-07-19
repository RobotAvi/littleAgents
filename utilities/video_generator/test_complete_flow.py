import requests
import time
from config import KL_URL, RESULT_BASE_URL, HEADERS

def check_status(request_id, max_wait_time=60):
    """Проверяет статус генерации"""
    print(f"⏳ Ожидание завершения генерации (request_id: {request_id})...")
    
    start_time = time.time()
    while time.time() - start_time < max_wait_time:
        try:
            result_url = f"{RESULT_BASE_URL}/{request_id}"
            r = requests.get(result_url, headers=HEADERS, timeout=30)
            
            if r.status_code == 200:
                response_data = r.json()
                status = response_data.get('status', 'unknown')
                print(f"📊 Статус: {status}")
                
                if status == 'success':
                    print(f"✅ Генерация завершена!")
                    return response_data
                elif status == 'failed':
                    print(f"❌ Генерация не удалась")
                    return None
                elif status == 'processing':
                    print(f"🔄 Обработка... (прошло {int(time.time() - start_time)}с)")
                    time.sleep(5)
                else:
                    print(f"❓ Неизвестный статус: {response_data}")
                    time.sleep(5)
            else:
                print(f"⚠️  Ошибка при проверке статуса: {r.status_code}")
                time.sleep(5)
                
        except Exception as e:
            print(f"⚠️  Ошибка при проверке статуса: {e}")
            time.sleep(5)
    
    print(f"⏰ Превышено время ожидания ({max_wait_time}с)")
    return None

def test_video_generation():
    """Тестирует генерацию видео с тестовым изображением"""
    
    print("🎬 Тестирование генерации видео...")
    
    # Используем тестовое изображение
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
        
        if r.status_code == 200:
            response_data = r.json()
            print(f"✅ Успешный ответ: {response_data}")
            
            if "request_id" in response_data:
                request_id = response_data["request_id"]
                print(f"🆔 Получен request_id: {request_id}")
                
                # Ждем завершения генерации
                result = check_status(request_id)
                if result:
                    print(f"🎉 Видео готово!")
                    print(f"📋 Результат: {result}")
                    
                    # Извлекаем URL видео
                    if "result" in result and len(result["result"]) > 0:
                        video_url = result["result"][0]
                        print(f"🎥 URL видео: {video_url}")
                    else:
                        print(f"⚠️  URL видео не найден в результате")
                else:
                    print(f"❌ Не удалось получить результат")
            else:
                print(f"⚠️  Нет request_id в ответе")
        else:
            print(f"❌ Ошибка API: {r.status_code}")
            print(f"📄 Ответ: {r.text}")
            
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")

if __name__ == "__main__":
    test_video_generation()