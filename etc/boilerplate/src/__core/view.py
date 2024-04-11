import os
import zlib
from jinja2 import Template

class View:
  __DATA: dict[str, str | bytes] = {}

  @staticmethod
  def Init(dir: str = "public", use_compression: bool = False) -> None:
    files = os.listdir(dir)
    for file in files:
      path = f"{dir}/{file}"
      if os.path.isdir(path) and path != "public/static" and path != "public/emails":
        View.Init(path)

      if file.endswith(".html"):
        with open(path, "r") as html_file:
          data = "".join([part.strip() for part in html_file.read().split("\n")])
          View.__DATA[path] = zlib.compress(bytes(data, "utf-8")) if use_compression else data

  def __init__(self, name: str):
    path = f"public/{name}.html"
    self.__html = View.__DATA.get(path)
    if not self.__html:
      with open(path, "r") as html_file:
        self.__html = html_file.read()

  def render(self, params: dict[str, str | int] = {}) -> str:
    if type(self.__html) == bytes:
      self.__html = str(zlib.decompress(self.__html))

    template = Template(self.__html)
    return template.render(params)
