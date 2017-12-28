#!/usr/bin/env python3

from botcalendar import BotCalendar
from config import Config

config = Config()
CAL = BotCalendar(config.calendar["API_KEY"], config.calendar["CALID"])

CAL.check()

print('')
print('')

CAL.get_urgentEvents()
