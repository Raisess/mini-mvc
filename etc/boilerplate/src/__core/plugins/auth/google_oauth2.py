from __core.env import Env
from __core.exceptions import InvalidEnvironmentException, NotConnectedException

class GoogleOAuth2:
  """
  @FLAG: USE_GOOGLE_OAUTH2

  Required ENV's:
    - GOOGLE_OAUTH2_CLIENT_ID: your GCP project client id string
    - GOOGLE_OAUTH2_CLIENT_SECRET: your GCP project client secret
    - GOOGLE_OAUTH2_SCOPES: the scopes that will be enabled for that client

  @NOTE: To use this implementation you need to add the `google-auth-oauthlib==1.4.0` package to
  `requirements.txt`

  @REFERENCE: https://github.com/googleapis/google-auth-library-python-oauthlib
  """
  __STARTED = False
  __CLIENT = None

  @staticmethod
  def Init():
    if GoogleOAuth2.__STARTED:
      return

    GoogleOAuth2.__STARTED = True

  @staticmethod
  def __GetClient(state: str = None) -> any:
    if not GoogleOAuth2.__STARTED:
      raise NotConnectedException("GoogleOAuth2", "USE_GOOGLE_OAUTH2")

    if GoogleOAuth2.__CLIENT is not None:
      return GoogleOAuth2.__CLIENT

    client_id = Env.Get("GOOGLE_OAUTH2_CLIENT_ID")
    if not client_id:
      raise InvalidEnvironmentException("GOOGLE_OAUTH2_CLIENT_ID")

    client_secret = Env.Get("GOOGLE_OAUTH2_CLIENT_SECRET")
    if not client_id:
      raise InvalidEnvironmentException("GOOGLE_OAUTH2_CLIENT_SECRET")

    scopes = Env.Get("GOOGLE_OAUTH2_SCOPES")
    if not scopes:
      raise InvalidEnvironmentException("GOOGLE_OAUTH2_SCOPES")

    from google_auth_oauthlib.flow import InstalledAppFlow
    GoogleOAuth2.__CLIENT = InstalledAppFlow.from_client_config(
      client_config={
        "web": {
          "client_id": client_id,
          "client_secret": client_secret,
          "auth_uri": "https://accounts.google.com/o/oauth2/auth",
          "token_uri": "https://accounts.google.com/o/oauth2/token"
        },
      },
      scopes=scopes,
      state=state
    )
    return GoogleOAuth2.__CLIENT

  def get_authorization_url(self, redirect_uri: str, state: str = None) -> str:
    from google_auth_oauthlib.flow import InstalledAppFlow

    client: InstalledAppFlow = GoogleOAuth2.__GetClient(state)
    client.redirect_uri = redirect_uri
    (authorization_url, _state) = client.authorization_url(
      access_type="offline",
      prompt="select_account"
    )
    return authorization_url

  def get_authorized_token(self, from_uri: str, authorization_code: str) -> str:
    from google_auth_oauthlib.flow import InstalledAppFlow

    client: InstalledAppFlow = GoogleOAuth2.__GetClient()
    client.redirect_uri = from_uri
    client.fetch_token(code=authorization_code)
    return client.credentials.token
