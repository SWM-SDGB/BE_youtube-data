import asyncio

import ray

from src.core.crwaling.youtube_livechat_crawling_nonBuffer import live_chat
from src.core.crwaling.youtube_parsing_viewing_distribution import html_parsing
from src.core.crwaling.youtube_video_down import get_video_sound
from src.exception.error_handling import error_handling
from src.lock.SystemMutex import SystemMutex
from src.parser.url_parser import get_video_id
from src.summary.summary_generate import generate_summary_csv
from src import globals
"""
모든 crwaling task를 실행하는 레거시 Process 입니다.
"""
@ray.remote
def process(url, index, folder):
  video_id = get_video_id(url)
  print(f"URL: {url} -> Video ID: {video_id} #index {index}")

  try:
    asyncio.run(async_task(url, video_id, folder))
    with SystemMutex('critical-section'):
      generate_summary_csv(url,folder)
  except Exception as e:
    error_handling(e, url, video_id)


async def async_task(url, video_id, folder):
  await asyncio.gather(html_parsing(url, video_id, folder), live_chat(video_id, folder), get_video_sound(url, video_id, folder))

