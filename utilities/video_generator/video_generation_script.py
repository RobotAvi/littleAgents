import os
import requests
import time

# Импортируем настройки из отдельного файла
try:
    from config import API_KEY, MJ_URL, KL_URL, MJ_STATUS_URL, KL_STATUS_URL, HEADERS
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

def check_status(request_id, status_url, max_wait_time=300):
    """
    Проверяет статус генерации и ждет завершения
    """
    print(f"⏳ Ожидание завершения генерации (request_id: {request_id})...")
    
    start_time = time.time()
    while time.time() - start_time < max_wait_time:
        try:
            payload = {"request_id": request_id}
            r = requests.post(status_url, headers=HEADERS, json=payload, timeout=30)
            
            if r.status_code == 502:
                print(f"⚠️  Сервер временно недоступен (502). Повторная попытка через 10 секунд...")
                time.sleep(10)
                continue
                
            if r.status_code == 503:
                print(f"⚠️  Сервис временно недоступен (503). Повторная попытка через 15 секунд...")
                time.sleep(15)
                continue
                
            r.raise_for_status()
            response_data = r.json()
            
            print(f"📊 Статус: {response_data.get('status', 'unknown')}")
            
            if response_data.get('status') == 'completed':
                print(f"✅ Генерация завершена!")
                return response_data
            elif response_data.get('status') == 'failed':
                print(f"❌ Генерация не удалась: {response_data.get('error', 'Unknown error')}")
                return None
            elif response_data.get('status') == 'processing':
                print(f"🔄 Обработка... (прошло {int(time.time() - start_time)}с)")
                time.sleep(10)  # Ждем 10 секунд перед следующей проверкой
            else:
                print(f"❓ Неизвестный статус: {response_data}")
                time.sleep(10)
                
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Ошибка при проверке статуса: {e}")
            time.sleep(10)
    
    print(f"⏰ Превышено время ожидания ({max_wait_time}с)")
    return None

def upload_image_to_temp_service(img_file):
    """
    Загружает изображение на временный сервис и возвращает URL
    Для демонстрации используем base64 data URL
    """
    try:
        import base64
        
        with open(img_file, "rb") as f:
            img_data = f.read()
        
        # Кодируем изображение в base64
        img_base64 = base64.b64encode(img_data).decode('utf-8')
        
        # Определяем MIME тип по расширению файла
        ext = img_file.lower().split('.')[-1]
        mime_type = {
            'png': 'image/png',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'gif': 'image/gif',
            'webp': 'image/webp'
        }.get(ext, 'image/png')
        
        # Создаем data URL
        data_url = f"data:{mime_type};base64,{img_base64}"
        
        print(f"📤 Изображение закодировано в base64 data URL")
        return data_url
        
    except Exception as e:
        print(f"❌ Ошибка при загрузке изображения: {e}")
        return None

def generate_keyframe(prompt, idx):
    payload = {
        "prompt": prompt,
        "width": 1024,
        "height": 1024
    }
    
    try:
        print(f"🚀 Отправка запроса на генерацию кадра {idx+1}...")
        r = requests.post(MJ_URL, headers=HEADERS, json=payload, timeout=30)
        
        if r.status_code == 502:
            print(f"⚠️  Сервер временно недоступен (502). Повторная попытка через 10 секунд...")
            time.sleep(10)
            r = requests.post(MJ_URL, headers=HEADERS, json=payload, timeout=30)
        
        if r.status_code == 503:
            print(f"⚠️  Сервис временно недоступен (503). Повторная попытка через 15 секунд...")
            time.sleep(15)
            r = requests.post(MJ_URL, headers=HEADERS, json=payload, timeout=30)
        
        r.raise_for_status()
        response_data = r.json()
        
        # Проверяем, что получили request_id
        if "request_id" not in response_data:
            print(f"❌ Неожиданный формат ответа API: {response_data}")
            return None
        
        request_id = response_data["request_id"]
        print(f"📋 Получен request_id: {request_id}")
        
        # Ждем завершения генерации
        result = check_status(request_id, MJ_STATUS_URL)
        if not result:
            print(f"❌ Не удалось дождаться завершения генерации кадра {idx+1}")
            return None
        
        # Получаем URL изображения
        if "data" in result and len(result["data"]) > 0:
            url = result["data"][0]["url"]
        elif "url" in result:
            url = result["url"]
        else:
            print(f"❌ Неожиданный формат результата: {result}")
            return None
            
        # Скачиваем изображение
        print(f"📥 Скачивание изображения...")
        img_data = requests.get(url).content
        fname = f"frame_{idx+1:02d}.png"
        with open(fname, "wb") as f:
            f.write(img_data)
        print(f"✅ Сохранен {fname}")
        return fname
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при генерации кадра {idx+1}: {e}")
        return None

