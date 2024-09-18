import os
import sys
import traceback

from flask import Flask
from flask_session import Session

from __core.env import Env
from __core.view import View

# @NOTE: Each plugin needs to have an static `Init` method
PLUGINS = [
  ("USE_MAILER", "__core.plugins.services.mailer", "Mailer"),
  ("USE_POSTGRES", "__core.plugins.database.postgresql", "PostgreSQL"),
  ("USE_SQLITE", "__core.plugins.database.sqlite", "SQLite"),
  ("USE_REDIS", "__core.plugins.cache.redis", "Redis"),
  ("USE_MEMORY", "__core.plugins.cache.memory", "Memory"),
]

class Server:
  def __init__(self, port: int = 8080, host: str = "localhost"):
    self.__port = sys.argv[1] if len(sys.argv) > 1 else port
    self.__host = sys.argv[2] if len(sys.argv) > 2 else host

  def listen(self) -> None:
    Env.Init()
    if Env.Get("LAZY_LOAD") != "1":
      enable_compression = Env.Get("ENABLE_VIEW_COMPRESSION") == "1"
      View.Init(use_compression=enable_compression)

    for plugin in PLUGINS:
      if Env.Get(plugin[0]) == "1":
        module = getattr(__import__(plugin[1]), "plugins")
        attrs = plugin[1].split(".")[2:]
        for attr in attrs:
          module = getattr(module, attr)

        module = getattr(module, plugin[2])
        module.Init()


    app = Flask(__name__, static_folder="../../public/static", static_url_path="")
    app.config["SESSION_PERMANENT"] = Env.Get("SESSION_PERMANENT") == "1"
    app.config["SESSION_TYPE"] = Env.Get("SESSION_TYPE") or "filesystem"
    if app.config["SESSION_TYPE"] == "redis":
      app.config["SESSION_REDIS"] = Redis.GetClient()

    Session(app)

    @app.errorhandler(Exception)
    def handle_exception(e: Exception):
      print(e.__str__())
      print("".join(traceback.format_tb(e.__traceback__)))
      return View("error").render({
        "reason": e.__str__(),
        "stacktrace": "".join(traceback.format_tb(e.__traceback__)),
      })


    for file in os.listdir("src/routes"):
      if file.endswith(".py"):
        file = file[:-3]
        bp = getattr(getattr(__import__(f"routes.{file}"), file), "routes")
        app.register_blueprint(bp)

    app.run(self.__host, self.__port)
