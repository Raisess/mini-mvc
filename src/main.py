#! /usr/bin/env python3

import os
import shutil
from yacli import CLI, Command

class Init(Command):
  def __init__(self):
    super().__init__(
      command="init",
      description="Init new project.",
      args_len=1
    )

  def handle(self, args: list[str]) -> None:
    name = args[0]
    shutil.copytree("/usr/local/etc/mini-mvc/boilerplate", f"./{name}")
    os.system(f"cd ./{name} && ./scripts/setup.sh")
    print(f"> Created new project {name}!")


class Generate(Command):
  def __init__(self):
    super().__init__(
      command="gen",
      description="Generate new file.",
      args_len=2
    )

  def handle(self, args: list[str]) -> None:
    ftype = args[0]
    ["controller", "model", "view"].index(ftype)

    src_content = ""
    with open(f"/usr/local/etc/mini-mvc/templates/{ftype}.template.py", "r") as src:
      src_content = src.read()

    path = args[1].split("/")
    folder = None
    name = path[0]
    full_path = f"./src/app/{ftype}s/{name}.py"
    if len(path) > 1:
      folder = path[:-1][0]
      name = path[-1:][0]
      dest_path = f"./src/app/{ftype}s/{folder}"
      full_path = f"{dest_path}/{name}.py"

      if not os.path.exists(dest_path):
        os.mkdir(dest_path)


    if os.path.exists(full_path):
      print("> FAIL: File already exists!")
      return

    with open(full_path, "w") as dest:
      dest.write(src_content.replace("{{name}}", self.__to_camel(name)))

    with open(f"./src/app/{ftype}s/__init__.py", "a") as init:
      class_name = f"{self.__to_camel(name)}{ftype.capitalize()}"
      if folder:
        init.write(f"\nfrom app.{ftype}s.{folder}.{name} import {class_name}")
      else:
        init.write(f"\nfrom app.{ftype}s.{name} import {class_name}")

    print(f"> SUCCESS: Generated new {ftype} at {full_path}!")

  def __to_camel(self, string: str) -> str:
    return "".join([item.capitalize() for item in string.split("_")])


if __name__ == "__main__":
  cli = CLI("mini-mvc", [Init(), Generate()])
  cli.handle()
