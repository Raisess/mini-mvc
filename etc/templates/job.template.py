from __core.scheduler import Job

class {{name}}Job(Job):
  def __init__(self):
    super().__init__("{{name}}", interval_minutes=1)

  def run(self) -> None:
    pass
