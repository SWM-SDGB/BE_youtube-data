import fcntl
import hashlib


class SystemMutex:
  def __init__(self, name):
    self.name = name

  def __enter__(self):
    lock_id = hashlib.md5(self.name.encode('utf8')).hexdigest()
    self.fp = open(f'/tmp/.lock-{lock_id}.lck', 'wb')
    fcntl.flock(self.fp.fileno(), fcntl.LOCK_EX)

  def __exit__(self, _type, value, tb):
    fcntl.flock(self.fp.fileno(), fcntl.LOCK_UN)
    self.fp.close()