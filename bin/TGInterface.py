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
from logger import *  # Imports Logger class as well as predefined Logging levels(INFO, DEBUG, ERROR)
from config import Config

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

import json
import urllib
import requests
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
#  TGInterface
#
#  Telegram interface. Takes care of
#  interfacing with the Telegram API
#  including deleting and sending
#  messages.
# ###################################
@singleton
class TGInterface:
    logger = Logger()
    config = Config()
    #updater = Updater(self.config.telegram["TOKEN"], use_context=True)

    def testKeyboard(self):
        keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
                 InlineKeyboardButton("Option 2", callback_data='2')],
                [InlineKeyboardButton("Option 3", callback_data='3')]]

        reply_markup = InlineKeyboardMarkup(keyboard)

        #update.message.reply_text('Please choose:', reply_markup=reply_markup)
        #self.bot_say(reply_markup)
        #self.bot_say(json.dumps(reply_markup))
        #self.bot_say("Options", reply_markup=reply_markup)
        self.bot_say("Options", reply_markup=json.dumps(reply_markup))

    def button(self, update, context):
        query = update.callback_query
        query.edit_message_text(text="Selected option: {}".format(query.data))


    def help(self, update, context):
        update.message.reply_text("Use /start to test this bot.")

    def error(self, update, context):
        self.log(ERROR, "[{}] {}".format(context.error, update))

    # ###################################
    #  Log
    #
    #  Local log method to specify the
    #  name of the class/file of the
    #  caller.
    # ###################################
    def log(self, level, statement):
        self.logger.log(level, "TGInterface -- {}".format(statement))

    # ###################################
    #  welcome_say
    #
    #  Takes the name of the member that
    #  just joined the chat and triggers
    #  a bot_say event that includes the
    #  welcome message to the new member
    #  containing the group_name,
    #  member_name, and rules_link.
    # ###################################
    def welcome_say(self, member_name):
        self.log(INFO, "func --> send_welcome")
        welcome = self.config.WELCOME
        group_name = self.config.group_info["GROUPNAME"]
        rules_link = self.config.group_info["RULES"]
        response = self.bot_say(welcome.format(group_name, member_name, rules_link))
        return response

    # ###################################
    #  bot_say
    #
    #  Triggers a request to the chat to
    #  have the bot post a message
    #  containing the string contained in
    #  the text parameter.
    # ###################################
    def bot_say(self, text, reply_markup=None):
        self.log(DEBUG, "func --> bot_say")
        live = eval(self.config.server["LIVE"])
        say = eval(self.config.telegram["BOTSAY"])
        text = urllib.parse.quote(text)
        url = self.config.telegram["URL"].format(self.config.telegram["TOKEN"]) + "sendMessage?text={}&chat_id={}".format(text, self.config.telegram["CHAT_RESTRICTION"])
        if reply_markup != None:
            url = url + "&inline_keyboard={}".format(reply_markup)
        if live and say:
            self.log(DEBUG, "URL: {}".format(url))
            response = json.loads(self.get_url(url))
            self.log(DEBUG, "Response from server: {}".format(response))
            return {"message": response["result"]}
        else:
            self.log(DEBUG, '')
            self.log(DEBUG, "Would have sent Message:  {}".format(url))
            self.log(DEBUG, '')
            return None

    # ###################################
    #  get_url
    #
    #  Triggers a GET request to whatever
    #  url is passed to the function.
    # ###################################
    def get_url(self, url):
        self.log(DEBUG, "func --> get_config")
        self.log(DEBUG, "get_url: {}".format(url))
        response = requests.get(url)
        content = response.content.decode("utf8")
        return content

    # ###################################
    #  deleteFromChat
    #
    #  Triggers a request to the Telegram
    #  API to delete the message with
    #  message_id from the chat.
    #  On a failed delete, it waits 5
    #  seconds and then recurses to attempt
    #  another delete.
    # ###################################
    def deleteFromChat(self, message_id, chat_id, recurse=0):
        self.log(DEBUG, "func --> deleteFromChat")
        if recurse >= 5:
            self.log(ERROR, "Failed to delete message {} from chat!! Message_json to follow".format(message_id))
            self.log(ERROR, message_id)
            return False

        self.log(INFO, "Attempting to delete message: {} from chat: {}".format(message_id, chat_id))
        url = self.config.telegram["URL"].format(self.config.telegram["TOKEN"]) + "deleteMessage?message_id={}&chat_id={}".format(message_id, chat_id)
        if self.config.server["LIVE"]:
            result = self.get_url(url)
            self.log(DEBUG, "Return from Delete: {}".format(result))
            result = json.loads(result)
            if "ok" in result and result["ok"]:
                self.log(INFO, "Message deleted.")
                return True
            else:
                self.log(ERROR, "Message not deleted...trying again in 5 seconds")
                #time.sleep(5)
                return self.deleteFromChat(message_id, chat_id, recurse + 1)
        else:
            self.log(DEBUG, "TESTING DELETE")
