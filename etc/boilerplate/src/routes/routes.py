from flask import Blueprint, request

from __core.controller import Controller

routes = Blueprint("routes", __name__)
controller = Controller()

@routes.get("/")
def get():
  return controller.render("index")
