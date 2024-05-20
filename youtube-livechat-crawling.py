
import pytchat #실시간 댓글 크롤링
import pafy #유튜브 정보
import pandas as pd

#https://www.youtube.com/watch?v=kWt618nMGR0, 2024년 01월 27일 | 주말 잡담, 삼각 전략
api_key = 'api-key' #gcp youtube data api 에서 api key 생성
pafy.set_api_key(api_key)

video_id = 'kWt618nMGR0'
file_path = '../침착맨-2024년_01월_27일_|_주말_잡담,_삼각_전략.csv'

empty_frame = pd.DataFrame(columns=['chatId','댓글 작성자', '댓글 내용', '댓글 작성 시간','소요시간'])
chat = pytchat.create(video_id=video_id)

sequnce = 0;
while chat.is_alive():
  cnt = 0
  try:
    data = chat.get()
    items = data.items
    for c in items:
      print(f"{c.datetime} [{c.author.name}]- {c.message}")
      sequnce+=1;
      data.tick()
      data2 = {'chatId' : c.id, '댓글 작성자' : [c.author.name], '댓글 내용' : [c.message], '댓글 작성 시간' : [c.datetime], 'elapsedTime' : c.elapsedTime}
      result = pd.DataFrame(data2)
      result.to_csv(file_path, mode='a', header=False,index=False)
    cnt += 1
    if cnt == 5 : break
  except KeyboardInterrupt:
    chat.terminate()
    break

df = pd.read_csv(file_path, names=['chatId','댓글 작성자', '댓글 내용', '댓글 작성 시간','소요시간'])
df.head(30)