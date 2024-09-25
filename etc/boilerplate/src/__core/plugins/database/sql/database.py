class SQLDatabase:
  def void_query(self, sql: str, values: dict[str, any] | tuple[any] | None = None) -> None:
    raise NotImplemented()

  def query(self, sql: str, values: dict[str, any] | tuple[any] | None = None) -> list[any]:
    raise NotImplemented()
