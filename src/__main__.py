import time

from src.core.ray.process.ray_process import process
from src.core.ray.ray_execute import ray_execute

channel_id = "@15ya.fullmoon"
default_folder = "./data/"+channel_id.startswith('@')[1:]

if __name__ == "__main__":
    start = time.time()
    ray_execute(process)
    end = time.time()

    print(f"총 걸린시간 - {end-start}")


