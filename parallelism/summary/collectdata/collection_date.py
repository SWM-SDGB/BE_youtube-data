from datetime import datetime

def get_collection_date():
  now = datetime.now()
  return now.strftime("%Y/%m/%d")

