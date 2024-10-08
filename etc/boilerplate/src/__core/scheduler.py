class Job:
  def __init__(self, name: str, interval_minutes: float):
    self.__name = name
    self.__interval_minutes = interval_minutes

  def name(self) -> str:
    return self.__name

  def interval_minutes(self) -> float:
    return self.__interval_minutes

  def run(self) -> None:
    raise NotImplemented()


class Scheduler:
  def __init__(self):
    self.__jobs: dict[str, Job] = {}

  def add(self, job: Job):
    if self.__jobs.get(job.name()) != None:
      raise Exception("Job already registered")

    self.__jobs[job.name()] = job

  def start(self) -> None:
    from apscheduler.schedulers.background import BackgroundScheduler

    aps = BackgroundScheduler()
    for job in self.__jobs.values():
      aps.add_job(job.run, "interval", minutes=job.interval_minutes())

    if len(self.__jobs.keys()) > 0:
      aps.start()
