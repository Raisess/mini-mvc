# Plugins

### Available plugins

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

Thats all for postgres!

### Importing and using a plugin

Once you enabled a plugin in the `.env` file you can easily import it on the code
and create a instance as provider.

There's a example of how to use the google oauth2 plugin to create an authentication
controller.

```python
# src/app/controllers/auth_controller.py
from __core.controller import Controller
from __core.plugins.auth import GoogleOAuth2

REDIRECT_URI = "http://localhost:8080/auth/callback"

class AuthController(Controller):
    def auth(self) -> None:
        auth_provider = GoogleOAuth2()
        authorization_url = auth_provider.get_authorization_url(REDIRECT_URI)
        return self.redirect(authorization_url)

    def callback(self) -> None:
        arguments = self.request().args()
        authorization_code = arguments.get("code") 

        auth_provider = GoogleOAuth2()
        credentials = auth_provider.get_authorized_credentials(REDIRECT_URI, authorization_code)
        self.session().add("google_oauth2_token", credentials.token)
        return self.redirect("/")

    def logout(self) -> None:
        self.session().clear()
        return self.redirect("/")


# src/routes/auth_routes.py
from app.controllers import AuthController

controller = AuthController("auth_routes", __name__)
routes = controller.router()

@routes.get("/auth")
def auth():
    return controller.auth()


@routes.get("/auth/callback")
def auth_callback():
    return controller.callback()


@routes.get("/auth/logout")
def auth_callback():
    return controller.logout()
```
