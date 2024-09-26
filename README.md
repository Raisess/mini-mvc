# Mini MVC

Model-View-Controller made easy, keeping it simple.

#### Features:

- OAuth2 authentication plugin:
    - Google
- Relational databases integration:
    - PostgreSQL
    - SQLite
- No relational databases integration:
    - Firestore
- Fast memory access databases:
    - Redis
    - Memory caching
- SMTP client for sending email's;
- View's and email's templating using `Jinja2`

Check all our plugins [here](/docs/PLUGINS.md).

### Installing the CLI:

```shell
$ git clone https://github.com/Raisess/mini-mvc.git
$ cd mini-mvc && ./install.py
```

### Creating and running your project:

```shell
$ mini-mvc init my-project
$ cd my-project
$ ./src/main.py
```

- Configuration ENV's:
    - `USE_SESSION`: Enable the application to store sessions data;
    - `SESSION_PERMANENT`: Indicates if the session will live forever, default: `0`;
    - `SESSION_TYPE`: Select the session store type, default: `filesystem`;
    - `LAZY_LOAD`: When disabled will store all views in the application memory, default: `0`
    - check `.env.example` file for more variables

### Generating resources:

```shell
$ mini-mvc gen controller|model|view <name>
```

Or

```shell
$ mini-mvc gen controller|model|view <namespace>/<name>
```
