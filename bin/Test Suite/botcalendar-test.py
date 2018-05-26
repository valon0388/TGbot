#!/usr/bin/env python3

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from botcalendar import BotCalendar
from config import Config

config = Config()
CAL = BotCalendar(config.calendar["API_KEY"], config.calendar["CALID"])

print(' CHECK '.center(80, '+'))
CAL.check()

print('', end='\n\n')

print(' get_urgentEvents '.center(80, '+'))
CAL.get_urgentEvents()
