import csv
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import re

def get_video_name(driver):
  video_name = driver.title.split('-')[0]
  print(video_name)
  return video_name

def get_collection_date():
  now = datetime.now()
  return now.strftime("%Y/%m/%d")

def get_view_score(description_inner_text):
  pattern = r'조회수 (\d{1,3}(,\d{3})*)회'
  match = re.search(pattern, description_inner_text)
  if match:
    # 첫 번째 그룹 (조회수 숫자)
    views = match.group(1)
    return views
  else:
    print("조회수를 찾을 수 없습니다.")
    return

def convert_datetime(time, unit):
  now = datetime.now()
  if unit == '초':
    past_time = now - timedelta(seconds=time)
  elif unit == '분':
    past_time = now - timedelta(minutes=time)
  elif unit == '시간':
    past_time = now - timedelta(hours=time)
  elif unit == '일':
    past_time = now - timedelta(days=time)
  elif unit == '주':
    past_time = now - timedelta(weeks=time)
  elif unit == '개월':
    past_time = now.replace(month=now.month - time if now.month > time else 12 + now.month - time)
  elif unit == '년':
    past_time = now.replace(year=now.year - time)

  return past_time.strftime('%Y/%m/%d')

def get_start_date(description_inner_text): # return ex) "2024/06/21"
  pattern = r'(\d+)\s*(초|분|시간|일|주|개월|년)\s*전'
  match = re.search(pattern, description_inner_text)
  if match:
   time = int(match.group(1)) # 시간 숫자값
   unit = match.group(2) # 시간 단위
   return convert_datetime(time, unit)
  else:
    print("조회수를 찾을 수 없습니다.")
    return

def get_hash_tag(description_inner_text):
  hashtag_pattern = re.compile(r'#\S+')
  hashtags = hashtag_pattern.findall(description_inner_text)
  return ''.join(hashtags)

def generate_summary_csv(url):
  summary_data = summary_collect_data(url)
  save_to_csv(summary_data[0],summary_data[1],summary_data[2],summary_data[3],"output.csv")

def save_to_csv(str1, str2, str3, str4, filename):
  # 데이터 준비
  data = [['video_name', 'collection_date', 'start_date', 'hash_tag'],  # 컬럼명
          [str1, str2, str3, str4]]  # 데이터

  # CSV 파일 작성
  with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file,delimiter="\\")
    writer.writerows(data)

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

if __name__ == '__main__':
  generate_summary_csv('https://www.youtube.com/watch?v=MPf9LfHZEGs')