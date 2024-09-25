class NoSQLDatabase:
  def expose(self) -> any:
    raise NotImplemented()

  def add(self, collection: str, data: dict, id: str = None) -> str:
    raise NotImplemented()

  def get(self, collection: str, id: str) -> dict | None:
    raise NotImplemented()

  def list_by(self, collection: str, key: str = None, value: str | int = None) -> list[dict]:
    raise NotImplemented()

  def remove(self, collection: str, id: str) -> None:
    raise NotImplemented()