def generate_video_segment(img_file, prompt, idx):
    try:
        print(f"🚀 Отправка запроса на генерацию видео {idx+1}...")
        
        # Загружаем изображение и получаем URL
        img_url = upload_image_to_temp_service(img_file)
        if not img_url:
            print(f"❌ Не удалось загрузить изображение {img_file}")
            return None
        
        payload = {
            "prompt": prompt,
            "duration": 10,
            "input_image_urls": [img_url]
        }
        
        r = requests.post(KL_URL, headers=HEADERS, json=payload, timeout=30)
        
        if r.status_code == 502:
            print(f"⚠️  Сервер временно недоступен (502). Повторная попытка через 10 секунд...")
            time.sleep(10)
            r = requests.post(KL_URL, headers=HEADERS, json=payload, timeout=30)
        
        if r.status_code == 503:
            print(f"⚠️  Сервис временно недоступен (503). Повторная попытка через 15 секунд...")
            time.sleep(15)
            r = requests.post(KL_URL, headers=HEADERS, json=payload, timeout=30)
        
        r.raise_for_status()
        response_data = r.json()
        
        # Проверяем, что получили request_id
        if "request_id" not in response_data:
            print(f"❌ Неожиданный формат ответа API: {response_data}")
            return None
        
        request_id = response_data["request_id"]
        print(f"📋 Получен request_id: {request_id}")
        
        # Ждем завершения генерации
        result = check_status(request_id, KL_STATUS_URL)
        if not result:
            print(f"❌ Не удалось дождаться завершения генерации видео {idx+1}")
            return None
        
        # Получаем URL видео
        if "data" in result and len(result["data"]) > 0:
            url = result["data"][0]["url"]
        elif "url" in result:
            url = result["url"]
        else:
            print(f"❌ Неожиданный формат результата: {result}")
            return None
            
        # Скачиваем видео
        print(f"📥 Скачивание видео...")
        vid_data = requests.get(url).content
        vname = f"segment_{idx+1:02d}.mp4"
        with open(vname, "wb") as f:
            f.write(vid_data)
        print(f"✅ Сохранен {vname}")
        return vname
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при генерации видео {idx+1}: {e}")
        return None

def main():
    print("🚀 Запуск генерации видео с обновленными API эндпоинтами...")
    print(f"📡 Midjourney API: {MJ_URL}")
    print(f"📡 Kling API: {KL_URL}")
    print("=" * 50)
    
    image_files = []
    video_files = []

    # 1. Генерация первых двух ключевых кадров
    print("\n🎨 Генерация ключевых кадров...")
    for i, prompt in enumerate(keyframe_prompts):
        print(f"\n📸 Генерация кадра {i+1}/2...")
        fname = generate_keyframe(prompt, i)
        if fname:
            image_files.append(fname)
        else:
            print(f"❌ Не удалось сгенерировать кадр {i+1}")
        time.sleep(2)  # задержка для соблюдения rate limit

    # 2. Генерация одного видеофрагмента для первых 20 сек
    if image_files:
        print(f"\n🎬 Генерация видео из кадра {image_files[0]}...")
        video_file = generate_video_segment(image_files[0], video_prompts[0], 0)
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