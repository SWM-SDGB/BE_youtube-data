import asyncio
import ray
from parallelism.exception.error_handling import errorHandling
from parallelism.parser.url_parser import get_video_id
from parallelism.util.youtube_livechat_crawling_nonBuffer import live_chat
from parallelism.util.youtube_parsing_viewing_distribution import html_parsing
from parallelism.util.youtube_video_down import get_video_sound

class ArgsProcessor:
  def __init__(self, args):
    self.args = args

  @ray.remote
  def args_process(self, url, index, folder):
    video_id = get_video_id(url)
    print(f"URL: {url} -> Video ID: {video_id} #index {index}")
    tasks = []
    if self.args.viewing:
      tasks.append(html_parsing(url, video_id, folder))
    if self.args.chat:
      tasks.append(live_chat(video_id, folder))
    if self.args.sound:
      tasks.append(get_video_sound(url, video_id, folder))
    try:
      asyncio.run(self.gather(tasks))
    except Exception as e:
      self.error_handling(e, url, video_id)

  async def gather(self, tasks):
    await asyncio.gather(*tasks)

  def error_handling(self, e, url, video_id):
    errorHandling(e, url, video_id)