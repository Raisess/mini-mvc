from time import sleep, time
from threading import Lock, Thread

from __core.exceptions import NotConnectedException
from __core.plugins.cache.cache import Cache

WORKER_INTERVAL_SECS = 0.100

class Memory(Cache):
  __STARTED = False
  __LOCK = None
  __DATA: dict[str, any] = {}
  __TTL: dict[str, (int, int)] = {}

  @staticmethod
  def Init():
    if Memory.__STARTED:
      return

    Memory.__LOCK = Lock()
    Thread(target=Memory.__Worker, daemon=True).start()
    Memory.__STARTED = True

  @staticmethod
  def __ValidateStart() -> None:
    if not Memory.__STARTED:
      raise NotConnectedException("Memory", "USE_MEMORY")

  def write(self, key: str, value: str, ttl: int = None) -> None:
    return self.write_json(key, value, ttl)

  def write_json(self, key: str, value: any, ttl: int = None) -> None:
    Memory.__ValidateStart()
    Memory.__DATA[key] = value
    if ttl and ttl > 0:
      Memory.__TTL[key] = (time(), ttl)

  def read(self, key: str) -> any:
    return self.read_json(key)

  def read_json(self, key: str) -> any:
    Memory.__ValidateStart()
    return Memory.__DATA.get(key)

  def remove(self, keys: list[str]) -> int:
    Memory.__ValidateStart()
    for key in keys:
      Memory.__DATA.pop(key)
      Memory.__TTL.pop(key)

  def ttl(self, key: str) -> int | None:
    Memory.__ValidateStart()
    ttl = Memory.__TTL.get(key)
    return ttl[1] if ttl else None

  @staticmethod
  def __Flush() -> None:
    ttl_entries = Memory.__TTL.items()
    if len(ttl_entries) == 0:
      return

    with Memory.__LOCK:
      now = time()
      to_delete_keys = []
      for (key, (timestamp, ttl)) in ttl_entries:
        if int(now) - int(timestamp) >= ttl:
          Memory.__DATA.pop(key)
          to_delete_keys.append(key)

      for key in to_delete_keys:
        Memory.__TTL.pop(key)

  @staticmethod
  def __Worker() -> None:
    while True:
      Memory.__Flush()
      sleep(WORKER_INTERVAL_SECS)
