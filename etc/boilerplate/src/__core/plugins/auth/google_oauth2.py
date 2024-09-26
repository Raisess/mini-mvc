# @NOTE: To use this implementation you need to add the `google-auth-oauthlib` package to
# `requirements.txt`
# @REFERENCE: https://github.com/googleapis/google-auth-library-python-oauthlib

from google.auth.credentials import Credentials
from google_auth_oauthlib.flow import Flow, InstalledAppFlow

from __core.env import Env
from __core.exceptions import InvalidEnvironmentException, NotConnectedException

class GoogleOAuth2:
  __FLOW: InstalledAppFlow = None

  @staticmethod
  def Init():
    if GoogleOAuth2.__FLOW:
      return

    client_id = Env.Get("GOOGLE_OAUTH2_CLIENT_ID")
    if not client_id:
      raise InvalidEnvironmentException("GOOGLE_OAUTH2_CLIENT_ID")

    client_secret = Env.Get("GOOGLE_OAUTH2_CLIENT_SECRET")
    if not client_id:
      raise InvalidEnvironmentException("GOOGLE_OAUTH2_CLIENT_SECRET")

    redirect_uri = Env.Get("GOOGLE_OAUTH2_REDIRECT_URI")
    if not client_id:
      raise InvalidEnvironmentException("GOOGLE_OAUTH2_REDIRECT_URI")

    scopes = Env.Get("GOOGLE_OAUTH2_SCOPES")
    if not scopes:
      raise InvalidEnvironmentException("GOOGLE_OAUTH2_SCOPES")

    GoogleOAuth2.__FLOW = InstalledAppFlow.from_client_config(
      client_config={
        "web": {
          "client_id": client_id,
          "client_secret": client_secret,
          "auth_uri": "https://accounts.google.com/o/oauth2/auth",
          "token_uri": "https://accounts.google.com/o/oauth2/token"
        },
      },
      scopes=scopes
    )
    GoogleOAuth2.__FLOW.redirect_uri = redirect_uri

  def get_authorization_url(self) -> str:
    if not GoogleOAuth2.__FLOW:
      raise NotConnectedException("GoogleOAuth2", "USE_GOOGLE_OAUTH2")

    authorization_url = GoogleOAuth2.__FLOW.authorization_url(
      access_type="offline",
      prompt="select_account"
    )
    return authorization_url

  def get_authorized_credentials(self, authorization_code: str) -> Credentials:
    if not GoogleOAuth2.__FLOW:
      raise NotConnectedException("GoogleOAuth2", "USE_GOOGLE_OAUTH2")

    GoogleOAuth2.__FLOW.fetch_token(code=authorization_code)
    return GoogleOAuth2.__FLOW.credentials
