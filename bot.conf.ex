[server]
ip = 1.2.3.4
port = 443
key = YOUR_Private.key
cert = YOUR_Public.pem
live = True
db = messageQueue.db

[telegram]
chat_id = -100000000
token = 987654321:ABCDEFGHIJKLMNOPQRSTUVWXYZ
botname = @Botty_the_bot
# time_limit is currently set to 23 hours
time_limit = 82800
botsay = True
botwelcome = True
url = https://api.telegram.org/bot{}/

[group_info]
name = MY_GROUP
rules_link = https://mygroup.com/group/link/to/rules
upcoming = https://mygroup.com/group/link/to/upcoming/events/post

[calendar]
app_name = Bot Calendar Access
cal_id = A0B1C2D3E4F5G6H7I8J9K0@group.calendar.google.com
api_key = Z00Y11X22W33V44U55T66S77R88Q99

[events]
list = True
reminders = True

[triggers]
on = True
name = '(BOT|@BOT|bot|@bot)'
trigger_one = 'Hey {}'
trigger_two = '.*[pP]oke.* {}'

[responses]
name_one = You rang?
name_two = What was that?
welcome = Welcome to the {} chat, {}!

    Take a moment and read our rules before getting started. You can find them at {}.

