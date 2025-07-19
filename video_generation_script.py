import os
import requests
import time

# ====== Настройки API ======
API_KEY = "sk-FqTcgsrIEEKcz6g8z9mkal0I6XeW7hWly8V8GuUACi5UGcdnLaoFIfz7P3Yd"
MJ_URL = "https://gen-api.ru/api/v1/generate"
KL_URL = "https://gen-api.ru/api/v1/video"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# ====== Prompts для первых 20 секунд ======

# Два ключевых кадра (00:00–00:10 и 00:10–00:20)
keyframe_prompts = [
    # [00:00–00:10]
    "cinematic, pastel color palette, retro film grain, consistent wide-angle lens 24mm, soft golden northern light of Saint Petersburg, bright and cheerful, late-80s–00s Soviet apartment, surreal dynamic, sharp focus, lively expressive faces, no temporal artifacts, characters and cat must remain identical in every frame: red-haired girl in pink 'КРУ' T-shirt, plaid shorts, colourful socks leaps at sunrise in pastel-yellow Khrushchyovka kitchen with pale-blue cabinets, worn linoleum, tall window showing brick-roofed yards and domes; creamy cake in hand; tall boy with tousled black hair, round glasses, striped pajamas slides on slipper; chubby striped cat with blue collar stretches by metal bowl; backgrounds and outfits unchanged.",
    # [00:10–00:20]
    "cinematic, pastel color palette, retro film grain, consistent wide-angle lens 24mm, soft golden northern light of Saint Petersburg, bright and cheerful, late-80s–00s Soviet apartment, surreal dynamic, sharp focus, lively expressive faces, no temporal artifacts, characters and cat must remain identical in every frame: on the same pastel-yellow kitchen table under tall window to brick courtyards and domes, boy with tousled black hair, round glasses, striped pajamas balances red ball on bare foot while holding stickered electric guitar; red-haired girl in pink 'КРУ' T-shirt and plaid shorts raises a bright-blue ladle like a microphone; chubby striped cat with blue collar leaps by fairy lights and faded cartoon posters; kitchen layout, window view, outfits, and faces unchanged."
]

# Один видеопереход (00:00–00:10 → 00:10–00:20)
video_prompts = [
    # переход из кадра 1 в кадр 2
    "cinematic, pastel color palette, retro film grain, consistent wide-angle lens 24mm, soft golden northern light of Saint Petersburg, bright and cheerful, surreal dynamic, sharp focus, lively expressive faces, no temporal artifacts, characters and cat must remain identical in every frame: cake arcs through golden kitchen light, powdered sugar sparkles, spoons and flour swirl in slow-mo, boy glides across linoleum, cat weaves between feet, red ball rolls toward guitar; all backgrounds, outfits, and facial features remain constant, window view of brick yards and cathedral silhouette present."
]

def generate_keyframe(prompt, idx):
    payload = {
        "model": "midjourney",
        "prompt": prompt,
        "width": 1024,
        "height": 1024
    }
    resp = requests.post(MJ_URL, headers=HEADERS, json=payload)
    resp.raise_for_status()
    url = resp.json()["data"][0]["url"]
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
        resp = requests.post(KL_URL, headers={"Authorization": f"Bearer {API_KEY}"}, data=data, files=files)
    resp.raise_for_status()
    url = resp.json()["url"]
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
    #    используем кадр_01.png
    video_files.append(
        generate_video_segment(image_files[0], video_prompts[0], 0)
    )

    print("Сгенерированные кадры:", image_files)
    print("Сгенерированные видео:", video_files)

if __name__ == "__main__":
    main()