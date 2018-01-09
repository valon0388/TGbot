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

# local imports
# Imports Logger class as well as predefined Logging levels(INFO, DEBUG, ERROR)
from logger import *
from TGInterface import TGInterface
from config import Config

# import httplib2
# import os
import queue
import json
from datetime import datetime, timedelta, timezone
import dateutil.parser
import pycurl
from io import BytesIO

# URL=https://www.googleapis.com/calendar/v3/calendars/{cal_id}/events?key={api_key}


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
#  BotCalendar
#
#  Uses the Google API to read events
#  from an calendar specified by a
#  calendar ID using the pycurl
#  module and an api key.
# ###################################
@singleton
class BotCalendar:
    logger = Logger()
    config = Config()
    eventQueue = queue.Queue()
    TGI = TGInterface()

    URL = 'https://www.googleapis.com/calendar/v3/calendars/{}/events?key={}&timeMin={}&maxResults=3&showDeleted=false&orderBy=startTime&singleEvents=true'

    # ###################################
    #  __init__
    #
    #  Grabs the api key and calendar id
    #  to initialize the class.
    # ###################################s
    def __init__(self):
        self.log(DEBUG, " func --> __init__")
        self.API_KEY = self.config.calendar['API_KEY']
        self.CALID = self.config.calendar['CALID']

    # ###################################
    #  Log
    #
    #  Local log method to specify the
    #  name of the class/file of the
    #  caller.
    # ###################################
    def log(self, level, statement):
        self.logger.log(level, "calendar -- {}".format(statement))

    # ###################################
    #  build_eventQueue
    #
    #  Grabs the events and then loads
    #  them into a queue for use later.
    # ###################################
    def build_eventQueue(self):
        events = self.get_events()
        for event in events:
            self.add_to_eventQueue(event)
        return events

    # ###################################
    #  add_to_eventQueue
    #
    #  Takes a passed in event and checks
    #  the queue for its event id. If the
    #  id exists, the index of that event
    #  is overwritten (in case the event
    #  has been updated), in the event
    #  that the id is not found, the event
    #  is added to the back of the queue.
    # ###################################
    def add_to_eventQueue(self, event):
        self.log(DEBUG, " func --> add_to_eventQueue")
        eventID = event['id']
        i = 0
        found = False
        while i < self.eventQueue.qsize():
            if eventID is self.eventQueue.queue[i]['id']:
                found = True
                self.eventQueue.queue[i]['id'] = event
                break
            i = i + 1
        if not found:
            self.eventQueue.put(event)

    # ###################################
    #  check
    #
    #  If the event_list is not empty and
    #  config setting for listing events
    #  is enabled, then trigger a bot_say
    #  event to post the event_string to
    #  chat.
    # ###################################
    def check(self):
        self.log(DEBUG, " func --> check")
        event_list = self.get_eventlist()
        if event_list is not '' and eval(self.config.events["LIST"]):
            response = self.TGI.bot_say(self.get_eventlist())
            return response
        else:
            self.log(DEBUG, "EVENT STRING: {}".format(event_list))
            return None

    # ###################################
    #  get_events
    #
    #  Calls the event_list function and
    #  then grabs the items object, which
    #  contains the next 10 events in the
    #  calendar.
    # ###################################
    def get_events(self):
        self.log(DEBUG, " func --> get_events")
        eventsResult = self.event_list()
        events = eventsResult.get('items', [])
        return events

    # ###################################
    #  event_list
    #
    #  Grabs the events from the calendar
    #  url and converts the returned
    #  string into a json object.
    # ###################################
    def event_list(self):
        self.log(DEBUG, "func --> get_eventlist")
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        URL = self.URL.format(self.CALID, self.API_KEY, now)
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, URL)
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()
        body = buffer.getvalue().decode('iso-8859-1')
        response_json = json.loads(body)
        self.log(DEBUG, "Response_json: {}".format(response_json))
        return response_json

    # ###################################
    #  get_eventlist
    #
    #  Builds the eventqueue and then, if
    #  the queue is not empty, generates
    #  and event_string that contains the
    #  next three upcoming events and a
    #  link to a website page containing
    #  all the upcoming events.
    # ###################################
    # Check the next 3 events
    def get_eventlist(self):
        self.log(DEBUG, " func --> get_eventlist")
        events = self.build_eventQueue()
        if not events:
            self.log(INFO, 'No upcoming events found.')
            return 'No Events Found :('
        event_string = 'Upcoming event list:\n'
        i = 0
        for event in events:
            self.log(DEBUG, "EVENT: {}".format(event))
            start = dateutil.parser.parse(event['start'].get('dateTime', event['start'].get('date')))
            event_string = event_string + "\nTime: {}, Event: {}".format(start.strftime("%a %D @ %I:%M%p"), event['summary'])
            i = i + 1
            if i >= 3:
                break
        if "UPCOMING" in self.config.group_info:
            event_string = event_string + '\n\nUpcoming Events: {}'.format(self.config.group_info["UPCOMING"])
        return event_string

    # ###################################
    #  get_urgentEvents
    #
    #  If there are events in the queue,
    #  compares the current date, down to
    #  minute, of the first event in the
    #  queue to the current date, down
    #  to the minute, to see if the event
    #  is ocurring now, or in 1, 3, 6, 12,
    #  48, or 72 hours and then prints a
    #  string stating that along with the
    #  description of the event, to the
    #  chat.
    # ###################################
    def get_urgentEvents(self):
        self.log(DEBUG, " func --> get_urgentEvents")
        if self.eventQueue.qsize() > 0:
            event = self.eventQueue.queue[0]
            now = datetime.today()
            currentMinute = now.replace(second=0, microsecond=0, tzinfo=timezone(timedelta(hours=-6)))
            self.log(DEBUG, "EVENT: {}".format(event))
            start = dateutil.parser.parse(event['start'].get('dateTime', event['start'].get('date')))
            startMinute = start.replace(second=0, microsecond=0)
            event_string = ''
            if startMinute < currentMinute:
                oldEV = self.eventQueue.get()
                self.log(DEBUG, "REVOVING OLD EVENT FROM EVENT QUEUE: {}".format(oldEV))
                self.get_urgentEvents()
            else:
                for time in 0, 1, 3, 6, 12, 24, 48, 72:
                    self.log(DEBUG, "startMinute: {}".format(startMinute))
                    self.log(DEBUG, "currentMinute: {}".format(currentMinute))
                    self.log(DEBUG, "timedelta: {}".format(timedelta(hours=time)))
                    self.log(DEBUG, "+: {}".format(currentMinute + timedelta(hours=time)))
                    if startMinute == currentMinute + timedelta(hours=time):
                        if time is 0:
                            event_string = "Event: {} Starts now!!!\n\n{}".format(event['summary'])
                            self.eventQueue.get()
                        else:
                            if time is 1:
                                hour = 'hour'
                            else:
                                hour = 'hours'
                            event_string = "Event: {} Starts in {} {} at {}!!!".format(event['summary'], time, hour, start.strftime("%a %D @ %I:%M%p"))
                        if 'description' in event:
                            event_string = event_string + "\nDescription: {}".format(event['description'])
                        break
                if event_string is not '' and eval(self.config.events["REMINDERS"]):
                    self.TGI.bot_say(event_string)
