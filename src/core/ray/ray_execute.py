import sys

from src.__main__ import default_folder
import ray
import os

from src.core.crwaling.youtube_live_video_list_crawling import \
  get_video_urls_by_selenium

ray.init(num_cpus=globals.args["cpus"], dashboard_host="0.0.0.0", ignore_reinit_error=True)

def ray_execute(ray_process_func):
  channel_id = globals.args["channel_id"]
  folder = globals.args["folder"]

  if str(folder) == 'None':
    folder = default_folder

  ensure_folder_exists(folder)

  video_urls = get_video_urls_by_selenium(channel_id)
  tasks = len(video_urls)
  print("총 비디오 개수 : " + str(tasks))

  [(ray_process_func.remote(video_urls[task], task, folder)) for task in range(tasks)]

def ensure_folder_exists(folder_path):
  if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"Folder '{folder_path}' created.")
  else:
    print(f"Folder '{folder_path}' already exists.")
    overwrite = input("그대로 진행하시겠습니까? (Y/N): ").strip().lower()
    if overwrite == 'y':
      print("기존 폴더를 유지합니다.")
    elif overwrite == 'n':
      print("프로그램을 종료합니다.")
      sys.exit()
    else:
      print("잘못된 입력입니다. 프로그램을 종료합니다.")
      sys.exit()


