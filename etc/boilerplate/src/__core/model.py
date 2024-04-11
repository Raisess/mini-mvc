import json
# @NOTE: field is imported just to export from here to model implementation
from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

@dataclass
class Model:
  @staticmethod
  def GenUUID() -> str:
    return str(uuid4())

  @staticmethod
  def GetTime() -> str:
    return datetime.utcnow().isoformat()

  @staticmethod
  def _FromDict(Class: "Model", data: dict) -> "Model":
    model = Class()
    for (key, value) in dict.items(data):
      model.__dict__[key] = value

    return model

  @staticmethod
  def _FromJSON(Class: "Model", data: str) -> "Model":
    return Model._FromDict(Class, json.loads(data))

  def to_dict(self) -> dict:
    return self.__dict__

  def to_json(self) -> str:
    return json.dumps(
      self,
      default=lambda o: o.__dict__,
      sort_keys=True,
      indent=2
    )
