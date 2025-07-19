import requests
import os

def upload_to_imgbb(image_path, api_key):
    """Загружает изображение на imgbb.com и возвращает URL"""
    try:
        with open(image_path, "rb") as f:
            files = {"image": f}
            data = {"key": api_key}
            
            response = requests.post("https://api.imgbb.com/1/upload", files=files, data=data)
            response.raise_for_status()
            
            result = response.json()
            if result["success"]:
                return result["data"]["url"]
            else:
                print(f"❌ Ошибка загрузки: {result}")
                return None
                
    except Exception as e:
        print(f"❌ Ошибка при загрузке: {e}")
        return None

def upload_to_temp_service(image_path):
    """Загружает изображение на временный сервис"""
    # Для демонстрации используем простой сервис
    # В реальном проекте нужно использовать ваш собственный сервис
    
    # Вариант 1: imgbb (требует API ключ)
    # imgbb_api_key = "YOUR_IMGBB_API_KEY"
    # return upload_to_imgbb(image_path, imgbb_api_key)
    
    # Вариант 2: Используем готовый URL (для тестирования)
    print(f"📤 Используем готовый URL для тестирования")
    return "https://gen-api.storage.yandexcloud.net/input_files/1752894423_687b0bd7da4e8.png"

if __name__ == "__main__":
    if os.path.exists("test_frame_01.png"):
        url = upload_to_temp_service("test_frame_01.png")
        print(f"📤 URL изображения: {url}")
    else:
        print("❌ Файл test_frame_01.png не найден")