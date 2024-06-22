import os
import traceback


def errorHandling(e, url, videoId):
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