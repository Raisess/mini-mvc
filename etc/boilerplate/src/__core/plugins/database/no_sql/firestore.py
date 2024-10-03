# @NOTE: To use this implementation you need to add the `firebase-admin` package to
# `requirements.txt`
# @REFERENCE: https://github.com/firebase/firebase-admin-python

from __core.env import Env
from __core.exceptions import InvalidEnvironmentException, NotConnectedException
from __core.plugins.database.no_sql.database import NoSQLDatabase

class Firestore(NoSQLDatabase):
  __CLIENT = None

  @staticmethod
  def Init():
    if Firestore.__CLIENT:
      return

    credentials_path = Env.Get("GCLOUD_CREDENTIALS_PATH")
    if not credentials_path:
      raise InvalidEnvironmentException("GCLOUD_CREDENTIALS_PATH")

    from firebase_admin import credentials, initialize_app, firestore
    credentials_data = credentials.Certificate(credentials_path)
    initialize_app(credentials_data)
    Firestore.__CLIENT = firestore.client()

  @staticmethod
  def __GetClient() -> any:
    if not Firestore.__CLIENT:
      raise NotConnectedException("Firestore", "USE_FIRESTORE")

    return Firestore.__CLIENT

  def expose(self) -> any:
    return Firestore.__GetClient()

  def add(self, collection: str, data: dict, id: str = None) -> str:
    client = Firestore.__GetClient()
    (_, result) = client.collection(collection).add(data, id)
    return result.id

  def get(self, collection: str, id: str) -> dict | None:
    client = Firestore.__GetClient()
    document = client.collection(collection).document(id)
    return document.get().to_dict()

  def list_by(self, collection: str, key: str = None, value: str | int = None) -> list[dict]:
    client = Firestore.__GetClient()
    if not key:
      data = client.collection(collection).get()
      return [item.to_dict() for item in data]

    from google.cloud.firestore import FieldFilter
    data = client.collection(collection).where(filter=FieldFilter(key, "==", value)).stream()
    return [item.to_dict() for item in data]

  def remove(self, collection: str, id: str) -> None:
    client = Firestore.__GetClient()
    document = client.collection(collection).document(id)
    document.delete()
