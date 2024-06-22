import asyncio
import ray
from parallelism.exception.error_handling import errorHandling
from parallelism.lock.SystemMutex import SystemMutex
from parallelism.parser.url_parser import get_video_id
from parallelism.summary.summary_generate import generate_summary_csv
from parallelism.util.youtube_livechat_crawling_nonBuffer import live_chat
from parallelism.util.youtube_parsing_viewing_distribution import html_parsing
from parallelism.util.youtube_video_down import get_video_sound
from parallelism import globals

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
    asyncio.run(gather(tasks))
    with SystemMutex('critical-section'):
      generate_summary_csv(url,folder)
  except Exception as e:
    errorHandling(e, url, video_id)

async def gather(tasks):
  await asyncio.gather(*tasks)

