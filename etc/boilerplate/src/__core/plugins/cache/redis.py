# @NOTE: To use this implementation you need to add the `redis` package to
# `requirements.txt`
# @REFERENCE: https://github.com/redis/redis-py

import json
from redis import Redis as RedisClient

from __core.env import Env, InvalidEnvironmentException

class NotConnectedException(Exception):
  def __init__(self):
    super().__init__("Redis cache not connected")


class Redis:
  __CLIENT: RedisClient = None

  @staticmethod
  def Init():
    if Redis.__CLIENT:
      return

    host = Env.Get("REDIS_HOST")
    if not host: raise InvalidEnvironmentException("REDIS_HOST")
    port = Env.Get("REDIS_PORT")
    if not port: raise InvalidEnvironmentException("REDIS_PORT")

    Redis.__CLIENT = RedisClient(
      host=host,
      port=int(port),
      password=Env.Get("REDIS_PASS")
    )

  def write(self, key: str, value: any, ttl: int = None) -> None:
    if not Redis.__CLIENT:
      raise NotConnectedException()

    if not Redis.__CLIENT.set(key, value, ex=ttl):
      raise Exception(f"Failed to set {key} in cache")

  def write_json(self, key: str, value: any, ttl: int = None) -> None:
    if not Redis.__CLIENT:
      raise NotConnectedException()

    self.write(key, json.dumps(value), ttl)

  def read(self, key: str) -> str | None:
    if not Redis.__CLIENT:
      raise NotConnectedException()

    return Redis.__CLIENT.get(key)

  def read_json(self, key: str) -> any:
    if not Redis.__CLIENT:
      raise NotConnectedException()

    data = self.read(key)
    if not data:
      return None

    return json.loads(data)

  def remove(self, keys: list[str]) -> int:
    if not Redis.__CLIENT:
      raise NotConnectedException()

    return Redis.__CLIENT.delete(keys)

  def ttl(self, key: str) -> int | None:
    if not Redis.__CLIENT:
      raise NotConnectedException()

    Redis.__CLIENT.ttl(key)
