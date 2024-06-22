import re
def get_hash_tag(description_inner_text):
  hashtag_pattern = re.compile(r'#\S+')
  hashtags = hashtag_pattern.findall(description_inner_text)
  return ''.join(hashtags)
