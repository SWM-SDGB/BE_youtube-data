
from src import globals
from src.core.ray.process.ray_process import process
from src.core.ray.ray_execute import ray_execute

if __name__ == "__main__":
    channel_id = "@15ya.fullmoon"
    default_folder = "../data/"+channel_id[1:]

    globals.args["channel_id"] = channel_id
    globals.args["folder"] = default_folder
    globals.args["cpus"] = 10

    ray_execute(process)


