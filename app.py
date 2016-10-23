import __builtin__
import logging
import os
from logging.config import fileConfig

import yaml
from flask import Flask
from flask_restful import Api
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer
from lcs import LCS

# fileConfig('config/logging_config.ini')
# logger = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app)

api.add_resource(LCS, '/api/get_lcs_tables')

if __name__ == '__main__':
    # logger.info("server starting with port 10260:")
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(port=10260)
    IOLoop.instance().start()
