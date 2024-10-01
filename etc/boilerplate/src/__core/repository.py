from __core.model import Model

class Repository:
  def create(self, data: Model) -> str:
    raise NotImplemented()

  def update(self, id: str, new_data: dict) -> None:
    raise NotImplemented()

  def find_one(self, id: str) -> Model | None:
    raise NotImplemented()

  def find(self, filter: dict) -> list[Model]:
    raise NotImplemented()

  def remove_one(self, id: str) -> None:
    raise NotImplemented()

  def remove(self, filter: dict) -> None:
    raise NotImplemented()
