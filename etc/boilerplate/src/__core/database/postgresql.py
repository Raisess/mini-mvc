from postgres import Postgres

from __core.env import Env

class NotConnectedException(Exception):
  def __init__(self):
    super().__init__("PostgreSQL database not connected")


class InvalidEnvironmentException(Exception):
  def __init__(self, option: str):
    super().__init__(f"Invalid PostgreSQL database option {option}")


class PostgresDatabase:
  __CONN: Postgres = None

  @staticmethod
  def Init():
    username = Env.Get("POSTGRES_USER")
    if not username: raise InvalidEnvironmentException("POSTGRES_USER")
    password = Env.Get("POSTGRES_PASS")
    if not password: raise InvalidEnvironmentException("POSTGRES_PASS")
    hostname = Env.Get("POSTGRES_HOST")
    if not hostname: raise InvalidEnvironmentException("POSTGRES_HOST")
    port = Env.Get("POSTGRES_PORT")
    if not port: raise InvalidEnvironmentException("POSTGRES_PORT")
    dbname = Env.Get("POSTGRES_DBNAME")
    if not dbname: raise InvalidEnvironmentException("POSTGRES_DBNAME")

    url = f"postgresql://{username}:{password}@{hostname}:{port}/{dbname}"
    PostgresDatabase.__CONN = Postgres(url=url)

  def void_query(self, sql: str, values: dict[str, any] | None = None) -> None:
    if not PostgresDatabase.__CONN:
      raise NotConnectedException()

    PostgresDatabase.__CONN.run(sql, vaules)

  def query(self, sql: str, values: dict[str, any] | None = None) -> list[any]:
    if not PostgresDatabase.__CONN:
      raise NotConnectedException()

    return PostgresDatabase.__CONN.all(sql, values)
