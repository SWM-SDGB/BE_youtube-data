import asyncio
import os
import time
import traceback

import ray

from parallelism.Lock.SystemMutex import SystemMutex
from parallelism.summary.summary_generate import generate_summary_csv
from util.youtube_live_video_list_crawling import get_video_urls_by_selenium
from util.youtube_livechat_crawling_nonBuffer import live_chat
from util.youtube_parsing_viewing_distribution import html_parsing
from util.youtube_video_down import get_video_sound

ray.init(num_cpus=1, dashboard_host="0.0.0.0")

folder = "./15yafullmoon"
channel_id = "@15ya.fullmoon"


@ray.remote
def proccess(url, index, folder):
    videoId = get_video_id(url)
    print(f"URL: {url} -> Video ID: {videoId} #index {index}")

    try:
        asyncio.run(async_process(url, videoId, folder))
    except Exception as e:
        try:
            print(f"Error processing {url}: {e.message}")
        except AttributeError:
            print("[Unknown Error]")
            traceback.print_exc()
        csv_file = videoId + ".csv"
        json_file = videoId + ".json"
        audio_file = videoId + ".m4a"
        if os.path.exists(csv_file):
            os.remove(csv_file)
        if os.path.exists(json_file):
            os.remove(json_file)
        if os.path.exists(audio_file):
            os.remove(audio_file)
        pass


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


if __name__ == "__main__":
    start = time.time()

    ensure_folder_exists(folder)

    video_urls = get_video_urls_by_selenium(channel_id)
    tasks = len(video_urls)
    print("총 비디오 개수 : " + str(tasks))

    result_url = []
    [result_url.append((proccess.remote(video_urls[task], task, folder))) for task in range(tasks)]
    result = ray.get(result_url)

    end = time.time()
    print(f"총 걸린시간 - {end-start}")
    print(f"results count - {str(len(result))}")
