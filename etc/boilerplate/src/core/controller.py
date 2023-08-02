from flask import session
from typing import Callable
from core.view import View

class Controller:
  def session_set(key: str, value: str) -> None:
    return session[key] = value

  def session_get(key: str) -> str | None:
    return session.get(key)

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
