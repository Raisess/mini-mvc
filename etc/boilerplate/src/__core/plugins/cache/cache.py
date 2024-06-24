class Cache:
  def write(self, key: str, value: str, ttl: int = None) -> None:
    raise Exception("Not implemented")

  def write_json(self, key: str, value: any, ttl: int = None) -> None:
    raise Exception("Not implemented")

  def scan(self, pattern: str) -> list[str]:
    raise Exception("Not implemented")

  def read(self, key: str) -> str | None:
    raise Exception("Not implemented")

  def read_json(self, key: str) -> any:
    raise Exception("Not implemented")

  def remove(self, keys: list[str]) -> int:
    raise Exception("Not implemented")

  def ttl(self, key: str) -> int | None:
    raise Exception("Not implemented")
