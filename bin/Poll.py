from logger import *
from TGInterface import TGInterface

import json
import collections
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

class Poll:
    TGI = TGInterface()

    def __init__(self,query, options, end_date):
        self.logger = Logger()
        self.query = query
        self.options = options
        self.end_date = end_date
        self.log(INFO, "INIT")

    def log(self, level, statement):
        self.logger.log(level, "Poll -- {}".format(statement))

    def closePoll(self):
        pass

    def newVote(self):
        pass

    def changeVote(self):
        pass

    def alreadyVoted(self):
        pass

    def setVote(self):
        pass

    def testKeyboard(self):
        self.log(INFO, "func -> testKeyboard")
        keyboard = [[
            InlineKeyboardButton("Option 1", callback_data='1'),
            InlineKeyboardButton("Option 2", callback_data='2'),
            InlineKeyboardButton("Option 3", callback_data='3')
        ]]

        reply_markup = InlineKeyboardMarkup(keyboard)

        reply_markup = json.dumps(reply_markup.to_dict())
        self.bot_say("Options", reply_markup=reply_markup)

    def displayPoll(self):
        self.log(INFO, "func -> displayPoll")
        keyboard = []
        self.log(DEBUG, "Options: {}".format(self.options))
        for key, value in self.options.items():
            keyboard.append([InlineKeyboardButton('{}: {}'.format(key, value),
                                                  callback_data='{}'.format(key))])
        reply_markup = InlineKeyboardMarkup(keyboard)
        reply_markup = json.dumps(reply_markup.to_dict())
        self.TGI.bot_say(self.query, reply_markup=reply_markup)

    def to_json(self):
        pass
