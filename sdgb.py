import argparse
import ray

from parallelism.util.ray.ray_process_args import ArgsProcessor
from parallelism.youtube_parallelism_crawling import ray_execute


# 명령행 인자를 사용하여 옵션을 조절하도록 구성합니다.
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Process some functions.")
  parser.add_argument("--channel_id", type=str, required=True, help="Target channel Id")
  parser.add_argument("--cpus", type=int, required=True, help="use cpu core")
  parser.add_argument("--folder", type=str, required=False, help="savefolder path")

  parser.add_argument("--viewing", action="store_true", help="Run HTML parsing")
  parser.add_argument("--chat", action="store_true", help="Run live chat extraction")
  parser.add_argument("--sound", action="store_true", help="Run video sound extraction")
  parser.add_argument("--all", action="store_true", default=True, help="Run all functions (default)")

  args = parser.parse_args()
  ray.init(num_cpus=args.cpus, dashboard_host="0.0.0.0",ignore_reinit_error=True)

  if args.viewing or args.chat or args.sound:
    args.all = False

  if args.all:
    args.viewing = True
    args.chat = True
    args.sound = True

  print(f"""
    args.channel_id = {args.channel_id} 
    args.viewing = {args.viewing}
    args.chat = {args.chat}
    args.sound = {args.sound}
    args.folder = {args.folder}
    args.cpus = {args.cpus}
  """)
  args_processor = ArgsProcessor(args)
  ray_execute(args.channel_id, args_processor.args_process, args.folder)
