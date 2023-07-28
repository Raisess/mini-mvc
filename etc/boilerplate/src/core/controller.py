from flask import redirect, request, Request, Response
from typing import Callable
from core.view import View

class Controller:
  def render(self, view: View, data: dict = {}) -> str:
    return view.render(data)

  def request(self) -> Request:
    return request

  def redirect(self, location: str, code: int = 302) -> Response:
    return redirect(location, code)


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
