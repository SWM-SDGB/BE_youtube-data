import pytchat
import pandas as pd

from exception.EmptyLiveChatException import EmptyLiveChatException
from exception.LiveChatUnknownException import LiveChatUnknownException


async def live_chat(videoId, folder):
    chat = pytchat.create(video_id=videoId)
    file_path = f"./{folder}/{videoId}.csv"

    while chat.is_alive():
        chatdata = chat.get()
        for item in chatdata.items:
            data = {
                "ID": [item.id],
                "Name": [item.author.name],
                "comment": [item.message],
                "Date": [item.datetime],
                "time": [item.elapsedTime],
            }
            result = pd.DataFrame(data)
            result.to_csv(file_path, mode="a", index=False)

    try:
        # 채팅이 더이상 존재하지 않은면 exception 발생
        chat.raise_for_status()
    except Exception as e:
        if type(e).__name__ == "ChatDataFinished":
            pass
        elif type(e).__name__ == "NoContents":
            raise EmptyLiveChatException()
        else:
            raise LiveChatUnknownException()
