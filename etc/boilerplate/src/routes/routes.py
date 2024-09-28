from __core.controller import Controller

controller = Controller("routes", __name__)
routes = controller.router()

@routes.get("/")
def index():
  return controller.render("index")
