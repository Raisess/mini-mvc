import os
import sys
import traceback

from flask import Flask
from flask_session import Session

from core.view import View

class Server:
  def __init__(self, port: int = 8080, host: str = "localhost"):
    self.__port = sys.argv[1] if len(sys.argv) > 1 else port
    self.__host = sys.argv[2] if len(sys.argv) > 2 else host

  def listen(self) -> None:
    app = Flask(__name__, static_folder="../../public/static", static_url_path="")
    app.config["SESSION_PERMANENT"] = True if os.getenv("SESSION_PERMANENT") == "0" else False
    app.config["SESSION_TYPE"] = os.getenv("SESSION_TYPE") or "filesystem"
    Session(app)

    if not os.getenv("LAZY_LOAD") == "1":
      View.Init()

    @app.errorhandler(Exception)
    def handle_exception(e: Exception):
      print(e.__str__())
      print("".join(traceback.format_tb(e.__traceback__)))
      view = View("error")
      return view.render({
        "reason": e.__str__(),
        "stacktrace": "".join(traceback.format_tb(e.__traceback__)),
      })


    for file in os.listdir("src/routes"):
      if file.endswith(".py"):
        file = file[:-3]
        bp = getattr(getattr(__import__(f"routes.{file}"), file), "routes")
        app.register_blueprint(bp)

    app.run(self.__host, self.__port)
