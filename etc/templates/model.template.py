import __core.model as model

@model.dataclass
class {{name}}Model(model.Model):
  id: str = model.field(default_factory=model.Model.GenUUID)
  created_at: str = model.field(default_factory=model.Model.GetTime)
  updated_at: str = model.field(default_factory=model.Model.GetTime)

  @staticmethod
  def FromDict(data: dict) -> "{{name}}Model":
    return model.Model._FromDict({{name}}Model, data)

  @staticmethod
  def FromJSON(data: str) -> "{{name}}Model":
    return model.Model._FromJSON({{name}}Model, data)
