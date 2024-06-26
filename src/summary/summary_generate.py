import csv
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from src.summary.VideoInfoExtractor import VideoInfoExtractor


def generate_summary_csv(url,folder):
  filename = folder+"/summary.csv"
  summary_data = get_summary_data_by_selenium(url)
  save_to_csv(summary_data,filename)

def get_summary_data_by_selenium(url):
  # Chrome 드라이버 옵션 설정
  options = webdriver.ChromeOptions()
  options.add_argument("--headless")

  # Chrome 드라이버 실행
  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
  driver.get(url)

  #description_inner 수집
  description_inner = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.ID, "description-inner"))
  )
  """
    print(description_inner.text)
    output:
       조회수 403,571회  17시간 전  #망고빙수 #빙수 #애플망고
       JOB것덜~~,,♥ 인력소장이다,,~~
    
        오늘은,, 성규가,,, …
       ...더보기
  """
  extractor = VideoInfoExtractor()
  video_name = extractor.get_video_name(driver.title)
  collection_date = extractor.get_collection_date()
  start_date = extractor.get_start_date(description_inner.text)
  hash_tag = extractor.get_hash_tag(description_inner.text)
  view_score = extractor.get_view_score(description_inner.text)

  # print(f"""
  #   video_name = {video_name}
  #   collection_date = {collection_date}
  #   start_date = {start_date}
  #   hash_tag = {hash_tag}
  #   view_score = {view_score}
  # """)

  return [video_name,collection_date,start_date,hash_tag,view_score]

def save_to_csv(summary_data, filename):
  headers = ['video_name', 'collection_date', 'start_date', 'hash_tag',"view_score"]  # 컬럼명
  file_exists = os.path.isfile(filename)

  with open(filename, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter='\\')
    if not file_exists:
      # 파일이 존재하지 않으면 컬럼명 추가
      writer.writerow(headers)
    # 데이터 추가
    writer.writerow(summary_data)


if __name__ == '__main__':
  generate_summary_csv('https://www.youtube.com/watch?v=MPf9LfHZEGs',"../")