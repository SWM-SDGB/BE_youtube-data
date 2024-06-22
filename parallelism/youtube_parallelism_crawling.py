import asyncio
import os
import sys
import time
import ray

from parallelism.exception.error_handling import errorHandling
from parallelism.lock.SystemMutex import SystemMutex
from parallelism.summary.summary_generate import generate_summary_csv
from util.youtube_live_video_list_crawling import get_video_urls_by_selenium
from util.youtube_livechat_crawling_nonBuffer import live_chat
from util.youtube_parsing_viewing_distribution import html_parsing
from util.youtube_video_down import get_video_sound

ray.init(num_cpus=10, dashboard_host="0.0.0.0")

channel_id = "@15ya.fullmoon"

def remove_leading_at_sign(s):
    if s.startswith('@'):
        return s[1:]
    return s

default_folder = "./data/"+remove_leading_at_sign(channel_id)


@ray.remote
def proccess(url, index, folder):
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


if __name__ == "__main__":
    start = time.time()

    ensure_folder_exists(default_folder)

    video_urls = get_video_urls_by_selenium(channel_id)
    tasks = len(video_urls)
    print("총 비디오 개수 : " + str(tasks))

    result_url = []
    [result_url.append((proccess.remote(video_urls[task], task, default_folder))) for task in range(tasks)]
    result = ray.get(result_url)

    end = time.time()
    print(f"총 걸린시간 - {end-start}")
    print(f"results count - {str(len(result))}")
