from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import time

# Настройки браузера
options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1400,900')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Запуск браузера
service = ChromeService(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)

try:
    browser.get('http://localhost:8501/')
    time.sleep(5)  # Ждем полной загрузки страницы
    browser.save_screenshot('ui_screenshot.png')
    print('Скриншот сохранен: ui_screenshot.png')
finally:
    browser.quit()