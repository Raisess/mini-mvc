import sqlite3

from __core.env import Env, InvalidEnvironmentException
from __core.plugins.database.database import Database

class NotConnectedException(Exception):
  def __init__(self):
    super().__init__("SQLite database not connected")


class SQLite(Database):
  __CONN = None

  @staticmethod
  def Init():
    if SQLite.__CONN:
      return

    path = Env.Get("SQLITE_DB_PATH")
    if not path:
      raise InvalidEnvironmentException("SQLITE_DB_PATH")

    SQLite.__CONN = sqlite3.connect(path)

  def void_query(self, sql: str, values: dict[str, any] | tuple[any] | None = []) -> None:
    if not SQLite.__CONN:
      raise NotConnectedException()

    cursor = SQLite.__CONN.cursor()
    cursor.execute(sql, values)
    SQLite.__CONN.commit()

  def query(self, sql: str, values: dict[str, any] | tuple[any] | None = []) -> list[any]:
    if not SQLite.__CONN:
      raise NotConnectedException()

    cursor = SQLite.__CONN.cursor()
    result = cursor.execute(sql, values)
    return result.fetchall()