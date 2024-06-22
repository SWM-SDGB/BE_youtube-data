import re
def get_view_score(description_inner_text):
  pattern = r'\d+(?:\.\d+)?[만천]?회'
  match = re.search(pattern, description_inner_text)
  if match:
    views_str = match.group(0) # ex) '15만회'
    # 만회인 경우
    if '만' in views_str:
      views = int(float(views_str[:-2]) * 10000)
    # 천회인 경우
    elif '천' in views_str:
      views = int(float(views_str[:-2]) * 1000)
    # 일반적인 경우
    else:
      views = int(views_str[:-1])

    return views
  else:
    print(f"조회수를 찾을 수 없습니다. match={match}")
    return None