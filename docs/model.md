# Model

### Creating a new model

You can generate a controller by using the command:

```shell
mini-mvc gen model task
```

And it will look like this:

```python
from __core.model as model

@model.dataclass
class TaskModel(model.Model):
  id: str = model.field(default_factory=model.Model.GenUUID)
  created_at: str = model.field(default_factory=model.Model.GetTime)
  updated_at: str = model.field(default_factory=model.Model.GetTime)
```

- `id`: is a v4 `UUID`;
- `created_at`: `UTC` iso datetime;
- `updated_at`: `UTC` iso datetime

now you can add your model properties to it.

### Base methods

All models that derives from `model.Model`, will have those base methods:

- `to_dict`: transform the model into a dictionary:

```python
my_task = TaskModel()
print(my_task.to_dict())
```

- `to_json`: transform the model into a json string:

```python
my_task = TaskModel()
print(my_task.to_json())
```

### Static methods

Models also have soem base methods to act like models factories,
here are some examples:

- `FromDict`: transform a dict into a model:

```python
# This will generate a task model with the property name = my_task,
# if the model has the `name` property.
TaskModel.FromDict(TaskModel, { "name": "my_task" })
```

- `FromJSON`: transform a json string into a model:

```python
TaskModel.FromJSON(TaskModel, "{ \"name\": \"my_task\" }")
```
