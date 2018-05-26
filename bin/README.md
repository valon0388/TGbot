# TGbot

This bot is being created to manage messages in a group Telegram conversation.
It's set up to use the webhook method and not poll for updates with getupdates.

Requirements: # Note that this is a python3 project and all packages will need
                to be the python3 variants.
    _thread
    datetime
    dateutil
    http
    io
    json
    os
    pprint
    pycurl
    queue
    re
    sqlite3
    ssl
    time


Currently Working Features:
    - Listens for updates from the Telegram api
    - Loads from and backs up messages to a sqlite database
        Deletes each message 23 hours after it has been posted.
    - Reads events from a Google Calendar
        posts next 3 events to chat once per day
        when '@<telegram-botname> eventlist' is said by any member of chat,
            the bot will post the next three events to the chat
        Checks to see if the next event in the google calendar is happening soon
            if it is, bot posts to chat with the Event name, time, and
            description. (Happens at 0, 1, 3, 6, 12, 24, 48, and 72 hours)
    - Each option is configurable and can be turned on and off with a setting in
        the config file.
    - Sends a welcome message contining the rules link whenever a user joins the
        chat.

Planned Features:
    Simple Polls (yes/no, or one question with choices)
    Triggers based on Regex.
        Bot detects trigger message containing "poke", randomly triggers one of
        the responses named poke_<number>


NOTE: The below config is specifially to explain each setting. Do not attempt to
Copy and paste this section into a config file. Run the application and a sample
config will be generated.
=============================  SAMPLE BOT CONFIG  =============================
[server]
ip = 1.2.3.4   # The IP that the server will be listening on
port = 443    #       ^ and port
key = YOUR_Private.key  # Private Key that will be used to decrypt incoming messages
cert = YOUR_Public.pem  # Public Key that the Telegram server will encrypt messages with
live = True  # Turn this to False for testing. Disables posts going to the chat.
db = messageQueue.db  # Name of the local database to store the messages in.

[telegram]
chat_id = -100000000  # Telegram chat ID
token = 987654321:ABCDEFGHIJKLMNOPQRSTUVWXYZ  # Telegram API token
botname = @Botty_the_bot  # Name of the bot in the chat.
# time_limit is currently set to 23 hours
time_limit = 82800  # Amount of time for messages to stay in chat.
botsay = True  # Set to False to disable posting messages to chat.
botwelcome = True  # Set to False to disable posting welcome messages
url = https://api.telegram.org/bot{}/  # DO NOT CHANGE: telegram api url

[group_info]
name = MY_GROUP  # Name of the group and/or chat
rules_link = https://mygroup.com/group/link/to/rules  # Link to a website with the rules
upcoming = https://mygroup.com/group/link/to/upcoming/events/post  # Link to an events post

[calendar]
app_name = Bot Calendar Access  # Google App Name (I don't believe that this is actually used anymore)
cal_id = A0B1C2D3E4F5G6H7I8J9K0@group.calendar.google.com  # Link to the publicly available calendar
api_key = Z00Y11X22W33V44U55T66S77R88Q99  # Google API token used to access the calendar

[events]
list = True  # List the upcoming events every day or when someone requests an eventlist
reminders = True  # Post reminders about individual events that are coming up soon.

[triggers] # each trigger should start with 'trigger_' followed by the trigger's name
on = True  # Respond to triggers or not
trigger_name = (BOT|@BOT|bot|@bot)    # Trigger for the bot's name. Manually set the regex here
trigger_hey = Hey {}        # Randomly defined trigger
trigger_poke = .*[pP]oke.* {}  # Randomly defined trigger

[responses]  # Responses for the items defined in the 'trigger' section
name_one = You rang?  # First response for the 'name' trigger
name_two = What was that?  # Second response for the 'name' trigger
welcome = Welcome to the {} chat, {}!  # Welcome message.

    Take a moment and read our rules before getting started. You can find them at {}.

