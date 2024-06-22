import csv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from parallelism.summary.collectdata.collection_date import get_collection_date
from parallelism.summary.collectdata.hash_tag import get_hash_tag
from parallelism.summary.collectdata.start_date import get_start_date
from parallelism.summary.collectdata.video_name import get_video_name


def generate_summary_csv(url,filename):
  summary_data = summary_collect_data(url)
  save_to_csv(summary_data[0], summary_data[1], summary_data[2], summary_data[3],
              filename)

  print(f"데이터가 {filename} 파일로 저장되었습니다.")

def summary_collect_data(url):
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

  video_name = get_video_name(driver)
  collection_date = get_collection_date()
  start_date = get_start_date(description_inner.text)
  hash_tag = get_hash_tag(description_inner.text)

  print(f"""
    video_name = {video_name}
    collection_date = {collection_date}
    start_date = {start_date}
    hash_tag = {hash_tag}
  """)

  return [video_name,collection_date,start_date,hash_tag]

def save_to_csv(str1, str2, str3, str4, filename):
  # 데이터 준비
  data = [['video_name', 'collection_date', 'start_date', 'hash_tag'],  # 컬럼명
          [str1, str2, str3, str4]]  # 데이터

  # CSV 파일 작성
  with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file,delimiter="\\")
    writer.writerows(data)


if __name__ == '__main__':
  generate_summary_csv('https://www.youtube.com/watch?v=MPf9LfHZEGs',"outputs.csv")