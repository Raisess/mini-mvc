from __core.repository import Repository
from app.models import {{name}}Model

class {{name}}Repository(Repository):
  def create(self, data: {{name}}Model) -> str:
    raise NotImplemented()

  def update(self, id: str, new_data: {{name}}Model) -> None:
    raise NotImplemented()

  def find_one(self, id: str) -> {{name}}Model | None:
    raise NotImplemented()

  def find(self, filter: dict) -> list[{{name}}Model]:
    raise NotImplemented()

  def remove_one(self, id: str) -> None:
    raise NotImplemented()

  def remove(self, filter: dict) -> None:
    raise NotImplemented()
