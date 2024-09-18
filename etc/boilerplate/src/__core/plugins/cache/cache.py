class Cache:
  def write(self, key: str, value: str, ttl: int = None) -> None:
    raise NotImplemented()

  def write_json(self, key: str, value: any, ttl: int = None) -> None:
    raise NotImplemented()

  def scan(self, pattern: str) -> list[str]:
    raise NotImplemented()

  def read(self, key: str) -> str | None:
    raise NotImplemented()

  def read_json(self, key: str) -> any:
    raise NotImplemented()

  def remove(self, keys: list[str]) -> int:
    raise NotImplemented()

  def ttl(self, key: str) -> int | None:
    raise NotImplemented()
