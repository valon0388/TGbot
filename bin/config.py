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


import configparser as cp
from os.path import isfile
from os.path import realpath
import re


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
#  Config
#
#  Used to get the config from the config
#  file bot.conf, in the local directory.the
#  if the file doesn't exist, it is created
#  with a default set of values.
# ###################################
@singleton
class Config:
    #logger = Logger()
    config = cp.ConfigParser()
    server = {}
    telegram = {}
    group_info = {}
    calendar = {}
    events = {}
    triggers = {}
    responses = {}

    # ###################################
    #  __init__
    # ###################################
    def __init__(self, config_file='./bot.conf'):
        self.config_file = realpath(config_file)
        self.get_config()

    # ###################################
    #  Log
    #
    #  Local log method to specify the
    #  name of the class/file of the
    #  caller.
    # ###################################
    def log(self, level, statement):
        #self.logger = Logger()
        print(level, "config -- {}".format(statement))

    # ###################################
    #  GET_CONFIG
    #
    #  Grabs the configuration information from bot.conf
    #  If bot.conf doesn't exist, uses save_config() to
    #  generate and save a default config and use that.
    # ###################################
    def get_config(self):
        print(self.config_file)
        if isfile(self.config_file):
            self.config.read(self.config_file)

            #
            section = 'server'
            self.server["LIVE"] = self.config[section]['live']
            self.server["IP"] = self.config[section]['ip']
            self.server["PORT"] = self.config[section]['port']
            self.server["KEY"] = self.config[section]['key']
            self.server["CERT"] = self.config[section]['cert']
            self.server["DB"] = self.config[section]['db']
            self.server["LOGNAME"] = self.config[section]['logname']

            section = 'telegram'
            self.telegram["BOTSAY"] = self.config[section]['botsay']
            self.telegram["BOTLIMIT"] = self.config[section]['botlimit']
            self.telegram["BOTWELCOME"] = self.config[section]['botwelcome']
            self.telegram["CHAT_RESTRICTION"] = self.config[section]['chat_id']
            self.telegram["TOKEN"] = self.config[section]['token']
            self.telegram["TIME_LIMIT"] = self.config[section]['time_limit']
            self.telegram["URL"] = self.config[section]['url']
            self.telegram["BOTNAME"] = self.config[section]['botname']

            section = 'group_info'
            self.group_info["GROUPNAME"] = self.config[section]['name']  
            self.group_info["STARTUP"] = self.config[section]['startup']
            self.group_info["RULES"] = self.config[section]['rules_link']
            self.group_info["UPCOMING"] = self.config[section]['upcoming']


            section = 'calendar'
            self.calendar["APP_NAME"] = self.config[section]['app_name']
            self.calendar["CALID"] = self.config[section]['cal_id']
            self.calendar["API_KEY"] = self.config[section]['api_key']

            section = 'events'
            self.events["LIST"] = self.config[section]['list']
            self.events["REMINDERS"] = self.config[section]['reminders']

            self.TIMEOUT = {"def_val": 101}

            section = 'triggers'
            regex = re.compile('^trigger_')
            self.triggers["ON"] = self.config[section]['on']
            self.triggers["TRIGGERS"] = {}
            for key, value in self.config[section].items():
                if regex.match(key) is not None:
                    self.triggers["TRIGGERS"][re.sub(regex, "", key)] = value

            self.log(DEBUG, self.triggers)
            section = 'responses'
            self.WELCOME = self.config[section]['welcome']
            self.RESPONSES = {}
            for key, value in self.config[section].items():
                if key != 'welcome':
                    res_head = re.compile('_.*').sub('', key)
                    if res_head in self.RESPONSES:
                        self.RESPONSES[res_head].append(value)
                    else:
                        self.RESPONSES[res_head] = [value]
        else:
            self.save_config(True)

    # ###################################
    # SAVE_CONFIG
    #
    # Saves the config that is currently being used to the file
    # bot.conf. If there is no config, saves a default file.
    # ###################################
    def save_config(self, default=False):
        self.log(DEBUG, "func --> save_config")
        if default:
            self.config['server'] = {
                'ip': '1.2.3.4',
                'port': 443,
                'key': 'YOUR_Private.key',
                'cert': 'YOUR_Public.pem',
                'live': True,
                'db': 'messageQueue.db'
            }

            self.config['telegram'] = {
                'chat_id': -100000000,
                'token': '987654321:ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                'time_limit': '82800',
                'botsay': True,
                'botwelcome': True,
                'url': 'https://api.telegram.org/bot{}/'
            }

            self.config['group_info'] = {
                'name': 'BOT_CHAT',
                'rules_link': 'https://mygroup.com/group/link/to/rules',
                'upcoming': 'https://mygroup.com/group/link/to/upcoming/events/post'
            }

            self.config['calendar'] = {
                'cal_id': 'A0B1C2D3E4F5G6H7I8J9K0@group.calendar.google.com',
                'api_key': 'Z00Y11X22W33V44U55T66S77R88Q99'
            }

            self.config['events'] = {
                'list': True,
                'reminders': True
            }

            self.config['triggers'] = {
                'on': True,
                'trigger_hey': 'Hey {}',
                'trigger_poke': ".*['pP']oke.* {}"
            }

            self.config['responses'] = {
                'hey_one': 'You rang?',
                'poke_one': 'What was that?',
                'welcome': 'Welcome to the {} chat, {}! \n\n Take a moment and read our rules before getting started. You can find them at {}.'
            }

        with open(self.config_file, 'w') as config_link:
            self.config.write(config_link)
