class NotConnectedException(Exception):
  def __init__(self, database: str, env: str):
    super.__init__(f"{database} plugin not connected, check {env} environment variable")


class InvalidEnvironmentException(Exception):
  def __init__(self, var: str):
    super().__init__(f"Invalid enviroment variable {var}")
