import os
import sys


import time

import ray

from src import globals
from src.core.crwaling.youtube_live_video_list_crawling import \
  get_video_urls_by_selenium

"""
ray_process 를 인자로 받아 실행킵니다.
상황에따라 Ray_process를 새로 작성하고 사용할 수 있습니다.
"""
def ray_execute(ray_process_func):

  channel_id = globals.args["channel_id"]
  folder = globals.args["folder"]
  ensure_folder_exists(folder)

  video_urls = get_video_urls_by_selenium(channel_id)
  tasks = len(video_urls)
  print("총 비디오 개수 : " + str(tasks))

  start = time.time()
  result_url = []
  [result_url.append(ray_process_func.remote(video_urls[task], task, folder)) for task in range(tasks)]
  ray.get(result_url)
  end = time.time()
  print(f"총 걸린시간 - {end-start}")
  print(f"처리된 개수 - "+str(len(result_url)))


def ensure_folder_exists(folder_path):
  if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"Folder '{folder_path}' created.")
  else:
    print(f"Folder '{folder_path}' already exists.")
    overwrite = input("그대로 진행하시겠습니까? (Y/N): ").replace(" ","").strip().lower()
    if overwrite == 'y':
      print("기존 폴더를 유지합니다.")
    elif overwrite == 'n':
      print("프로그램을 종료합니다.")
      sys.exit()
    else:
      print("잘못된 입력입니다. 프로그램을 종료합니다.")
      sys.exit()


