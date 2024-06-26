import os
from collections import defaultdict

import pandas as pd
import pytchat

from src.exception.CustomException import CustomException


async def live_chat(videoId, folder):
    filename = videoId+'.csv'
    file_path = os.path.join(folder,filename)
    if os.path.exists(filename):
        print(f"파일 '{file_path}'이 이미 존재하여 넘어갑니다.")
    else:
        chat = pytchat.create(video_id=videoId)
        data = defaultdict(list)
        while chat.is_alive():
            chatdata = chat.get()
            for item in chatdata.items:
                data["ID"].append(item.id)
                data["Name"].append(item.author.name)
                data["comment"].append(item.message)
                data["Date"].append(item.datetime)
                data["time"].append(item.elapsedTime)

        result = pd.DataFrame(data)
        result.to_csv(file_path, mode="a", index=False)

        try:
            # 채팅이 더이상 존재하지 않은면 exception 발생
            chat.raise_for_status()
        except Exception as e:
            if type(e).__name__ == "ChatDataFinished":
                pass
            elif type(e).__name__ == "NoContents":
                raise CustomException("채팅 데이터가 없습니다")
            else:
                raise CustomException("[live_chat] 알 수 없는 ERROR")
