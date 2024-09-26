from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
from jinja2 import Template

from __core.env import Env, InvalidEnvironmentException
from __core.exceptions import InvalidEnvironmentException

class Mailer:
  __CLIENT: SMTP = None
  __SENDER: str = None

  @staticmethod
  def Init() -> None:
    host = Env.Get("MAILER_HOST")
    if not host:
      raise InvalidEnvironmentException("MAILER_HOST")

    port = Env.Get("MAILER_PORT")
    if not port:
      raise InvalidEnvironmentException("MAILER_PORT")

    Mailer.__SENDER = Env.Get("MAILER_USER")
    if not Mailer.__SENDER:
      raise InvalidEnvironmentException("MAILER_USER")

    password = Env.Get("MAILER_PASS")
    if not password:
      raise InvalidEnvironmentException("MAILER_PASS")

    import ssl
    Mailer.__CLIENT = SMTP(host, int(port))
    Mailer.__CLIENT.starttls(context=ssl.create_default_context())
    Mailer.__CLIENT.login(Mailer.__SENDER, password)

  def send(self, template: str, to: str, subject: str, data: dict = {}) -> None:
    if not Mailer.__CLIENT:
      raise NotConnectedException("Mailer (SMTP Client)", "USE_MAILER")

    message = MIMEMultipart()
    message["Subject"] = subject
    message.attach(MIMEText(self.__load(template, data), "html"))
    Mailer.__CLIENT.sendmail(Mailer.__SENDER, to, message.as_string())

  def __load(self, template: str, data: dict) -> str:
    template: Template
    with open(f"public/emails/{template}.html") as html:
      template = Template(html.read())

    return template.render(data)
