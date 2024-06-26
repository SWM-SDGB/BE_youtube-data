import os
import traceback

"""
하나의 비디오에 대해 데이터 수집 중 예외가 발생할 경우 실패로 간주. 생성된 파일을 삭제합니다.
"""

def error_handling(custom_error, url, video_id):
  try:
    print(f"Error processing {url}: {custom_error.message}")
  except AttributeError:
    print("[Unknown Error]")
    traceback.print_exc()

  # 생성되는 파일 확장자 목록
  extensions = [".csv", ".json", ".m4a"]

  # 파일 삭제
  for extension in extensions:
    file = f"{video_id}{extension}"
    if os.path.exists(file):
      os.remove(file)