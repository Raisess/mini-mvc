# SQL Database

### Available SQL databases and how to connect

The list below shows the currently available sql databases implementations:

- [PostgreSQL](/etc/boilerplate/src/__core/plugins/database/sql/postgresql.py)
    - For connecting with a `PostgreSQL` you will need 6 environment variables:
        - `USE_POSTGRES`: the value should be 1 to enable and 0 to disable;
        - `POSTGRES_DBNAME`: the database name you want to use for performing queries,
        it should exists on the database, otherwise the queries will fail;
        - `POSTGRES_HOST`: the database host;
        - `POSTGRES_PORT`: the database port;
        - `POSTGRES_USER`: the database user;
        - `POSTGRES_PASS`: the database pass

- [SQLite](/etc/boilerplate/src/__core/plugins/database/sql/sqlite.py)
    - For connecting with a `SQLite` you only need 2 environment variables:
        - `USE_SQLITE`: the value enables or disable the plugin, same as `PostgreSQL`;
        - `SQLITE_DB_PATH`: the path of the data file, where it will be stored, can also be `:memory`

All of then derive from the same base class [SQLDatabase](/etc/boilerplate/src/__core/plugins/database/sql/database.py)
this class is responsible for implementation signature and expose the main
methods for making sql queries: `void_query`, `query` and `plain` it also
implements the `ORM` methods that will boost your repositories development.

### Core methods

#### void_query

The `void_query` method is a method that you should use for making queries that
the results do not actually matter, such an insert without result, cause this method return nothing.

```python
db = SQLite()
db.void_query("INSERT INTO my_table(name) VALUES(:name);", { "name": "test" })

db = PostgreSQL()
db.void_query("INSERT INTO my_table(name) VALUES(%(name)s);", { "name": "test" })
```

You can notice that is some diferences between the two queries, we can normalize
this using the `ORM` methods.

#### query

`query` is the method you will use, is for making all types of sql queries that
will return something.

```python
db = SQLite()
db.query("SELECT * FROM my_table WHERE NAME = :name;", { "name": "test" })

db = PostgreSQL()
db.query("SELECT * FROM my_table WHERE NAME = %(name)s;", { "name": "test" })
```

Both returns will be a `list[dict]`.

#### plain

The `plain` method is just like the `query` method but instead of returning a dict,
it will return the value like how it was supposed to be, this is util when will need to make
a query like this:

```sql
SELECT COUNT(1) FROM my_table;
```

### ORM methods

SQL is a really standard language, so you can use the same query for some different database engines,
with that in mind, you can generate queries for simple tasks based on what parameters will need to pass.

#### select

The most complex queries will be selects, when you have a lot parameters in your `WHERE` clause,
with this method you can simplify that a lot.

```python
db = PostgreSQL()
db.select(
    table="my_table",
    columns=["name", "timestamp"],
    where={ "name": "test" },
    order_by={ "timestamp": "desc" },
    limit=100,
    offset=0,
)
```

The executed query will be something like this:

```sql
SELECT name, timestamp FROM my_table WHERE name = ? ORDER BY timestamp DESC LIMIT 100 OFFSET 0;
```

#### insert

Simple row insert:

```python
db = PostgreSQL()
db.insert("my_table", { "name": "test" })
```

Until now there's no batch insertion method, but it will be available on the future.

#### update

```python
db = PostgreSQL()
db.update("my_table", where={ "name": "test" }, values={ "name": "new name" })
```

You can use an empty `dict` on where for updating all rows.

#### delete

```python
db = PostgreSQL()
db.delete("my_table", where={ "name": "new name" })
```

You can use an empty `dict` on where for deleting all rows.
