
class EmptyLiveChatException(Exception):
  def __init__(self, message="채팅 데이터가 없습니다"):
    self.message = message
    super().__init__(self.message)

