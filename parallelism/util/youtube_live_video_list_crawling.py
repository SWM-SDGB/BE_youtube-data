from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

VIDEO_TABLE_ELEMENTS = "div[id='content'] div[class='style-scope ytd-rich-item-renderer']"
WEB_DRIVER_WAIT_TIMEOUT = 10
SCROLL_DOWN_WAIT = 1


def get_video_urls_by_selenium(channel_id):
  print("[셀레니움] 채널의 라이브영상 목록 수집 시작")
  # 백그라운드 실행 옵션 추가
  options = webdriver.ChromeOptions()
  options.add_argument("headless")

  # 크롬 드라이버 생성
  driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()),options=options)
  driver.get(url_by_channel_id(channel_id))

  # 무한 스크롤을 진행하며 크롤링
  scroll_down(driver)

  # Video url 추출
  content_elements = driver.find_elements(By.CSS_SELECTOR, VIDEO_TABLE_ELEMENTS)
  return parse_video_url(content_elements)

def url_by_channel_id(channel_id):
  return 'https://www.youtube.com/'+channel_id+'/streams'

def scroll_down(driver):

  while True:
    num_items = len(driver.find_elements(By.CSS_SELECTOR, "div[id='content'] div[class='style-scope ytd-rich-item-renderer']"))

    # Keys.END를 이용한 스크롤
    actions = driver.find_element(By.CSS_SELECTOR, 'body')
    actions.send_keys(Keys.END)

    # content가 load될 때까지 대기
    WebDriverWait(driver, WEB_DRIVER_WAIT_TIMEOUT).until(EC.presence_of_element_located((By.ID, "content")))
    time.sleep(SCROLL_DOWN_WAIT)

    # 새로운 content가 load되었는지 확인
    new_num_items = len(driver.find_elements(By.CSS_SELECTOR, VIDEO_TABLE_ELEMENTS))
    if new_num_items == num_items:
      break


def parse_video_url(content_elements):
  video_urls = []
  for content in content_elements:
    video_url = content.find_element(By.CSS_SELECTOR, "a[id='thumbnail']").get_attribute('href')
    video_urls.append(video_url)
  return video_urls
