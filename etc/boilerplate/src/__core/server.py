import importlib
import logging
import os
import sys
import traceback

from flask import Flask

from __core.env import Env
from __core.logger import Logger
from __core.view import View

# @NOTE: Each plugin needs to have an static `Init` method
PLUGINS = [
  # Services
  ("USE_MAILER", "__core.plugins.services.mailer", "Mailer"),

  # SQL Databases
  ("USE_POSTGRES", "__core.plugins.database.sql.postgresql", "PostgreSQL"),
  ("USE_SQLITE", "__core.plugins.database.sql.sqlite", "SQLite"),

  # NOSQL Databases
  ("USE_FIRESTORE", "__core.plugins.database.no_sql.firestore", "Firestore"),

  # Cache
  ("USE_REDIS", "__core.plugins.cache.redis", "Redis"),
  ("USE_MEMORY", "__core.plugins.cache.memory", "Memory"),

  # Auth
  ("USE_GOOGLE_OAUTH2", "__core.plugins.auth.google_oauth2", "GoogleOAuth2"),
]

class Server:
  def __init__(self, port: int = 8080, host: str = "localhost"):
    self.__port = sys.argv[1] if len(sys.argv) > 1 else port
    self.__host = sys.argv[2] if len(sys.argv) > 2 else host

    Env.Init(".env.production" if Env.IsEnabled("PRODUCTION") else ".env")
    if not Env.IsEnabled("LAZY_LOAD"):
      View.Init(use_compression=Env.IsEnabled("ENABLE_VIEW_COMPRESSION"))

    for (flag, path, name) in PLUGINS:
      if Env.IsEnabled(flag):
        module = getattr(importlib.import_module(path), name)
        module.Init()


    app = Flask(__name__, static_folder="../../public/static", static_url_path="")
    if Env.IsEnabled("USE_SESSION"):
      from flask_session import Session

      app.config["SESSION_PERMANENT"] = Env.IsEnabled("SESSION_PERMANENT")
      app.config["SESSION_TYPE"] = Env.Get("SESSION_TYPE", "filesystem")
      if app.config["SESSION_TYPE"] == "redis":
        from __core.plugins.cache.redis import Redis
        app.config["SESSION_REDIS"] = Redis.GetClient()

      Session(app)

    render_exception_stack = Env.IsEnabled("RENDER_EXCEPTION_STACK")
    @app.errorhandler(Exception)
    def handle_exception(ex: Exception):
      Logger.Error("Internal Server Error", ex)
      return View("error").render({
        "reason": ex.__str__(),
        "stacktrace": "".join(traceback.format_tb(ex.__traceback__)) if render_exception_stack else None,
      })


    for file in os.listdir("src/routes"):
      if file.endswith(".py"):
        file = file[:-3]
        bp = getattr(getattr(__import__(f"routes.{file}"), file), "routes")
        app.register_blueprint(bp)

    if Env.IsEnabled("USE_SCHEDULER"):
      for file in os.listdir("src/scheduler"):
        if file.endswith(".py"):
          file = file[:-3]
          scheduler = getattr(getattr(__import__(f"scheduler.{file}"), file), "scheduler")
          scheduler.start()

    self.__app = app

  def listen(self) -> None:
    logger = self.__app.logger
    logger.setLevel(Env.Get("LOG_LEVEL"))
    self.__app.run(self.__host, self.__port, debug=Env.IsEnabled("DEBUG"))

  def expose(self) -> Flask:
    return self.__app

  def host(self) -> str:
    return self.__host

  def port(self) -> int:
    return self.__port
