from __core.controller import Controller

controller = Controller("routes", __name__)
routes = controller.router()

@routes.get("/")
def get():
  return controller.render("index")
