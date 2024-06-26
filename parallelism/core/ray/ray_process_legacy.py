import asyncio
import ray

from parallelism.exception.error_handling import error_handling
from parallelism.lock.SystemMutex import SystemMutex
from parallelism.parser.url_parser import get_video_id
from parallelism.summary.summary_generate import generate_summary_csv
from parallelism.core.youtube_livechat_crawling_nonBuffer import live_chat
from parallelism.core.youtube_parsing_viewing_distribution import html_parsing
from parallelism.core.youtube_video_down import get_video_sound



@ray.remote
def process(url, index, folder):
  videoId = get_video_id(url)
  print(f"URL: {url} -> Video ID: {videoId} #index {index}")

  try:
    asyncio.run(async_process(url, videoId, folder))
    with SystemMutex('critical-section'):
      generate_summary_csv(url,folder)
  except Exception as e:
    error_handling(e, url, videoId)


async def async_process(url, video_id, folder):
  await asyncio.gather(html_parsing(url, video_id, folder), live_chat(video_id, folder), get_video_sound(url, video_id, folder))

