
class ParseViewingUnknownException(Exception):
  def __init__(self, message="[Parse Viewing] 알 수 없는 ERROR"):
    self.message = message
    super().__init__(self.message)