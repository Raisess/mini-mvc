# @NOTE: To use this implementation you need to add the `firebase-admin` package to
# `requirements.txt`
# @REFERENCE: https://github.com/firebase/firebase-admin-python

from firebase_admin import credentials, initialize_app, firestore
from google.cloud.firestore import Client
# exporting
from google.cloud.firestore import DocumentReference, DocumentSnapshot

from __core.env import Env, InvalidEnvironmentException
from __core.plugins.database.no_sql.database import NoSQLDatabase

class NotConnectedException(Exception):
  def __init__(self):
    super.__init__("Firestore database not connected")


class Firestore(NoSQLDatabase):
  __CLIENT: Client = None

  @staticmethod
  def Init():
    if Firestore.__CLIENT:
      return

    credentials_path = Env.Get("GCLOUD_CREDENTIALS_PATH")
    if not credentials_path:
      raise InvalidEnvironmentException("GCLOUD_CREDENTIALS_PATH")

    credentials_data = credentials.Certificate(credentials_path)
    initialize_app(credentials_data)
    Firestore.__CLIENT = firestore.client()

  def expose(self) -> Client:
    if not Firestore.__CLIENT:
      raise NotConnectedException()

    return Firestore.__CLIENT
