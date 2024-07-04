import asyncio

import ray

from src import globals
from src.core.crwaling.youtube_livechat_crawling_nonBuffer import live_chat
from src.core.crwaling.youtube_parsing_viewing_distribution import html_parsing
from src.core.crwaling.youtube_video_down import get_video_sound
from src.exception.error_handling import error_handling
from src.lock.SystemMutex import SystemMutex
from src.parser.url_parser import get_video_id
from src.summary.summary_generate import generate_summary_csv

"""
커맨드 실행 명령으로 작동하는 Process 입니다.
옵션을 통해 실행할 task를 지정할 수 있습니다.
"""

ray.init(num_cpus=globals.args["cpus"], dashboard_host="0.0.0.0",ignore_reinit_error=True)
@ray.remote
def args_process(url, index, folder):
  video_id = get_video_id(url)
  print(f"URL: {url} -> Video ID: {video_id} #index {index}")
  tasks = []
  if globals.args["viewing"]:
    tasks.append(html_parsing(url, video_id, folder))
  if globals.args["chat"]:
    tasks.append(live_chat(video_id, folder))
  if globals.args["sound"]:
    tasks.append(get_video_sound(url, video_id, folder))
  try:
    asyncio.run(async_task(tasks))
    with SystemMutex('critical-section'):
      generate_summary_csv(url,folder)
  except Exception as e:
    error_handling(e, url, video_id)

async def async_task(tasks):
  await asyncio.gather(*tasks)

