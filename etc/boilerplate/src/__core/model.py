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
  def FromDict(ModelClass: "Model", data: dict) -> "Model":
    model = ModelClass()
    for (key, value) in dict.items(data):
      model.__dict__[key] = value

    return model

  @staticmethod
  def FromJSON(ModelClass: "Model", data: str) -> "Model":
    return Model.FromDict(ModelClass, json.loads(data))

  def to_dict(self) -> dict:
    """
    @WARNING: This method drop the keys with the `fk_` prefix, this is to
    obfuscate foreign key returned data, so if you have that type of data in
    your model I'd recommend to use `fk_` prefix on it.
    """
    dictionare = self.__dict__
    for key in list(dictionare.keys()):
      if key.startswith("fk_"):
        dictionare.pop(key)

    return dictionare

  def to_json(self) -> str:
    return json.dumps(
      self,
      default=lambda o: o.__dict__,
      sort_keys=True,
      indent=2
    )
