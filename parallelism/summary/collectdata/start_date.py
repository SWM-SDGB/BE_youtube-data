from datetime import datetime, timedelta
import re
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
  writer.writerows(data)