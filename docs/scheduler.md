# Scheduler

### Creating asynchronous background jobs

To create a new job just generate the file using the command:

```shell
$ mini-mvc gen job my_test
```

This will create the file:

```python
# src/app/jobs/my_test.py

class MyTestJob(Job):
  def __init__(self):
    super().__init__("MyTest", interval_minutes=1) # You also can use crontab parameter to especify execution time

  def run(self) -> None:
    pass
```

and you can edit the run method to execute your background routine.

### Adding the job to the scheduler

You can create a new scheduler file into the `src/scheduler` folder or just add
your job to the `src/scheduler/jobs.py` file, just by adding some new lines:

```python
# src/app/scheduler/jobs.py

from __core.scheduler import Scheduler

from app.jobs import MyTestJob

scheduler = Scheduler()
scheduler.add(MyTestJob())
```
