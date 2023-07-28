#! /usr/bin/env python3

import os
import shutil
from yacli import CLI, Command

class Create(Command):
  def __init__(self):
    super().__init__(
      command="create",
      description="Create new project.",
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
    name = args[1]
    ["controller", "model", "view"].index(ftype)

    src_content = ""
    with open(f"/usr/local/etc/mini-mvc/templates/{ftype}.template.py", "r") as src:
      src_content = src.read()

    dest_path = f"./src/app/{ftype}s/{name}.py"
    with open(dest_path, "w") as dest:
      dest.write(src_content.replace("{{name}}", name.capitalize()))

    with open(f"./src/app/{ftype}s/__init__.py", "a") as init:
      init.write(f"\nfrom app.{ftype}s.{name} import {name.capitalize()}{ftype.capitalize()}")

    print(f"> Generated new {ftype} at {dest_path}!")


if __name__ == "__main__":
  cli = CLI("mini-mvc", [Create(), Generate()])
  cli.handle()
