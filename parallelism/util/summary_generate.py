from datetime import datetime, timedelta
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

  return past_time.strftime('%Y/%m/%d %H:%M')

def get_start_date(description_inner_text): # return ex) "2024/06/21 18:09"
  pattern = r'(\d+)\s*(초|분|시간|일|주|개월|년)\s*전'
  match = re.search(pattern, description_inner_text)
  if match:
   time = int(match.group(1)) # 시간 숫자값
   unit = match.group(2) # 시간 단위
   return convert_datetime(time, unit)
  else:
    print("조회수를 찾을 수 없습니다.")
    return

def get_hash_tag(description_inner_text): # return ex) "#mbti#최고민수#이창호"
  hashtag_pattern = re.compile(r'#\S+')
  hashtags = hashtag_pattern.findall(description_inner_text)
  return ''.join(hashtags)