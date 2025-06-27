# Controller

### Creating a new controller

You can generate a controller by using the command:

```shell
mini-mvc gen controller user_tasks
```

And it will look like this:

```python
from __core.controller import Controller

class UserTasksController(Controller):
  pass
```

### Base methods

The base methods are simple:

#### Router, rendering and redirect:

```python
# Creates a router exposing the http methods decorator
from app.controllers import UserTasksController

controller = UserTasksController("user_tasks", __name__)
routes = controller.router()

@routes.get("/")
def index():
    # Render a page based on your public folder, excluding `emails` and `static`
    return controller.render("/")


@routes.get("/redirect_to_index")
def redirect_to_index():
    return controller.redirect("/")
```

- They also can be used inside the controller using `self`.
    E.g: `self.redirect("/")`

#### Session:

Expose session helper methods, like: `add`, `get`, `pop` and `clear`.

#### Request:

Expose request helper methods.
