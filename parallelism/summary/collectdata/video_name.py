
def get_video_name(driver):
  video_name = driver.title.split('-')[0]
  return video_name
