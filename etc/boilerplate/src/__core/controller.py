import json
from flask import Blueprint, redirect, request, session
from typing import Callable

from __core.view import View

class Controller:
  class __Session:
    def add(self, key: str, value: str) -> None:
      session[key] = value

    def get(self, key: str) -> str | None:
      return session.get(key)

    def pop(self, key: str) -> None:
      session.pop(key, None)

    def clear(self) -> None:
      session.clear()


  class __Request:
    def form(self) -> dict:
      return request.form

    def args(self) -> dict:
      return request.args

    def method(self) -> str:
      return request.method


  def __init__(self, name: str, import_name: str):
    self.__name = name
    self.__import_name = import_name

  def router(self) -> Blueprint:
    return Blueprint(self.__name, self.__import_name)

  def redirect(self, path: str) -> None:
    return redirect(path)

  def session(self) -> __Session:
    return Controller.__Session()

  def request(self) -> __Request:
    return Controller.__Request()

  def render(self, view: View | str, data: dict = {}) -> str:
    is_view = isinstance(view, View)
    return (view if is_view else View(view)).render(data)

  def json(self, data: dict | str) -> str:
    return json.dumps(data) if isinstance(data, dict) else data
