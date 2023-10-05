import json
from dataclasses import asdict, dataclass, field
from uuid import uuid4

@dataclass
class Model:
  @staticmethod
  def GenUUID() -> str:
    return str(uuid4())

  def to_dict(self) -> dict:
    return asdict(self)

  def to_json(self) -> str:
    return json.dumps(
      self,
      default=lambda o: o.__dict__,
      sort_keys=True,
      indent=2
    )
