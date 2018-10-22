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
from TGInterface import TGInterface
from config import Config
from botcalendar import BotCalendar
from MessageQueue import MessageQueue
from Poller import Poller

import json
import re
import random
from datetime import datetime, timedelta, timezone


# ###################################
#  InputProcessor
#
#  Processes the incoming text from
#  Telegram and other clients to
#  determine if cation needs to be
#  taken by the bot.
# ###################################
class InputProcessor:
        
    def __init__(self):    
        self.logger = Logger()
        self.TGI = TGInterface()
        self.config = Config()
        self.Poller = Poller()
        self.CAL = BotCalendar()
        self.MQ = MessageQueue()
        self.ZONE = -5

    # ###################################
    #  Log
    #
    #  Local log method to specify the
    #  name of the class/file of the
    #  caller.
    # ###################################
    def log(self, level, statement):
        self.logger.log(level, "InputProcessor -- {}".format(statement))

    # ###################################
    #  new_member_check
    #
    #  Checks to see if a new member has
    #  joined the chat. If so, triggers a
    #  welcome message to be sent based on
    #  the one defined in the config file.
    # ###################################
    def new_member_check(self, message_json):
        self.log(DEBUG, "func --> new_member_check")
        mType = self.getMType(message_json)
        if 'new_chat_member' in message_json[mType]:
            self.TGI.welcome_say(message_json[mType]["new_chat_member"]["first_name"])

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

    # ################################################
    #  process_post_data
    #
    #  Takes the post_data for an incoming
    #  message and sends it to process_now
    #  to check if it needs to be processed now.
    #  The return response or message from Telegram is
    #  added to the queue to be processed_later. Following
    #  that the original message is run through the later
    #  processor to be logged.
    # ################################################
    def process_post_data(self, post_data):
        self.log(DEBUG, post_data)
        post_data = json.loads(post_data.decode('utf-8'))
        response = self.process_now(post_data)

        if response is not None:
            self.log(DEBUG, "RESPONSE: {}".format(response))
            if self.process_later(response):
                self.MQ.addMessage(response)
        if self.process_later(post_data):
            self.MQ.addMessage(post_data)

    # ###################################
    #  process_later
    #
    #  Determines if a message will need
    #  processing later. In the current
    #  case, if a message will need to be
    #  deleted at a later date.
    # ###################################
    def process_later(self, post_data):
        self.log(DEBUG, "func --> process_later")
        # TODO: What if I don't want a message to be processed?
        if "edited_message" in post_data or "message" in post_data:
            return True
        else:
            return False

    def event_request_check(self, text):
        self.log(DEBUG, "func -> event_request_check")
        if re.compile(self.config.telegram["BOTNAME"]).match(text) is not None and re.compile(self.config.RESPONSES['events'][0]).search(text) is not None:
            self.log(DEBUG, "EVENTLIST AND BOTNAME MATCH: {}".format(text))
            self.CAL.check()
            return True
        return False

    def poll_request_check(self, text):
        self.log(DEBUG, "func -> poll_request_check")
        if re.compile(self.config.telegram["BOTNAME"]).match(text) is not None and re.compile(self.config.RESPONSES['newpoll'][0]).search(text) is not None:
            self.log(DEBUG, "NEWPOLL AND BOTNAME MATCH: {}".format(text))
            self.Poller.newPoll(text)
            self.log(DEBUG, "Poller created with {}".format(text))
            return True
        return False


    def get_timeout(self, key):
        self.log(DEBUG, "func -> get_timeout")
        if not key in self.config.TIMEOUT:
            timeout = 0
        else:
            timeout = self.config.TIMEOUT[key]
        return timeout

    def check_timeout(self, timeout):
        self.log(DEBUG, "func -> check_timeout")
        now = datetime.today().replace(microsecond=0,tzinfo=timezone(timedelta(hours=self    .ZONE)))

        if timeout is 0 or timeout <= now:
            self.log(DEBUG, "TIMEOUT NOT IN EFFECT!!!")
            return True
        self.log(DEBUG, "TIMEOUT STILL IN EFFECT...")
        return False

    def set_timeout(self, timeout, key):
        self.log(DEBUG, "func -> set_timeout")
        now = datetime.today().replace(microsecond=0,tzinfo=timezone(timedelta(hours=self.ZONE)))
        new_timeout = now + timedelta(seconds=+int(self.config.telegram["BOTLIMIT"]))
        self.config.TIMEOUT[key] = new_timeout
        self.log(DEBUG, "Set Done: {}".format(self.config.TIMEOUT[key]))

    def process_triggers(self, text):
        self.log(DEBUG, "func --> process_triggers")
        

        if not self.event_request_check(text) and not self.poll_request_check(text):
            for key, value in self.config.triggers["TRIGGERS"].items():
                timeout = self.get_timeout(key)
                try:
                    value = value.format(self.config.telegram["BOTNAME"])
                    self.log(DEBUG, "FILLED IN THE BOTNAME. TRigger is now [{}]".format(value))
                except IndexError:
                    self.log(DEBUG, "No need to fill in the botname. This trigger [{}] doesn't take a name.".format(value)) 
        

                if self.check_timeout(timeout):
                    re_value = re.compile(value)
                    if re_value.search(text) is not None:
                        self.log(DEBUG, "SETTING THE TIMEOUT")
                        self.set_timeout(timeout, key)
                        self.TGI.bot_say(random.choice(self.config.RESPONSES[key]))
                        #self.TGI.testKeyboard()
                        break;
                    else:
                        self.log(DEBUG, "No Match for [{}] in text [{}]".format(value, text))


    # ###################################
    #  process_now
    #
    #  Determines if a message needs to be
    #  processed now. In this case, if
    #  someone has joined chat, a botsay
    #  event has been sent, or an eventlist
    #  has been requested.
    # ###################################
    def process_now(self, message):
        self.log(DEBUG, "func --> process_now")

        mType = self.getMType(message)
        response = None
        self.log(DEBUG, "Message: {}".format(message))
        if mType is not 'other' and 'text' in message[mType]:
            text = message[mType]['text']
        if "botsay" in message:
            #response = self.TGI.bot_say(message["botsay"])
            response = self.MQ.addBotMessage(message["botsay"])
        elif 'new_chat_member' in message[mType] and message[mType]["new_chat_member"]['is_bot'] is False:
            response = self.TGI.welcome_say(message[mType]['new_chat_member']["first_name"])
        elif 'text' in message[mType]:
            self.process_triggers(text)


        self.log(DEBUG, "response: {}".format(response))
        return response
