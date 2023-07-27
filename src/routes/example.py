from flask import Blueprint, redirect, request
from app.controllers import ExampleController

routes = Blueprint("example", __name__)
controller = ExampleController()

@routes.get("/")
def view():
  return controller.handle_view()

@routes.post("/")
def change_name():
  controller.handle_request(request.args, request.form)
  return redirect("/")
