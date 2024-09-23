# @NOTE: To use this implementation you need to add the `postgres` package to
# `requirements.txt`
# @REFERENCE: https://github.com/liberapay/postgres.py

from postgres import Postgres

from __core.env import Env, InvalidEnvironmentException
from __core.plugins.database.database import Database

class NotConnectedException(Exception):
  def __init__(self):
    super().__init__("PostgreSQL database not connected")


class PostgreSQL(Database):
  __CONN: Postgres = None

  @staticmethod
  def Init():
    if PostgreSQL.__CONN:
      return

    username = Env.Get("POSTGRES_USER")
    if not username:
      raise InvalidEnvironmentException("POSTGRES_USER")

    password = Env.Get("POSTGRES_PASS")
    if not password:
      raise InvalidEnvironmentException("POSTGRES_PASS")

    hostname = Env.Get("POSTGRES_HOST")
    if not hostname:
      raise InvalidEnvironmentException("POSTGRES_HOST")

    port = Env.Get("POSTGRES_PORT")
    if not port:
      raise InvalidEnvironmentException("POSTGRES_PORT")

    dbname = Env.Get("POSTGRES_DBNAME")
    if not dbname:
      raise InvalidEnvironmentException("POSTGRES_DBNAME")

    url = f"postgresql://{username}:{password}@{hostname}:{port}/{dbname}"
    PostgreSQL.__CONN = Postgres(url=url)

  def void_query(self, sql: str, values: dict[str, any] | tuple[any] | None = None) -> None:
    if not PostgreSQL.__CONN:
      raise NotConnectedException()

    PostgreSQL.__CONN.run(sql, vaules)

  def query(self, sql: str, values: dict[str, any] | tuple[any] | None = None) -> list[any]:
    if not PostgreSQL.__CONN:
      raise NotConnectedException()

    return PostgreSQL.__CONN.all(sql, values)
