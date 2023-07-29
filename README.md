# Mini MVC

### Creating and running your project:

```shell
$ mini-mvc init my-project
$ cd my-project
$ ./src/main.py
```

- Configuration ENV's:
    - `SESSION_PERMANENT`: Indicates if the session will live forever, default: `0`;
    - `SESSION_TYPE`: Select the session store type, default: `filesystem`;
    - `LAZY_LOAD`: When disabled will store all views in the application memory, default: `0`.

### Generating resources:

```shell
$ mini-mvc gen controller|model|view <name>
```

Or

```shell
$ mini-mvc gen controller|model|view <namespace>/<name>
```
