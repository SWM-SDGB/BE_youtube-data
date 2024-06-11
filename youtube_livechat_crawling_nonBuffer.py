# simple non-buffered object for fetching live chat
import pytchat
import time
import pandas as pd
import sys

videoId = "9EmfEyjIQo0";
chat = pytchat.create(video_id=videoId)
file_path = './'+videoId+'.csv'
empty_frame = pd.DataFrame(columns=['chatId','댓글 작성자', '댓글 내용', '댓글 작성 시간','소요시간'])

while chat.is_alive():
  chatdata = chat.get()
  for item in chatdata.items:
    print(item.json)

    print(f"{item.datetime} [{item.author.name}]- {item.message}")
    data = {
      'chatId' : [item.id],
      '댓글 작성자' : [item.author.name],
      '댓글 내용' : [item.message],
      '댓글 작성 시간' : [item.datetime],
      'elapsedTime' : [item.elapsedTime]
    }
    result = pd.DataFrame(data)
    result.to_csv(file_path, mode='a', header=False,index=False)


try:
  chat.raise_for_status()
except pytchat.ChatdataFinished:
  print("chat data finished")
except Exception as e:
  print(type(e), str(e))