
class LiveChatUnknownException(Exception):
  def __init__(self, message="[live_chat] 알 수 없는 ERROR"):
    self.message = message
    super().__init__(self.message)