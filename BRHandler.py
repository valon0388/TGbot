# v1.01

# This file is part of TGBOT.

# TGBOT is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# TGBOT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with TGBOT.  If not, see <http://www.gnu.org/licenses/>.


# TGBOT v3.0

# Local imports
# Imports Logger class as well as predefined Logging levels(INFO, DEBUG, ERROR)
from logger import *
from config import Config
from MessageQueue import MessageQueue
from InputProcessor import InputProcessor
from botcalendar import BotCalendar
from TGInterface import TGInterface

from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
import ssl
import json
import time
import _thread


# ##############################################################################
# class botRequestHandler
#
# Extends BaseHTTPRequestHandler to enable processing of incoming messages from
# the Telegram servers via POST requests.
# ##############################################################################
class botRequestHandler(BaseHTTPRequestHandler):
    logger = Logger()
    processor = InputProcessor()
    config = Config()
    TGI = TGInterface()
    CAL = BotCalendar()
    MQ = MessageQueue()

    # ##################################
    #  Log
    #
    #  Local log method to specify the
    #  name of the class/file of the
    #  caller.
    # ###################################
    def log(self, level, statement):
        self.logger.log(level, "botRequestHandler -- {}".format(statement))

    # ################################################
    #  process_post_data
    #
    #  Takes the post_data for an incoming
    #  message and sends it to the processor
    #  to check if it needs to be processed now.
    #  If process_now returns 'eventlist' a
    #  calendar check is triggered. Otherwise
    #  the return response or message from Telegram is
    #  added to the queue to be processed_later.
    # ################################################
    def process_post_data(self, post_data):
        self.log(DEBUG, post_data)
        post_data = json.loads(post_data.decode('utf-8'))
        response = self.processor.process_now(post_data)
        if response is 'eventlist':
            response = self.CAL.check()
        if response is not None:
            self.log(DEBUG, "RESPONSE: {}".format(response))
            if self.processor.process_later(response):
                self.MQ.addMessage(response)
        if self.processor.process_later(post_data):
            self.MQ.addMessage(post_data)

    # ###################################
    #  set_success_headers
    #
    #  Sets the headers indicating a correct
    #  query of the server.
    # ###################################
    def set_success_headers(self):
        self.log(DEBUG, "botRequestHandler --> set_success_headers")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    # ###################################
    #  set_forbidden_headers
    #
    #  Sets the headers indicating that
    #  the sent query is forbidden.
    # ###################################
    def set_forbidden_headers(self):
        self.log(DEBUG, "botRequestHandler --> set_forbidden_headers")
        self.send_response(403)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    # ###################################
    #  do_GET
    #
    #  Get is forbidden, so 403 forbidden
    #  is sent.
    # ###################################
    def do_GET(self):
        self.log(DEBUG, "botRequestHandler --> do_GET")
        self.set_forbidden_headers()
        self.send_response(403)

    # ###################################
    #  do_POST
    #
    #  Recieves messages from the Telegram
    #  servers and indicates a successful
    #  response when the requested path
    #  is /{TOKEN} as configured in the
    #  TGBOT config file.
    # ###################################
    def do_POST(self):
        self.log(DEBUG, "botRequestHandler --> do_POST")
        try:
            content_length = int(self.headers['Content-Length'])  # gets size
            self.log(DEBUG,
                     "PATH: {} \n TOKEN:{}".format(
                        self.path[1:],
                        self.config.telegram["TOKEN"]
                        ))
            if self.path[1:] == self.config.telegram["TOKEN"]:
                post_data = self.rfile.read(content_length)  # gets data
                _thread.start_new_thread(self.process_post_data, (post_data,))
                self.set_success_headers()
                self.wfile.write(b"<html><body><h1>POST!</h1></body></html>\n")
            else:
                self.set_forbidden_headers()
                self.wfile.write(
                    b"<html><body><h1>403 FORBIDDEN</h1></body></html>"
                    )
        except Exception as e:
            self.log(ERROR, "Exception: {}".format(e))
