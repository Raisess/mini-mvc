class Job:
  def __init__(self, name: str, interval_minutes: float = None, crontab: str = None):
    if not interval_minutes and not crontab:
      raise Exception("You should provide one option: interval_minutes or crontab")

    if interval_minutes and crontab:
      raise Exception("You should provide only one option: interval_minutes or crontab")

    self.__name = name
    self.__interval_minutes = interval_minutes
    self.__crontab = crontab

  def name(self) -> str:
    return self.__name

  def interval_minutes(self) -> float | None:
    return self.__interval_minutes

  def crontab(self) -> str | None:
    return self.__crontab

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
    from apscheduler.triggers.cron import CronTrigger

    aps = BackgroundScheduler()
    for job in self.__jobs.values():
      if job.crontab() != None:
        aps.add_job(job.run, trigger=CronTrigger.from_crontab(job.crontab()), id=job.name())
      else:
        aps.add_job(job.run, "interval", minutes=job.interval_minutes(), id=job.name())

    if len(self.__jobs.keys()) > 0:
      aps.start()
