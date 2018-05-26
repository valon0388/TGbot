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

# Local Imports
# Imports Logger class as well as predefined Logging levels(INFO, DEBUG, ERROR)
from logger import *
from DBHandler import DBHandler
from config import Config
from TGInterface import TGInterface


from queue import Queue
import json
import time


# ###################################
#  singleton
#
#  Used to define a function to create
#  a singleton object. @singleton above
#  class definition will either create
#  an instance of the class and add it
#  to the instances array or return the
#  already created instance of the
#  class.
# ###################################
def singleton(cls):
    instances = {}

    def __init__():
        return

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


# ###################################
#  MessageQueue
#
#  Grouping class that tracks a running
#  Message queue (loaded from the DB on
#  initialization) and a database
#  full of all the undeleted messages
#  in the chat.
# ###################################
@singleton
class MessageQueue:
    logger = Logger()
    DB = DBHandler()
    config = Config()
    TGI = TGInterface()
    messageQueue = Queue()

    # ###################################
    #  Log
    #
    #  Local log method to specify the
    #  name of the class/file of the
    #  caller.
    # ###################################
    def log(self, level, statement):
        self.logger.log(level, "MessageQueue -- {}".format(statement))

    # ###################################
    #  processQueue
    #
    #  Checks the first message in the
    #  queue to see if it has been in
    #  chat longer than the time specified
    #  in the config file. If it is over
    #  the threshold a delete action is
    #  triggered.
    # ###################################
    def processQueue(self):
        self.log(DEBUG, "func --> processQueue")
        time_limit = self.config.telegram["TIME_LIMIT"]
        first_message = self.message_peek()
        if first_message is not False:
            self.log(DEBUG, "First_Message: {}".format(first_message))
            message = json.loads(str(first_message))
            self.log(DEBUG, message)
            message_delta = time.time() - message[self.getMType(message)]["date"]
            if message is not False and message_delta >= int(time_limit):
                self.removeMessage(message)
                self.processQueue()

    # ###################################
    #  getMType
    #
    #  Determines the type of message that
    #  has been sent to the bot and sets
    #  a variable declaring said type.
    # ###################################
    def getMType(self, message_json):
        self.log(DEBUG, "func --> getMType")
        if "message" in message_json:
            mType = "message"
        elif "edited_message" in message_json:
            mType = "edited_message"
        elif "inline_query" in message_json:  # Not fully supported at this moment.
            mType = "inline_query"
        else:
            mType = "other"
        return mType

    # ###################################
    #  addBotMessage
    #
    #  Sends the message to chat and 
    #  adds the return message specified
    #  to the DB and to the queue.
    # ###################################
    def addBotMessage(self, message):
        self.log(DEBUG, "func --> addMessage")
        return_json = self.TGI.bot_say(message)
        self.addToQueue(return_json)
        self.DB.addToDB(self.getMType(return_json), return_json)

    # ###################################
    #  addToQueue
    #
    #  Adds a message to the queue.
    # ###################################
    def addToQueue(self, message_json):
        self.log(DEBUG, "func --> addToQueue")
        self.messageQueue.put(json.dumps(message_json))

    # ###################################
    #  removeMessage
    #
    #  Removes a message fromt the chat
    #  via the Telegram interface and
    #  then removes the message from the
    #  DB.
    # ###################################
    def removeMessage(self, message_json):
        self.log(DEBUG, "func --> removeMessage")
        mType = self.getMType(message_json)

        message_id = message_json[mType]["message_id"]
        chat_id = message_json[mType]["chat"]["id"]

        self.TGI.deleteFromChat(message_id, chat_id)
        self.messageQueue.get()
        self.DB.removeFromDB(message_id)

    # ###################################
    #  message_peek
    #
    #  If the queue size is not zero it
    #  returns the first element in the
    #  array which should be the oldest
    #  message in the chat.
    # ###################################
    def message_peek(self):
        self.log(DEBUG, "func --> message_peek")
        if self.messageQueue.qsize() > 0:
            return self.messageQueue.queue[0]
        else:
            return False

    # ###################################
    #  loadDB
    #
    #  Used when the class is initialized
    #  loads the messages in the DB into
    #  the queue with the oldest being
    #  the first in the queue and the
    #  newest being the last element.
    # ###################################
    def loadDB(self):
        messages = self.DB.loadDB()
        for i in messages:
            self.messageQueue.put(i[2])
        if len(messages) > 0:
            self.log(DEBUG, "First Message In Message Queue: {}".format(self.message_peek()))
