import posix_ipc

class SystemSemaphore:
  def __init__(self, name, limit):
    self.name  = name
    self.limit = limit

  def __enter__(self):
    kwargs = dict(posix_ipc.O_CREAT, mode=384, initial_value=self.limit)
    self.lock = posix_ipc.Semaphore(f'/{self.name}', **kwargs)
    self.lock.acquire()

  def __exit__(self, _type, value, tb):
    self.lock.release()