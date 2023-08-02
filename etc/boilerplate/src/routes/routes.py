from flask import Blueprint, request

from core.controller import Controller
from core.view import View

routes = Blueprint("routes", __name__)
controller = Controller()

@routes.get("/")
def get():
  return controller.render(View("index"))
