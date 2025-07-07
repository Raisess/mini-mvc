# Repository

### Creating a new repository

You can generate a repository by using the command:

```shell
mini-mvc gen repository task
```

And it will look like this:

```python
from __core.repository import Repository
from app.models import TaskModel

class TaskRepository(Repository):
  def create(self, data: TaskModel) -> str:
    raise NotImplemented()

  def update(self, id: str, new_data: TaskModel) -> None:
    raise NotImplemented()

  def find_one(self, id: str) -> TaskModel | None:
    raise NotImplemented()

  def find(self, filter: dict) -> list[TaskModel]:
    raise NotImplemented()

  def remove_one(self, id: str) -> None:
    raise NotImplemented()

  def remove(self, filter: dict) -> None:
    raise NotImplemented()
```

the repositories usually depends on a model, so it will assume will already
have a model for that new repository, check the [model](/docs/model.md) section.

### Base methods

The repository is just a simple wrapper for database queries, so it don't have
any complex base method to be described, we can procced to an implementation example.

### Example

In this example we'are assuming you already have `postgresql` instance running
and configured the plugin, check the [section](/docs/plugins/database/sql.md) for help.

This repository can create and find tasks from the `task` table of a `postgresql`
database, notice that we're are using a internal plugin for communicate with the database.

```python
from __core.repository import Repository
from __core.plugins.database.sql import PostgreSQL

from app.models import TaskModel

class TaskRepository(Repository):
  def __init__(self):
    self.__db = PostgreSQL()
    self.__table = "tasks"

  def create(self, data: TaskModel) -> str:
    self.__db.insert(self.__table, data.to_dict())

  def find_one(self, id: str) -> TaskModel | None:
    results = self.__db.select(self.__table, { "id": id })
    return TaskRepository.__format(results[0]) if len(results) > 0 else None

  @staticmethod
  def __format(data: dict) -> TaskModel:
    return TaskModel(
      id=data.get("id"),
      created_at=str(data.get("created_at")),
      updated_at=str(data.get("updated_at")),
      name=data.get("name"),
    )
```

The static `__format` method makes the conversion from the database data types
into model compatible ones, you need to do that to ensure model standards.
