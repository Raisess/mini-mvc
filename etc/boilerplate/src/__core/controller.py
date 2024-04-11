import json
from flask import session
from typing import Callable

from __core.view import View

class Controller:
  def session_set(key: str, value: str) -> None:
    session[key] = value

  def session_get(key: str) -> str | None:
    return session.get(key)

  def session_pop(key: str) -> None:
    session.pop(key, None)

  def render(self, view: View, data: dict = {}) -> str:
    return view.render(data)

  def json(self, data: dict | str) -> str:
    return data if isinstance(data, str) else json.dumps(data)


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
