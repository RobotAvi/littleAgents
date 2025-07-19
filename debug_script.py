import os
import requests
import time
import json

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

def test_api_connection():
    """Тестирует подключение к API"""
    print("=== ТЕСТИРОВАНИЕ API ПОДКЛЮЧЕНИЯ ===")
    
    # Тест 1: Проверка базового домена
    try:
        r = requests.get("https://gen-api.ru/", timeout=10)
        print(f"✓ Базовый домен доступен: {r.status_code}")
    except Exception as e:
        print(f"✗ Ошибка доступа к базовому домену: {e}")
        return False
    
    # Тест 2: Проверка Midjourney API
    try:
        payload = {
            "model": "midjourney",
            "prompt": "test",
            "width": 1024,
            "height": 1024
        }
        print(f"Отправляем запрос к: {MJ_URL}")
        print(f"Заголовки: {HEADERS}")
        print(f"Данные: {json.dumps(payload, indent=2)}")
        
        r = requests.post(MJ_URL, headers=HEADERS, json=payload, timeout=30)
        print(f"Статус ответа: {r.status_code}")
        print(f"Заголовки ответа: {dict(r.headers)}")
        print(f"Тело ответа: {r.text[:500]}...")
        
        if r.status_code == 200:
            print("✓ Midjourney API работает!")
            return True
        else:
            print(f"✗ Midjourney API вернул ошибку: {r.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Ошибка сети при обращении к Midjourney API: {e}")
        return False
    except Exception as e:
        print(f"✗ Неожиданная ошибка: {e}")
        return False

def generate_keyframe(prompt, idx):
    """Генерирует ключевой кадр"""
    print(f"\n=== ГЕНЕРАЦИЯ КАДРА {idx+1} ===")
    
    payload = {
        "model": "midjourney",
        "prompt": prompt,
        "width": 1024,
        "height": 1024
    }
    
    try:
        print(f"Отправляем запрос к: {MJ_URL}")
        r = requests.post(MJ_URL, headers=HEADERS, json=payload, timeout=60)
        
        print(f"Статус: {r.status_code}")
        if r.status_code != 200:
            print(f"Ошибка: {r.text}")
            return None
            
        response_data = r.json()
        print(f"Ответ API: {json.dumps(response_data, indent=2)}")
        
        url = response_data["data"][0]["url"]
        fname = f"frame_{idx+1:02d}.png"
        
        print(f"Загружаем изображение с: {url}")
        img_data = requests.get(url, timeout=30).content
        
        with open(fname, "wb") as f:
            f.write(img_data)
        print(f"✓ Сохранено: {fname}")
        return fname
        
    except Exception as e:
        print(f"✗ Ошибка при генерации кадра: {e}")
        return None

def generate_video_segment(img_file, prompt, idx):
    """Генерирует видео сегмент"""
    print(f"\n=== ГЕНЕРАЦИЯ ВИДЕО СЕГМЕНТА {idx+1} ===")
    
    try:
        with open(img_file, "rb") as f:
            files = {"file": f}
            data = {"model": "kling-elements", "prompt": prompt, "duration": 10}
            
            print(f"Отправляем запрос к: {KL_URL}")
            print(f"Файл: {img_file}")
            print(f"Данные: {data}")
            
            r = requests.post(KL_URL, headers={"Authorization": f"Bearer {API_KEY}"}, data=data, files=files, timeout=120)
            
            print(f"Статус: {r.status_code}")
            if r.status_code != 200:
                print(f"Ошибка: {r.text}")
                return None
                
            response_data = r.json()
            print(f"Ответ API: {json.dumps(response_data, indent=2)}")
            
            url = response_data["url"]
            vname = f"segment_{idx+1:02d}.mp4"
            
            print(f"Загружаем видео с: {url}")
            vid_data = requests.get(url, timeout=60).content
            
            with open(vname, "wb") as f:
                f.write(vid_data)
            print(f"✓ Сохранено: {vname}")
            return vname
            
    except Exception as e:
        print(f"✗ Ошибка при генерации видео: {e}")
        return None

def main():
    print("=== ЗАПУСК ОТЛАДОЧНОГО СКРИПТА ===")
    
    # Сначала тестируем подключение
    if not test_api_connection():
        print("\n❌ API недоступен. Проверьте:")
        print("1. Правильность API ключа")
        print("2. Доступность сервиса")
        print("3. Правильность эндпоинтов")
        return
    
    image_files = []
    video_files = []

    # 1. Генерация первых двух ключевых кадров
    print("\n=== ГЕНЕРАЦИЯ КЛЮЧЕВЫХ КАДРОВ ===")
    for i, prompt in enumerate(keyframe_prompts):
        fname = generate_keyframe(prompt, i)
        if fname:
            image_files.append(fname)
        else:
            print(f"❌ Не удалось создать кадр {i+1}")
            return
        time.sleep(2)

    # 2. Генерация одного видеофрагмента для первых 20 сек
    print("\n=== ГЕНЕРАЦИЯ ВИДЕО СЕГМЕНТА ===")
    video_file = generate_video_segment(image_files[0], video_prompts[0], 0)
    if video_file:
        video_files.append(video_file)
    else:
        print("❌ Не удалось создать видео сегмент")
        return

    print("\n=== РЕЗУЛЬТАТЫ ===")
    print("Сгенерированные кадры:", image_files)
    print("Сгенерированные видео:", video_files)

if __name__ == "__main__":
    main()