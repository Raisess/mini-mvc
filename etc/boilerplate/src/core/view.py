from jinja2 import Template

class View:
  def __init__(self, file: str):
    with open(f"public/{file}.html", "r") as html_file:
      self.__html = html_file.read()

  def render(self, params: dict[str, str | int] = {}) -> str:
    template = Template(self.__html)
    return template.render(params)
