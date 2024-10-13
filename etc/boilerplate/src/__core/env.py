import os

class Env:
  __DATA = {}

  @staticmethod
  def Init(filename: str = ".env") -> None:
    if os.path.isfile(filename):
      with open(filename, "r") as file:
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
    value = Env.Get(key)
    return value == "1" or value == 1
