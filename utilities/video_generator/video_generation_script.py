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

def generate_keyframe(prompt, idx):
    payload = {
        "model": "midjourney",
        "prompt": prompt,
        "width": 1024,
        "height": 1024
    }
    r = requests.post(MJ_URL, headers=HEADERS, json=payload)
    r.raise_for_status()
    url = r.json()["data"][0]["url"]
    fname = f"frame_{idx+1:02d}.png"
    img_data = requests.get(url).content
    with open(fname, "wb") as f:
        f.write(img_data)
    print(f"Saved {fname}")
    return fname

def generate_video_segment(img_file, prompt, idx):
    with open(img_file, "rb") as f:
        files = {"file": f}
        data = {"model": "kling-elements", "prompt": prompt, "duration": 10}
        r = requests.post(KL_URL, headers={"Authorization": f"Bearer {API_KEY}"}, data=data, files=files)
    r.raise_for_status()
    url = r.json()["url"]
    vname = f"segment_{idx+1:02d}.mp4"
    vid_data = requests.get(url).content
    with open(vname, "wb") as f:
        f.write(vid_data)
    print(f"Saved {vname}")
    return vname

def main():
    image_files = []
    video_files = []

    # 1. Генерация первых двух ключевых кадров
    for i, prompt in enumerate(keyframe_prompts):
        fname = generate_keyframe(prompt, i)
        image_files.append(fname)
        time.sleep(2)  # задержка для соблюдения rate limit

    # 2. Генерация одного видеофрагмента для первых 20 сек
    video_files.append(
        generate_video_segment(image_files[0], video_prompts[0], 0)
    )

    print("Сгенерированные кадры:", image_files)
    print("Сгенерированные видео:", video_files)

if __name__ == "__main__":
    main()