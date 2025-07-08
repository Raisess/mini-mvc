class SQLDatabase:
  def void_query(self, sql: str, values: dict[str, any] | tuple[any] | None = None) -> None:
    raise NotImplemented()

  def query(self, sql: str, values: dict[str, any] | tuple[any] | None = None) -> list[dict]:
    raise NotImplemented()

  def plain(self, sql: str, values: dict[str, any] | tuple[any] | None = None) -> list[any]:
    raise NotImplemented()

  def insert(self, table: str, values: dict[str, any]) -> None:
    mapper = self.__mapper()
    keys = values.keys()
    _columns = ", ".join(keys)
    _values = ", ".join([mapper for key in keys])
    query = f"INSERT INTO {table}({_columns}) VALUES({_values})"
    self.void_query(query, list(values.values()))

  def batch_insert(self, table: str, pk: str | None, values: list[dict[str, any]]) -> None:
    mapper = self.__mapper()

    _columns = ", ".join(values[0].keys())
    batch = []
    item_list_values = []
    for item in values:
      _values = ", ".join([mapper for key in item.keys()])
      batch.append(_values)
      item_list_values.extend(list(item.values()))

    _values = "), (".join(batch)
    query = f"INSERT INTO {table}({_columns}) VALUES({_values})"
    if pk:
      query += f" ON CONFLICT({pk}) DO NOTHING"

    self.void_query(query, item_list_values)

  def update(self, table: str, where: dict[str, any], values: dict[str, any]) -> None:
    mapper = self.__mapper()
    _values = ", ".join([f"{key} = {mapper}" for key in values.keys()])
    _where = " AND ".join([f"{key} = {mapper}" for key in where.keys()])
    query = f"UPDATE {table} SET {_values} WHERE {_where}"

    self.void_query(query, list(values.values()) + list(where.values()))

  def delete(self, table: str, where: dict[str, any]) -> None:
    mapper = self.__mapper()
    _where = " AND ".join([f"{key} = {self.__mapper()}" for key in where.keys()])
    query = f"DELETE FROM {table} WHERE {_where}"
    self.void_query(query, list(where.values()))

  def select(
    self,
    table: str,
    where: dict[str, any] = None,
    columns: list[str] = None,
    order_by: dict[str, str] = None,
    limit: int = None,
    offset: int = None
  ) -> list[dict]:
    OPERATORS = ["=", "<=", ">=", "<", ">", "<>"]

    mapper = self.__mapper()
    _columns = ", ".join(columns) if columns and len(columns) > 0 else "*"

    query = f"SELECT {_columns} FROM {table}"
    if where:
      _where = []
      for (key, value) in where.items():
        if value == None:
          _where.append(f"{key} IS NULL")
        elif isinstance(value, list):
          _in = ", ".join([f"{mapper}" for i in value])
          _where.append(f"{key} IN({_in})")
        elif isinstance(value, tuple):
          if value[0] in OPERATORS:
            _where.append(f"({key} {value[0]} {mapper})")
          else:
            _where.append(f"({key} BETWEEN {mapper} AND {mapper})")
        else:
          _where.append(f"{key} = {mapper}")

      _where = "WHERE " + " AND ".join(_where) if len(_where) > 0 else ""
      query += f" {_where}"
    if order_by:
      _order_by = ", ".join([f"{key} {value}" for (key, value) in order_by.items()])
      query += f" ORDER BY {_order_by}"
    if limit:
      query += f" LIMIT {limit}"
    if offset:
      query += f" OFFSET {offset}"

    values = []
    if where:
      for item in where.values():
        if isinstance(item, tuple) or isinstance(item, list):
          if item[0] in OPERATORS:
            values.append(item[1])
          else:
            values.extend(item)
        elif value != None:
          values.append(item)

    return self.query(query, values)

  def __mapper(self) -> str:
    from __core.plugins.database.sql import PostgreSQL, SQLite
    if isinstance(self, PostgreSQL):
      return "%s"
    elif isinstance(self, SQLite):
      return "?"
    else:
      raise Exception("Invalid sql mapper")
