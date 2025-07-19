import requests
import os

def download_image(url, filename):
    """Скачивает изображение по URL"""
    try:
        print(f"📥 Скачивание {filename}...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"✅ Сохранен {filename}")
        return True
    except Exception as e:
        print(f"❌ Ошибка при скачивании {filename}: {e}")
        return False

def main():
    print("🖼️ Скачивание тестовых изображений...")
    
    # URL изображений из готовых запросов
    test_images = [
        {
            "url": "https://gen-api.storage.yandexcloud.net/input_files/1752894423_687b0bd7da4e8.png",
            "filename": "test_frame_01.png"
        },
        {
            "url": "https://gen-api.storage.yandexcloud.net/input_files/1752894425_687b0bd935749.png", 
            "filename": "test_frame_02.png"
        },
        {
            "url": "https://gen-api.storage.yandexcloud.net/input_files/1752894725_687b0d050e00a.png",
            "filename": "test_frame_03.png"
        },
        {
            "url": "https://gen-api.storage.yandexcloud.net/input_files/1752894726_687b0d065ebc5.png",
            "filename": "test_frame_04.png"
        }
    ]
    
    downloaded_count = 0
    for image in test_images:
        if download_image(image["url"], image["filename"]):
            downloaded_count += 1
    
    print(f"\n📊 Результат: скачано {downloaded_count}/{len(test_images)} изображений")
    
    if downloaded_count > 0:
        print("\n✅ Тестовые изображения готовы для использования в Kling API")
        print("📁 Файлы:")
        for image in test_images:
            if os.path.exists(image["filename"]):
                print(f"   - {image['filename']}")

if __name__ == "__main__":
    main()