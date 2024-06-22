
def get_video_name(driver):
  video_name = driver.title.split('-')[0]
  print(video_name)
  return video_name
