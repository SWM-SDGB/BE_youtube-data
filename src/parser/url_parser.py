from datetime import datetime, timedelta

from src.globals import global_timestamp_format


def url_by_channel_id(channel_id):
  return 'https://www.youtube.com/' + channel_id + '/streams'


def get_video_id(youtube_url):
  return youtube_url.split("v=")[1]


def convert_datetime(time, unit, format=global_timestamp_format):
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
    past_time = now.replace(
        month=now.month - time if now.month > time else 12 + now.month - time)
  elif unit == '년':
    past_time = now.replace(year=now.year - time)

  return past_time.strftime(format)
  writer.writerows(data)
