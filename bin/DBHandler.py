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

import sqlite3
import json
import time
import os


# ###################################
#  DBHandler
#
#  Interface to the sqlite3 database
#  that acts as the long term storage
#  for the messages.
# ###################################
class DBHandler:
    #logger = Logger()
    #config = Config()

    # ###################################
    #  __init__
    #
    #  Runs the command to create the
    #  database.
    # ###################################
    def __init__(self):
        self.logger = Logger()
        self.config = Config()
        self.createDB()

    # ###################################
    #  Log
    #
    #  Local log method to specify the
    #  name of the class/file of the
    #  caller.
    # ###################################
    def log(self, level, statement):
        self.logger.log(level, "DBHandler -- {}".format(statement))

    # ###################################
    #  createDB
    #
    #  If a local database file with the
    #  name specified in the config file
    #  does not exist, it is created and
    #  initialized with a table to store
    #  all the messages for the chat.
    # ###################################
    def createDB(self):
        if not os.path.isfile(self.config.server["DB"]):
            self.log(DEBUG, "Database {} does not exist, creating....".format(self.config.server["DB"]))
            conn = sqlite3.connect(self.config.server["DB"])
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS messages(ID integer PRIMARY KEY, DATE text, JSON text);")
        else:
            self.log(INFO, "Database {} already exists!!!".format(self.config.server["DB"]))

    # ###################################
    #  addToDB
    #
    #  Adds the message specified in
    #  message_json to the database.
    #  Message is added as follows
    #    ID, DATE, JSON
    #  If database is locked due to a
    #  current write being performed,
    #  then the function waits and tries
    #  again in .1s.
    # ###################################
    def addToDB(self, mType, message_json):
        self.log(DEBUG, "func --> addToDB")
        ID = message_json[mType]["message_id"]
        date = message_json[mType]["date"]
        while True:
            try:
                conn = sqlite3.connect(self.config.server["DB"])
                c = conn.cursor()
                c.execute("INSERT INTO messages(ID, DATE, JSON) SELECT ?, ?, ? WHERE NOT EXISTS(SELECT 1 FROM messages WHERE ID = ?)", (ID, date, json.dumps(message_json), ID))
                conn.commit()  # Save
                conn.close()
                return True
            except Exception as e:
                self.log(ERROR, "Exception Triggered by database lock. Trying again in .1s. Exception: {}".format(e))
                time.sleep(0.1)

    # ###################################
    #  removeFromDB
    #
    #  Removes the message with the
    #  specified ID from the DB.
    # ###################################
    def removeFromDB(self, ID):
        self.log(DEBUG, "func --> removeFromDB")
        conn = sqlite3.connect(self.config.server["DB"])
        c = conn.cursor()
        c.execute("DELETE FROM messages WHERE ID = ?", (ID,))
        conn.commit()
        conn.close()

    # ###################################
    #  loadDB
    #
    #  Grabs all the message from the DB
    #  ordered by the ID, which is
    #  sequential based on the age of the
    #  messages.
    # ###################################
    def loadDB(self):
        self.log(DEBUG, "func --> loadDB")
        conn = sqlite3.connect(self.config.server["DB"])
        c = conn.cursor()
        c.execute("SELECT * FROM messages order by ID")
        messages = c.fetchall()
        # pp(messages)
        messages = sorted(messages, key=lambda message: int(message[1]))
        conn.close()
        return messages
