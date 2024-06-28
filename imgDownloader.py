from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
from PIL import Image
import os
import io

# ChromeDriver 경로 설정
CHROMEDRIVER_PATH = './chromedriver.exe'

# 이미지 저장 경로 설정
DOWNLOAD_DIR = './images'

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--headless")  # 브라우저를 백그라운드에서 실행

# WebDriver 초기화
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

def download_images(url):
    # 웹 페이지 열기
    driver.get(url)
    
    # 이미지 요소 찾기
    images = driver.find_elements(By.TAG_NAME, 'img')
    
    # 이미지 다운로드 및 저장
    for img in images:
        img_url = img.get_attribute('src')
        if img_url:
            try:
                response = requests.get(img_url)
                image = Image.open(io.BytesIO(response.content))
                
                # URL에서 파일명 추출
                img_filename = os.path.join(DOWNLOAD_DIR, os.path.basename(img_url))
                
                # 이미지 저장
                image.save(img_filename, 'PNG')
                
                print(f"Downloaded {img_filename}")
            except Exception as e:
                print(f"Failed to download {img_url}: {e}")

# 이미지 변환 함수
def convert_images_to_jpeg(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.png'):
            png_image = Image.open(os.path.join(directory, filename))
            if png_image.mode in ('RGBA', 'LA') or (png_image.mode == 'P' and 'transparency' in png_image.info):
                png_image = png_image.convert('RGB')
            jpeg_filename = os.path.splitext(filename)[0] + '.jpg'
            png_image.save(os.path.join(directory, jpeg_filename), 'JPEG', quality=95)
            print(f"Converted {filename} to {jpeg_filename}")

# 스크립트 실행
URL = 'https://www.ubisoft.com/en-gb/game/rainbow-six/siege/game-info/operators'  # 이미지가 있는 웹 페이지 URL
download_images(URL)
convert_images_to_jpeg(DOWNLOAD_DIR)

# WebDriver 종료
driver.quit()
