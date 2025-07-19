import os
import requests
import time

# Импортируем настройки из отдельного файла
try:
    from config import API_KEY, MJ_URL, KL_URL, HEADERS
except ImportError:
    print("Ошибка: Файл config.py не найден!")
    print("Скопируйте config.example.py в config.py и вставьте ваш API ключ")
    exit(1)

# ====== Prompts для первых 20 секунд ======

keyframe_prompts = [
    # [00:00–00:10]
    "cinematic, pastel color palette, retro film grain, consistent wide-angle lens 24mm, soft golden northern light of Saint Petersburg, bright and cheerful, late-80s–00s Soviet apartment, surreal dynamic, sharp focus, lively expressive faces, no temporal artifacts, characters and cat must remain identical in every frame: red-haired girl in pink 'КРУ' T-shirt, plaid shorts, colourful socks leaps at sunrise in pastel-yellow Khrushchyovka kitchen with pale-blue cabinets, worn linoleum, tall window showing brick-roofed yards and domes; creamy cake in hand; tall boy with tousled black hair, round glasses, striped pajamas slides on slipper; chubby striped cat with blue collar stretches by metal bowl; backgrounds and outfits unchanged.",
    # [00:10–00:20]
    "cinematic, pastel color palette, retro film grain, consistent wide-angle lens 24mm, soft golden northern light of Saint Petersburg, bright and cheerful, late-80s–00s Soviet apartment, surreal dynamic, sharp focus, lively expressive faces, no temporal artifacts, characters and cat must remain identical in every frame: on the same pastel-yellow kitchen table under tall window to brick courtyards and domes, boy with tousled black hair, round glasses, striped pajamas balances red ball on bare foot while holding stickered electric guitar; red-haired girl in pink 'КРУ' T-shirt and plaid shorts raises a bright-blue ladle like a microphone; chubby striped cat with blue collar leaps by fairy lights and faded cartoon posters; kitchen layout, window view, outfits, and faces unchanged."
]

video_prompts = [
    # переход из кадра 1 в кадр 2 (00:00–00:10 → 00:10–00:20)
    "cinematic, pastel color palette, retro film grain, consistent wide-angle lens 24mm, soft golden northern light of Saint Petersburg, bright and cheerful, surreal dynamic, sharp focus, lively expressive faces, no temporal artifacts, characters and cat must remain identical in every frame: cake arcs through golden kitchen light, powdered sugar sparkles, spoons and flour swirl in slow-mo, boy glides across linoleum, cat weaves between feet, red ball rolls toward guitar; all backgrounds, outfits, and facial features remain constant, window view of brick yards and cathedral silhouette present."
]

def generate_keyframe_simple(prompt, idx, max_wait_time=300):
    """
    Генерирует кадр с длительным ожиданием в одном запросе
    """
    payload = {
        "prompt": prompt,
        "width": 1024,
        "height": 1024
    }
    
    try:
        print(f"🚀 Отправка запроса на генерацию кадра {idx+1}...")
        print(f"⏳ Ожидание результата (максимум {max_wait_time}с)...")
        
        # Отправляем запрос с длительным таймаутом
        r = requests.post(MJ_URL, headers=HEADERS, json=payload, timeout=max_wait_time)
        
        if r.status_code == 502:
            print(f"⚠️  Сервер временно недоступен (502). Повторная попытка через 10 секунд...")
            time.sleep(10)
            r = requests.post(MJ_URL, headers=HEADERS, json=payload, timeout=max_wait_time)
        
        if r.status_code == 503:
            print(f"⚠️  Сервис временно недоступен (503). Повторная попытка через 15 секунд...")
            time.sleep(15)
            r = requests.post(MJ_URL, headers=HEADERS, json=payload, timeout=max_wait_time)
        
        r.raise_for_status()
        response_data = r.json()
        
        print(f"📊 Получен ответ: {response_data}")
        
        # Проверяем, что получили URL изображения
        if "data" in response_data and len(response_data["data"]) > 0:
            url = response_data["data"][0]["url"]
        elif "url" in response_data:
            url = response_data["url"]
        elif "request_id" in response_data:
            print(f"📋 Получен request_id: {response_data['request_id']}")
            print(f"⚠️  API работает асинхронно, но эндпоинт статуса недоступен")
            return None
        else:
            print(f"❌ Неожиданный формат ответа API: {response_data}")
            return None
            
        # Скачиваем изображение
        print(f"📥 Скачивание изображения...")
        img_data = requests.get(url).content
        fname = f"frame_{idx+1:02d}.png"
        with open(fname, "wb") as f:
            f.write(img_data)
        print(f"✅ Сохранен {fname}")
        return fname
        
    except requests.exceptions.Timeout:
        print(f"⏰ Превышено время ожидания ({max_wait_time}с)")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при генерации кадра {idx+1}: {e}")
        return None

