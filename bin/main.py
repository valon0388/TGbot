#!/usr/bin/env python3
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

# Local imports
# Imports Logger class as well as predefined Logging levels(INFO, DEBUG, ERROR)
from logger import *
from config import Config
from BRHandler import botRequestHandler
from MessageQueue import MessageQueue
from InputProcessor import InputProcessor
from botcalendar import BotCalendar
from TGInterface import TGInterface

from http.server import HTTPServer
import ssl
import json
import time
import _thread

config = ''
DB = ''
MQ = ''
CAL = ''
TGI = ''


logger = ''
httpd = ''


# ###################################
#  Log
#
#  Local log method to specify the
#  name of the class/file of the
#  caller.
# ###################################
def log(level, statement):
    logger.log(level, "main -- {}".format(statement))


# ###################################
#  __init__
#
#  Initializes the TGInterface, Calendar
#  MessageQueue, and the botRequestHandler.
#  Starts the botRequestHandler and wraps
#  the socket in an SSL context.
# ###################################
def __init__():
    global config
    global DB
    global MQ
    global CAL
    global TGI
    global logger
    config = Config()
    logger = Logger(auto=True, logname=config.server['LOGNAME'])
    logger.setup(config.server['LOGNAME'])
    log(DEBUG, "func --> __init__")
    TGI = TGInterface()
    CAL = BotCalendar()
    MQ = MessageQueue()
    MQ.loadDB()
    log(INFO, "Attempting to bind to IP: {} and port: {}".format(config.server["IP"], int(config.server["PORT"])))
    server_address = (config.server["IP"], int(config.server["PORT"]))
    global httpd
    httpd = HTTPServer(server_address, botRequestHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket,
                                   server_side=True,
                                   certfile=config.server["CERT"],  # TODO: Add flag to specify filename
                                   keyfile=config.server["KEY"],
                                   ssl_version=ssl.PROTOCOL_TLSv1)


# ###################################
#  push_listener
#
#  Starts the botRequestHandler listener
#  for the message pushes from the Telegram
#  api.
# ###################################
def push_listener(threadName, delay):
    log(INFO, "Starting the push_listener thread: {}".format(threadName))
    httpd.serve_forever()


# ###################################
#  calendar_checker
#
#  Starts the loop that triggers the
#  calendar check once every 24 hours.
# ###################################
def calendar_checker(threadName, delay):
    log(INFO, "Starting the calendar_checker thread: {}".format(threadName))
    while True:
        time.sleep(86400)  # 24 hours
        CAL.check()


# ###################################
#  Starts the main threads for the
#  botRequestHandler and the Calendar.
# ###################################

__init__()
_thread.start_new_thread(push_listener, (("push_listener", 0)))
_thread.start_new_thread(calendar_checker, (("calendar_checker", 0)))

MQ.addBotMessage(config.group_info["STARTUP"])
CAL.build_eventQueue()

log(INFO, "AFTER PUSH LISTENER")

# ###################################
#  Triggers the processing of the message queue
#  and the calendar check for urgent events
#  once every minute.
# ###################################
while True:
    MQ.processQueue()
    CAL.get_urgentEvents()
    time.sleep(60)
