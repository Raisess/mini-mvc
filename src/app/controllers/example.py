from core.controller import Controller, Validation, Validator
from app.models import ExampleModel
from app.views import ExampleView

def _name_validation(name: str) -> bool:
  return name.strip() != ""


class ExampleController(Controller):
  def __init__(self):
    self.__model = ExampleModel(name="Example")

  def handle_request(self, args: dict, form: dict) -> None:
    name = form.get("name")
    Validator.Validate(name, [
      Validation("Invalid name", _name_validation)
    ])

    self.__model.name = name

  def handle_view(self) -> str:
    return self.render(ExampleView(), { "data": self.__model })
