
def url_by_channel_id(channel_id):
  return 'https://www.youtube.com/'+channel_id+'/streams'

def get_video_id(youtube_url):
  return youtube_url.split("v=")[1]
