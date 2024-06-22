from datetime import datetime
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
