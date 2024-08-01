from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from PIL import Image
import os
import io

# ChromeDriver 경로 설정
CHROMEDRIVER_PATH = './chromedriver.exe'

# 이미지 저장 경로 설정
DOWNLOAD_DIR = './images'
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--headless")  # 브라우저를 백그라운드에서 실행
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36") # 사용자 에이전트 설정

# WebDriver 초기화
print("WebDriver 초기화 중...")
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)
print("WebDriver 초기화 성공")

def download_images(url):
    print(f"URL에 접근 중: {url}")
    # 웹 페이지 열기
    driver.get(url)
    print("페이지 접근 성공")
    
    # 페이지 로딩 대기
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'img')))
    print("페이지 접근 및 로딩 성공")
    
    # 이미지 요소 찾기
    images = driver.find_elements(By.TAG_NAME, 'img')
    print(f"이미지 {len(images)}개 발견")
    
    # 이미지 다운로드 및 저장
    for img in images:
        img_url = img.get_attribute('src')
        if img_url:
            try:
                print(f"이미지 다운로드 중: {img_url}")
                response = requests.get(img_url)
                image = Image.open(io.BytesIO(response.content))
                
                # URL에서 파일명 추출
                img_filename = os.path.join(DOWNLOAD_DIR, os.path.basename(img_url))
                
                # 이미지 저장
                image.save(img_filename, 'PNG')
                
                print(f"다운로드 완료: {img_filename}")
            except Exception as e:
                print(f"다운로드 실패: {img_url}: {e}")

# 이미지 변환 함수
def convert_images_to_jpeg(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.png'):
            png_image = Image.open(os.path.join(directory, filename))
            if png_image.mode in ('RGBA', 'LA') or (png_image.mode == 'P' and 'transparency' in png_image.info):
                png_image = png_image.convert('RGB')
            jpeg_filename = os.path.splitext(filename)[0] + '.jpg'
            png_image.save(os.path.join(directory, jpeg_filename), 'JPEG', quality=95)
            print(f"{filename}에서 {jpeg_filename}으로 변환 완료")

# 스크립트 실행
print("스크립트 실행 시작...")
URL = 'https://www.ubisoft.com/en-gb/game/rainbow-six/siege/game-info/operators'  # 이미지가 있는 웹 페이지 URL
download_images(URL)
convert_images_to_jpeg(DOWNLOAD_DIR)
print("스크립트 종료, 다운로드 및 변환 완료")

# WebDriver 종료
driver.quit()
print("WebDriver 종료")
