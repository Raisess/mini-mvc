import os
from jinja2 import Template

class View:
  __DATA = {}

  @staticmethod
  def Init(dir: str = "public") -> None:
    files = os.listdir(dir)
    for file in files:
      path = f"{dir}/{file}"
      if os.path.isdir(path) and path != "public/static" and path != "public/emails":
        View.Init(path)

      if file.endswith(".html"):
        with open(path, "r") as html_file:
          name = "/".join(path.split("/")[1:]).split(".")[0]
          View.__DATA[name] = html_file.read()

  def __init__(self, name: str):
    self.__html = View.__DATA.get(name)
    if not self.__html:
      with open(f"public/{name}.html", "r") as html_file:
        self.__html = html_file.read()

  def render(self, params: dict[str, str | int] = {}) -> str:
    template = Template(self.__html)
    return template.render(params)
