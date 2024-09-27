class NotConnectedException(Exception):
  def __init__(self, plugin: str, env: str):
    super().__init__(f"{plugin} plugin not connected, check {env} environment variable")


class InvalidEnvironmentException(Exception):
  def __init__(self, var: str):
    super().__init__(f"Invalid enviroment variable {var}")