def generate_video_segment_simple(img_file, prompt, idx, max_wait_time=300):
    """
    Генерирует видео с длительным ожиданием в одном запросе
    """
    try:
        print(f"🚀 Отправка запроса на генерацию видео {idx+1}...")
        
        # Используем реальные URL изображений с Yandex Cloud Storage
        image_urls = [
            "https://gen-api.storage.yandexcloud.net/input_files/1752891001_687afe790d46c.png",
            "https://gen-api.storage.yandexcloud.net/input_files/1752891002_687afe7a59119.png",
            "https://gen-api.storage.yandexcloud.net/input_files/1752891003_687afe7b824a3.png",
            "https://gen-api.storage.yandexcloud.net/input_files/1752891004_687afe7ccc0fe.png"
        ]
        
        # Используем изображение по индексу
        img_url = image_urls[idx % len(image_urls)]
        print(f"📸 Используем изображение: {img_url}")
        
        payload = {
            "prompt": prompt,
            "duration": 10,
            "input_image_urls": [img_url]
        }
        
        print(f"⏳ Ожидание результата (максимум {max_wait_time}с)...")
        
        # Отправляем запрос с длительным таймаутом
        r = requests.post(KL_URL, headers=HEADERS, json=payload, timeout=max_wait_time)
        
        if r.status_code == 502:
            print(f"⚠️  Сервер временно недоступен (502). Повторная попытка через 10 секунд...")
            time.sleep(10)
            r = requests.post(KL_URL, headers=HEADERS, json=payload, timeout=max_wait_time)
        
        if r.status_code == 503:
            print(f"⚠️  Сервис временно недоступен (503). Повторная попытка через 15 секунд...")
            time.sleep(15)
            r = requests.post(KL_URL, headers=HEADERS, json=payload, timeout=max_wait_time)
        
        r.raise_for_status()
        response_data = r.json()
        
        print(f"📊 Получен ответ: {response_data}")
        
        # Проверяем, что получили URL видео
        if "data" in response_data and len(response_data["data"]) > 0:
            url = response_data["data"][0]["url"]
        elif "url" in response_data:
            url = response_data["url"]
        elif "request_id" in response_data:
            print(f"📋 Получен request_id: {response_data['request_id']}")
            print(f"⚠️  API работает асинхронно, но эндпоинт статуса недоступен")
            return None
        else:
            print(f"❌ Неожиданный формат ответа API: {response_data}")
            return None
            
        # Скачиваем видео
        print(f"📥 Скачивание видео...")
        vid_data = requests.get(url).content
        vname = f"segment_{idx+1:02d}.mp4"
        with open(vname, "wb") as f:
            f.write(vid_data)
        print(f"✅ Сохранен {vname}")
        return vname
        
    except requests.exceptions.Timeout:
        print(f"⏰ Превышено время ожидания ({max_wait_time}с)")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при генерации видео {idx+1}: {e}")
        return None

def main():
    print("🚀 Запуск упрощенной генерации видео...")
    print(f"📡 Midjourney API: {MJ_URL}")
    print(f"📡 Kling API: {KL_URL}")
    print("=" * 50)
    
    image_files = []
    video_files = []

    # 1. Генерация первых двух ключевых кадров
    print("\n🎨 Генерация ключевых кадров...")
    for i, prompt in enumerate(keyframe_prompts):
        print(f"\n📸 Генерация кадра {i+1}/2...")
        fname = generate_keyframe_simple(prompt, i, max_wait_time=120)  # 2 минуты на кадр
        if fname:
            image_files.append(fname)
        else:
            print(f"❌ Не удалось сгенерировать кадр {i+1}")
        time.sleep(2)  # задержка для соблюдения rate limit

    # 2. Генерация одного видеофрагмента для первых 20 сек
    if image_files:
        print(f"\n🎬 Генерация видео из кадра {image_files[0]}...")
        video_file = generate_video_segment_simple(image_files[0], video_prompts[0], 0, max_wait_time=180)  # 3 минуты на видео
        if video_file:
            video_files.append(video_file)
        else:
            print("❌ Не удалось сгенерировать видео")
    else:
        print("❌ Нет изображений для генерации видео")

    print("\n" + "=" * 50)
    print("📊 Результаты:")
    print(f"✅ Сгенерированные кадры: {len(image_files)}")
    print(f"✅ Сгенерированные видео: {len(video_files)}")
    
    if image_files:
        print(f"📁 Кадры: {image_files}")
    if video_files:
        print(f"📁 Видео: {video_files}")

if __name__ == "__main__":
    main()