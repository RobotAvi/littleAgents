import os
import time
import base64
from PIL import Image, ImageDraw, ImageFont
import io

# ====== Демонстрационные настройки ======
print("=== ДЕМОНСТРАЦИОННАЯ ВЕРСИЯ СКРИПТА ===")
print("Создаем тестовые изображения и видео файлы для демонстрации логики")

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

def create_demo_image(prompt, idx):
    """Создает демонстрационное изображение с текстом промпта"""
    print(f"Создаем изображение {idx+1} с промптом: {prompt[:100]}...")
    
    # Создаем изображение 1024x1024
    img = Image.new('RGB', (1024, 1024), color='#FFE5B4')  # Пастельный желтый
    draw = ImageDraw.Draw(img)
    
    # Добавляем текст
    try:
        # Пытаемся использовать системный шрифт
        font = ImageFont.load_default()
    except:
        font = None
    
    # Рисуем рамку
    draw.rectangle([50, 50, 974, 974], outline='#FF6B6B', width=5)
    
    # Добавляем заголовок
    title = f"Демо кадр {idx+1:02d}"
    draw.text((100, 100), title, fill='#4A90E2', font=font)
    
    # Добавляем промпт (обрезанный)
    prompt_short = prompt[:200] + "..." if len(prompt) > 200 else prompt
    lines = [prompt_short[i:i+80] for i in range(0, len(prompt_short), 80)]
    
    y_pos = 200
    for line in lines[:10]:  # Максимум 10 строк
        draw.text((100, y_pos), line, fill='#333333', font=font)
        y_pos += 30
    
    # Добавляем информацию о времени
    time_info = f"Время: {idx*10:02d}:00-{(idx+1)*10:02d}:00"
    draw.text((100, 900), time_info, fill='#FF6B6B', font=font)
    
    fname = f"frame_{idx+1:02d}.png"
    img.save(fname)
    print(f"Сохранено: {fname}")
    return fname

def create_demo_video(img_file, prompt, idx):
    """Создает демонстрационный видео файл (на самом деле копию изображения)"""
    print(f"Создаем видео сегмент {idx+1} с промптом: {prompt[:100]}...")
    
    # В реальности здесь был бы код для создания видео
    # Для демонстрации просто копируем изображение
    import shutil
    vname = f"segment_{idx+1:02d}.mp4"
    
    # Создаем текстовый файл с информацией о видео
    with open(vname.replace('.mp4', '.txt'), 'w', encoding='utf-8') as f:
        f.write(f"Демонстрационный видео сегмент {idx+1}\n")
        f.write(f"Исходное изображение: {img_file}\n")
        f.write(f"Промпт: {prompt}\n")
        f.write(f"Длительность: 10 секунд\n")
        f.write(f"В реальности здесь был бы MP4 файл\n")
    
    print(f"Сохранено: {vname.replace('.mp4', '.txt')} (демо)")
    return vname

def main():
    print("=== ЗАПУСК ДЕМОНСТРАЦИОННОГО СКРИПТА ===")
    print("Этот скрипт демонстрирует логику работы без реальных API вызовов")
    
    image_files = []
    video_files = []

    # 1. Генерация первых двух ключевых кадров
    print("\n1. Генерация ключевых кадров...")
    for i, prompt in enumerate(keyframe_prompts):
        fname = create_demo_image(prompt, i)
        image_files.append(fname)
        time.sleep(1)  # Имитация задержки

    # 2. Генерация одного видеофрагмента для первых 20 сек
    print("\n2. Генерация видео сегмента...")
    video_files.append(
        create_demo_video(image_files[0], video_prompts[0], 0)
    )

    print("\n=== РЕЗУЛЬТАТЫ ===")
    print("Сгенерированные кадры:", image_files)
    print("Сгенерированные видео:", video_files)
    
    print("\n=== СТРУКТУРА ПРОЕКТА ===")
    print("frame_01.png - Первый ключевой кадр (00:00-00:10)")
    print("frame_02.png - Второй ключевой кадр (00:10-00:20)")
    print("segment_01.txt - Информация о видео сегменте")
    
    print("\n=== СЛЕДУЮЩИЕ ШАГИ ===")
    print("1. Проверьте правильность API эндпоинтов")
    print("2. Убедитесь в валидности API ключа")
    print("3. Проверьте документацию GenAPI")
    print("4. Замените демо функции на реальные API вызовы")

if __name__ == "__main__":
    main()