
class EmptyViewingDistributionException(Exception):
  def __init__(self, message="분포데이터가 없습니다."):
    self.message = message
    super().__init__(self.message)