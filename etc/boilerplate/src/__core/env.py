import os

class InvalidEnvironmentException(Exception):
  def __init__(self, var: str):
    super().__init__(f"Invalid enviroment variable {var}")


class Env:
  __DATA = {}

  @staticmethod
  def Init() -> None:
    if os.path.isfile(".env"):
      with open(".env", "r") as file:
        lines = file.read().strip().split("\n")
        for line in lines:
          cols = line.strip().split("=")
          if len(cols) == 2:
            Env.__DATA[cols[0]] = cols[1].replace("\"", "").replace("'", "")

  @staticmethod
  def Get(key: str, default: str = None) -> str | None:
    return Env.__DATA.get(key) or os.getenv(key, default)

  @staticmethod
  def IsEnabled(key: str) -> bool:
    Env.Get(key) == "1"
