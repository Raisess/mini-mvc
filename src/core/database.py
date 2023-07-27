import os

class Database:
  def __init__(self, user: str, pass: str, host: str, port: int):
    self.user = os.getenv("DB_USER") or user
    self.pass = os.getenv("DB_PASS") or pass
    self.host = os.getenv("DB_HOST") or host
    self.port = os.getenv("DB_PORT") or port
