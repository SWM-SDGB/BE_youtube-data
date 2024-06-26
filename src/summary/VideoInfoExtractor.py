import re
from datetime import datetime

from src.globals import global_timestamp_format
from src.parser.url_parser import convert_datetime


class VideoInfoExtractor:
  def __init__(self):
    self.hashtag_pattern = re.compile(r'#\S+')
    self.start_date_pattern = re.compile(r'(\d+)\s*(초|분|시간|일|주|개월|년)\s*전')
    self.view_score_pattern = re.compile(r'\d+(?:\.\d+)?[만천]?회')

  def get_collection_date(self):
    return datetime.now().strftime(global_timestamp_format)

  def get_hash_tag(self, description_inner_text):
    hashtags = self.hashtag_pattern.findall(description_inner_text)
    return ''.join(hashtags)

  def get_start_date(self, description_inner_text):  # return ex) "2024/06/21"
    match = self.start_date_pattern.search(description_inner_text)
    if match:
      time = int(match.group(1))  # 시간 숫자값
      unit = match.group(2)  # 시간 단위
      return convert_datetime(time, unit)
    else:
      print(f"스트리밍 시작일 찾을 수 없습니다. match={match}")
      return

  def get_view_score(self, description_inner_text):
    match = self.view_score_pattern.search(description_inner_text)
    if match:
      views_str = match.group(0)  # ex) '15만회'
      # n만회인 경우
      if '만' in views_str:
        views = int(float(views_str[:-2]) * 10000)
      # n천회인 경우
      elif '천' in views_str:
        views = int(float(views_str[:-2]) * 1000)
      # n회 경우
      else:
        views = int(views_str[:-1])

      return views
    else:
      print(f"조회수를 찾을 수 없습니다. match={match}")
      return None

  def get_video_name(self, title):
    video_name = title.split('-')[0]
    return video_name
