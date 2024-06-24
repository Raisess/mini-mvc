import json

from __core.plugins.cache.cache import Cache

class Memory(Cache):
  __DATA: dict[str, any] = {}

  @staticmethod
  def Init():
    pass

  def write_json(self, key: str, value: any, _: int = None) -> None:
    Memory.__DATA[key] = value

  def read_json(self, key: str) -> any:
    return Memory.__DATA.get(key)

  def remove(self, keys: list[str]) -> int:
    for key in keys:
      Memory.__DATA.pop(key)
