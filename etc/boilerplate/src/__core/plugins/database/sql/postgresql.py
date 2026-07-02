from __core.env import Env
from __core.exceptions import InvalidEnvironmentException, NotConnectedException
from __core.plugins.database.sql.database import SQLDatabase

class PostgreSQL(SQLDatabase):
  """
  @FLAG: USE_POSTGRES

  Required ENV's:
    - POSTGRES_USER: the authentication username
    - POSTGRES_PASS: the authentication password
    - POSTGRES_HOST: the instance host, without the protocol, e.g.: localhost
    - POSTGRES_PORT: the instance port the database is running on
    - POSTGRES_DBNAME: the name of the database that the application will use

  @NOTE: To use this implementation you need to add the `postgres==4.0` package to
  `requirements.txt`

  @REFERENCE: https://github.com/liberapay/postgres.py
  """
  __CONN = None

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

    from postgres import Postgres
    url = f"postgresql://{username}:{password}@{hostname}:{port}/{dbname}"
    PostgreSQL.__CONN = Postgres(url=url)

  def void_query(self, sql: str, values: dict[str, any] | tuple[any] | None = None) -> None:
    if not PostgreSQL.__CONN:
      raise NotConnectedException("PostgreSQL", "USE_POSTGRES")

    PostgreSQL.__CONN.run(sql, values)

  def query(self, sql: str, values: dict[str, any] | tuple[any] | None = None) -> list[dict]:
    if not PostgreSQL.__CONN:
      raise NotConnectedException("PostgreSQL", "USE_POSTGRES")

    results = PostgreSQL.__CONN.all(sql, values)
    return [item._asdict() for item in results]

  def plain(self, sql: str, values: dict[str, any] | tuple[any] | None = None) -> list[any]:
    if not PostgreSQL.__CONN:
      raise NotConnectedException("PostgreSQL", "USE_POSTGRES")

    return PostgreSQL.__CONN.all(sql, values)
