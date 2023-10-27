from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
from jinja2 import Template

from core.env import Env

class Mailer:
  __CLIENT: SMTP = None
  __SENDER: str = None

  @staticmethod
  def Init() -> None:
    host = Env.Get("MAILER_HOST")
    if not host:
      raise Exception("Mailer host not provided")

    port = Env.Get("MAILER_PORT")
    if not port:
      raise Exception("Mailer port not provided")

    Mailer.__SENDER = Env.Get("MAILER_USER")
    if not Mailer.__SENDER:
      raise Exception("Mailer user not provided")

    password = Env.Get("MAILER_PASS")
    if not password:
      raise Exception("Mailer password not provided")

    import ssl
    Mailer.__CLIENT = SMTP(host, int(port))
    Mailer.__CLIENT.starttls(context=ssl.create_default_context())
    Mailer.__CLIENT.login(Mailer.__SENDER, password)

  def send(self, template: str, to: str, subject: str, data: dict = {}) -> None:
    if not Mailer.__CLIENT:
      raise Exception("SMTP Client not initialized, check USE_MAILER env")

    message = MIMEMultipart()
    message["Subject"] = subject
    message.attach(MIMEText(self.__load(template, data), "html"))
    Mailer.__CLIENT.sendmail(Mailer.__SENDER, to, message.as_string())

  def __load(self, template: str, data: dict) -> str:
    template: Template
    with open(f"public/emails/{template}.html") as html:
      template = Template(html.read())

    return template.render(data)
