# Plugins

### About

The plugins are implementation of things that 90% of the Web Applications will
need, so why write it every time you need a new project?

If you have a plugin suggestion feel free to open a Issue or a Pull Request!

### Available plugins

- Mailer
- SQL Databases:
    - PostgreSQL
    - SQLite
- No SQL Databases:
    - Firestore
- Cache:
    - Local memory
    - Redis
- OAuth2:
    - Google Auth

### Enabling a plugin

To enable a plugin you can check for the `USE_<PLUGIN>` on the `.env.example`
file, change the value to 1 and fill the required plugin fields that will be
also on the env file.

Example of enabling PostgreSQL plugin with a local database:

```shell
USE_POSTGRES=1
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=user
POSTGRES_PASS=pass
POSTGRES_DBNAME=mydb
```
