from typing import Callable
from core.view import View

class Controller:
  def render(self, view: View, data: dict = {}) -> str:
    return view.render(data)


class Validation:
  def __init__(self, message: str, check: Callable[str, bool]):
    self.message = message
    self.check = check


class Validator:
  @staticmethod
  def Validate(value: str, validations: list[Validation]) -> None:
    for validation in validations:
      if not validation.check(value):
        raise Exception(validation.message)
