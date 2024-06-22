from datetime import datetime

def get_video_name(driver):
  video_name = driver.title.split('-')[0]
  print(video_name)
  return video_name

def get_collection_date():
  now = datetime.now()
  return now.strftime("%Y/%m/%d")


