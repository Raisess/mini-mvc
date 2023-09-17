from dataclasses import dataclass, field
from uuid import uuid4

@dataclass
class Model:
  @staticmethod
  def GenUUID() -> str:
    return str(uuid4())
