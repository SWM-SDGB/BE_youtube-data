import asyncio
import ray

from parallelism.exception.error_handling import errorHandling
from parallelism.lock.SystemMutex import SystemMutex
from parallelism.summary.summary_generate import generate_summary_csv
from parallelism.util.youtube_livechat_crawling_nonBuffer import live_chat
from parallelism.util.youtube_parsing_viewing_distribution import html_parsing
from parallelism.util.youtube_video_down import get_video_sound



@ray.remote
def process(url, index, folder):
  videoId = get_video_id(url)
  print(f"URL: {url} -> Video ID: {videoId} #index {index}")

  try:
    asyncio.run(async_process(url, videoId, folder))
    with SystemMutex('critical-section'):
      generate_summary_csv(url,folder)
  except Exception as e:
    errorHandling(e,url,videoId)


async def async_process(url, video_id, folder):
  await asyncio.gather(html_parsing(url, video_id, folder), live_chat(video_id, folder), get_video_sound(url, video_id, folder))

def get_video_id(youtube_url):
  return youtube_url.split("v=")[1]
