import argparse
import ray

from src import globals
from src.core.ray.ray_process_args import args_process
from src.youtube_parallelism_crawling import ray_execute

# 명령행 인자를 사용하여 옵션을 조절하도록 구성합니다.
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Process some functions.")
  parser.add_argument("--channel_id", type=str, required=True, help="Target channel Id")
  parser.add_argument("--cpus", type=int, required=True, help="use cpu core")
  parser.add_argument("--folder", type=str, required=False, help="Save folder path")

  parser.add_argument("--viewing", action="store_true", help="Run HTML parsing")
  parser.add_argument("--chat", action="store_true", help="Run live chat extraction")
  parser.add_argument("--sound", action="store_true", help="Run video sound extraction")
  parser.add_argument("--all", action="store_true", default=True, help="Run all functions (default)")

  args = parser.parse_args()
  if args.viewing or args.chat or args.sound:
    args.all = False

  if args.all:
    args.viewing = True
    args.chat = True
    args.sound = True

  globals.args["chat"] = args.chat
  globals.args["sound"] = args.sound
  globals.args["all"] = args.all
  globals.args["channel_id"] = args.channel_id
  globals.args["cpus"] = args.cpus
  globals.args["folder"] = args.folder
  globals.args["viewing"] = args.viewing

  print(f"""
      args.channel_id = {globals.args["channel_id"]} 
      args.viewing = {globals.args["viewing"]}
      args.chat = {globals.args["chat"]}
      args.sound = {globals.args["sound"]}
      args.folder = {globals.args["folder"]}
      args.cpus = {globals.args["cpus"]}
    """)

  ray.init(num_cpus=globals.args["cpus"], dashboard_host="0.0.0.0", ignore_reinit_error=True)
  ray_execute(globals.args["channel_id"], args_process, globals.args["folder"])
