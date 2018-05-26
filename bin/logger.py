#! /usr/bin/env python3

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

import pprint
import datetime
import os

# Log levels: if True, print
LOGINFO = True
LOGDEBUG = True
LOGERROR = True

# Level definitions
INFO = 0
DEBUG = 1
ERROR = 2
MOVE = 3


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

    def __init__(auto=False, logfile=False):
        return

    def getinstance(auto=False, logfile=False):
        if cls not in instances:
            instances[cls] = cls(auto, logfile)
        return instances[cls]
    return getinstance


# ###################################
#  Logger
#
#  Singleton logger class to pretty
#  print all triggered log messages
#  either to a log file that is
#  specified during the initialization.
# ###################################
@singleton
class Logger:
    p = pprint.PrettyPrinter(indent=2, width=120)
    pp = p.pprint

    # ###################################
    #  __init__
    #
    #  If auto is true then all logs get
    #  written to the log file, otherwise
    #  all logs are outputted to the
    #  terminal session.
    #  If a log file is specified, then
    #  either the file is opened for
    #  appending or the file is created
    #  and opened for appending.
    #  Any directory paths that precende
    #  the file are automatically created
    #  if they do not exist.
    # ###################################
    def __init__(self, auto=False, logfile=False):
        self.auto = auto
        if logfile is not False:
            self.logfile = os.path.expanduser(logfile)

            try:
                self.file = open(logfile, 'a+')
            except 'FileNotFoundError':
                directory = os.path.split(logfile)[0]
                if not os.path.exists(directory):
                    os.makedirs(directory)
                self.file = open(logfile, 'a+')
        else:
            self.logfile = None

        self.log(DEBUG, "Initialized Logger")

    # ###################################
    #  write_log
    #
    #  If self.auto is True then any log
    #  triggered is written to the log
    #  file that was specified. If it is
    #  false, then the output is written
    #  to the terminal with a pretty
    #  printer for debugging.
    # ###################################
    def write_log(self, statement):
        dt = datetime.datetime.today()
        if self.auto is True:
            self.file.write("[{}] {}\n".format(dt, statement))
        else:
            self.pp("[{}] {}".format(dt, statement))

    # ###################################
    #  Log
    #
    #  Logs output based on which log
    #  levels are set to True.
    # ###################################
    def log(self, level, logtext):
        if LOGINFO and level == INFO:
            # self.pp("INFO: {}".format(logtext))
            self.write_log("INFO: {}".format(logtext))
            return
        if LOGDEBUG and level == DEBUG:
            # self.pp("DEBUG: {}".format(logtext))
            self.write_log("DEBUG: {}".format(logtext))
            return
        if LOGERROR and level == ERROR:
            # self.pp("ERROR: {}".format(logtext))
            self.write_log("ERROR: {}".format(logtext))
            return
        if level == MOVE:
            # self.pp("MOVE: {}".format(logtext))
            self.write_log("MOVE: {}".format(logtext))
            return

    def error(self, logtext):
        log(ERROR, logtext)

    # ###################################
    #  quit
    #
    #  Writes the final log and closes
    #  the log file if one is open.
    # ###################################
    def quit(self):
        self.write_log("Closing program on user exit")
        if self.auto is True:
            self.file.close()
