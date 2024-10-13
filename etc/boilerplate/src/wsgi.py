#! /usr/bin/env python3

import logging
from waitress import serve

from __core.env import Env
from __core.server import Server

if __name__ == "__main__":
  server = Server()
  logger = logging.getLogger("waitress")
  logger.setLevel(Env.Get("LOG_LEVEL"))
  serve(server.expose(), host=server.host(), port=server.port())
