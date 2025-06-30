# Google OAuth2

### About

The `GoogleOAuth2` plugin is a simple and fast way to implement authentication to your app,
you'll only need a feel lines of code and Google Account.

### Getting Started

First you'll need to setup a Google Cloud project to create your auth page,
after that you need to setup the API Client credentials, you can do it here: [apis/credentials](https://console.cloud.google.com/apis/credentials).

With the new credentials you can setup the `.env` file, like this:

```shell
USE_GOOGLE_OAUTH2=1
GOOGLE_OAUTH2_CLIENT_ID=<client-id>
GOOGLE_OAUTH2_CLIENT_SECRET=<client-key>
GOOGLE_OAUTH2_SCOPES="openid https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"
```

The `GOOGLE_OAUTH2_SCOPES` are the scopes you have setup as permissions for the client.
When you are creating the client, you'll need to setup a redirect URI, that URI can be your localhost
where the app is running while you're coding, or even the production/staging environment URI,
you also can setup allowed origins who can access your auth page.

### Creating an authentication controller

Once you enabled a plugin in the `.env` file you can easily import it on the code
and create a instance as provider.

There's a example of how to use it to create an authentication controller.

```python
# src/app/controllers/auth_controller.py
from __core.controller import Controller
from __core.plugins.auth import GoogleOAuth2

# The redirect URI you had setup while creating the Google Cloud client
REDIRECT_URI = "http://localhost:8080/auth/callback"

class AuthController(Controller):
    # Redirects the user to the Google authentication page
    def auth(self) -> None:
        auth_provider = GoogleOAuth2()
        authorization_url = auth_provider.get_authorization_url(REDIRECT_URI)
        return self.redirect(authorization_url)
    
    # Google will redirect your authentication request to here if it was successfull,
    # you can get the user `authorization_code`, with that you can retrieve the,
    # user `token` for fetching user data from the Google API's
    def callback(self) -> None:
        arguments = self.request().args()
        authorization_code = arguments.get("code") 

        auth_provider = GoogleOAuth2()
        # Needs to inform the `REDIRECT_URI` here as the allowed request origin
        token = auth_provider.get_authorized_token(REDIRECT_URI, authorization_code)
        # Save the user `token` on the session for getting the user data later
        self.session().add("google_oauth2_token", token)
        return self.redirect("/")

    # Clear the session data preveting the token to be stored forever
    # @NOTE: to use this you'll need `USE_SESSION` to enabled
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


# The same route as your `REDIRECT_URI`
@routes.get("/auth/callback")
def auth_callback():
    return controller.callback()


@routes.get("/auth/logout")
def auth_callback():
    return controller.logout()
```
