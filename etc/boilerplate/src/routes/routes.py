from flask import Blueprint, request

routes = Blueprint("routes", __name__)

@routes.get("/")
def get():
  pass

@routes.post("/")
def post():
  pass
