# @NOTE: To use this implementation you need to add the `redis` package to
# `requirements.txt`
# @REFERENCE: https://github.com/redis/redis-py

import json
from redis import Redis as RedisClient

from __core.env import Env, InvalidEnvironmentException
from __core.plugins.cache.cache import Cache

class NotConnectedException(Exception):
  def __init__(self):
    super().__init__("Redis cache not connected")


class Redis(Cache):
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

  @staticmethod
  def GetClient() -> RedisClient:
    if not Redis.__CLIENT:
      raise NotConnectedException()

    return Redis.__CLIENT

  def write(self, key: str, value: str, ttl: int = None) -> None:
    client = Redis.GetClient()
    if not client.set(key, value, ex=ttl):
      raise Exception(f"Failed to set {key} in cache")

  def write_json(self, key: str, value: any, ttl: int = None) -> None:
    self.write(key, json.dumps(value), ttl)

  def scan(self, pattern: str) -> list[str]:
    client = Redis.GetClient()
    return [key for key in client.scan_iter(pattern)]

  def read(self, key: str) -> str | None:
    client = Redis.GetClient()
    return client.get(key)

  def read_json(self, key: str) -> any:
    data = self.read(key)
    if not data:
      return None

    return json.loads(data)

  def remove(self, keys: list[str]) -> int:
    client = Redis.GetClient()
    return client.delete(keys)

  def ttl(self, key: str) -> int | None:
    client = Redis.GetClient()
    client.ttl(key)
