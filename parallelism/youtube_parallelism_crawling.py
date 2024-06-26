import os
import sys
import time
import ray

from parallelism.core.ray.ray_process_legacy import process
from parallelism.core.crwaling.youtube_live_video_list_crawling import get_video_urls_by_selenium

ray.init(num_cpus=10, dashboard_host="0.0.0.0")
channel_id = "@15ya.fullmoon"

def remove_leading_at_sign(s):
    if s.startswith('@'):
        return s[1:]
    return s

default_folder = "./data/"+remove_leading_at_sign(channel_id)

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


def ray_execute(channel_id,ray_process_func,folder):

    if str(folder) == 'None':
        folder = default_folder

    start = time.time()
    ensure_folder_exists(folder)

    video_urls = get_video_urls_by_selenium(channel_id)
    tasks = len(video_urls)
    print("총 비디오 개수 : " + str(tasks))

    result_url = []
    [result_url.append((ray_process_func.remote(video_urls[task], task, folder))) for task in range(tasks)]
    result = ray.get(result_url)

    end = time.time()
    print(f"총 걸린시간 - {end-start}")
    print(f"results count - {str(len(result))}")

if __name__ == "__main__":
    ray_execute(channel_id,process,default_folder)

