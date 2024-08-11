import csv
import os

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
from parallelism.summary.collectdata.view_score import get_view_score


def generate_summary_csv(url,folder):
  filename = folder+"/summary.csv"
  summary_data = summary_collect_data(url)
  save_to_csv(summary_data,filename)

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
  view_score = get_view_score(description_inner.text)

  # print(f"""
  #   video_name = {video_name}
  #   collection_date = {collection_date}
  #   start_date = {start_date}
  #   hash_tag = {hash_tag}
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


# if __name__ == '__main__':
#   generate_summary_csv('https://www.youtube.com/watch?v=MPf9LfHZEGs',"../")

# 동시성 문제를 유발할 함수
def thread_task(filename, thread_id):
  for i in range(100):
    summary_data = [f'video_{thread_id}_{i}', '2024-08-11', '2024-08-10', f'#tag{thread_id}', i]
    with SystemMutex('critical-section'):
      save_to_csv(summary_data, filename)
# mutex task
def thread_safe_task(filename, thread_id):
  for i in range(100):
    summary_data = [f'video_{thread_id}_{i}', '2024-08-11', '2024-08-10', f'#tag{thread_id}', i]
    with SystemMutex('critical-section'):
      save_to_csv(summary_data, filename)

# 메인 실행 코드
if __name__ == "__main__":
  filename = 'output.csv'

  # 기존 파일 삭제 (실행 시마다 새로운 파일 생성)
  if os.path.exists(filename):
    os.remove(filename)

  # 10개의 쓰레드를 생성하여 동시에 save_to_csv 호출
  threads = []
  for thread_id in range(10):
    thread = threading.Thread(target=thread_task, args=(filename, thread_id))
    threads.append(thread)
    thread.start()

  # 모든 쓰레드가 종료될 때까지 대기
  for thread in threads:
    thread.join()

  print("CSV 파일 작성 완료")