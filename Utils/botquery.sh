#!/usr/bin/env bash

IP=$3
PORT=$4
TOKEN=$5
TEXT=$6
DATE=$(date +%s)
IPPORT="https://$IP:$PORT/$TOKEN"

#============Message with Text============
text()
{
  curl -v -k -X POST -H "Content-Type: application/json" -H "Cache-Control: no-cache" -d '{"update_id":10000, "message":{ "date":'"$(date +%s)"', "chat":{ "last_name":"Test Lastname", "id":1111111, "type": "private", "first_name":"Test Firstname", "username":"Testusername"}, "message_id":'"${MID}"', "from":{ "last_name":"Test Lastname", "id":1111111, "first_name":"Test Firstname", "username":"Testusername"}, "text":"'"${TEXT}"'"}}' $IPPORT
}

#============Forwarded Message============
forward()
{
  curl -v -k -X POST -H "Content-Type: application/json" -H "Cache-Control: no-cache" -d '{ "update_id":10000, "message":{ "date":'"$(date +%s)"', "chat":{ "last_name":"Test Lastname", "id":1111111, "type": "private", "first_name":"Test Firstname", "username":"Testusername" }, "message_id":'"${MID}"', "from":{ "last_name":"Test Lastname", "id":1111111, "first_name":"Test Firstname", "username":"Testusername" }, "forward_from": { "last_name":"Forward Lastname", "id": 222222, "first_name":"Forward Firstname" }, "f orward_date":1441645550, "text":"/start" } }' $IPPORT;
}

#============Forwarded Channel Message============
forwardedChannel()
{
  curl -v -k -X POST -H "Content-Type: application/json" -H "Cache-Control: no-cache" -d '{ "update_id":10000, "message":{ "date":'"$(date +%s)"', "chat":{ "last_name":"Test Lastname", "type": "private", "id":1111111, "first_name":"Test Firstname", "username":"Testusername" }, "message_id":'"${MID}"', "from":{ "last_name":"Test Lastname", "id":1111111, "first_name":"Test Firstname", "username":"Testusername" }, "forward_from": { "id": -10000000000, "type": "channel", "title": "Test channel" }, "forward_date":1441645550, "text":"/start" } }' $IPPORT;
}

#============Message with a reply============
reply()
{
  curl -v -k -X POST -H "Content-Type: application/json" -H "Cache-Control: no-cache" -d '{ "update_id":10000, "message":{ "date":'"$(date +%s)"', "chat":{ "last_name":"Test Lastname", "type": "private", "id":1111111, "first_name":"Test Firstname", "username":"Testusername" }, "message_id":'"${MID}"', "from":{ "last_name":"Test Lastname", "id":1111111, "first_name":"Test Firstname", "username":"Testusername" }, "text":"/start", "reply_to_message":{ "date":1441645000, "chat":{ "last_name":"Reply Lastname", "type": "private", "id":1111112, "first_name":"Reply Firstname", "username":"Testusername" }, "message_id":1334, "text":"Original" } } }' $IPPORT;
}

#============Edited message============
edited()
{
  curl -v -k -X POST -H "Content-Type: application/json" -H "Cache-Control: no-cache" -d '{ "update_id":10000, "edited_message":{ "date":'"$(date +%s)"', "chat":{ "last_name":"Test Lastname", "type": "private", "id":1111111, "first_name":"Test Firstname", "username":"Testusername" }, "message_id":'"${MID}"', "from":{ "last_name":"Test Lastname", "id":1111111, "first_name":"Test Firstname", "username":"Testusername" }, "text":"Edited text", "edit_date": 1441646600 } }' $IPPORT;
}

#============Message with entities============
entities()
{
  curl -v -k -X POST -H "Content-Type: application/json" -H "Cache-Control: no-cache" -d '{ "update_id":10000, "message":{ "date":'"$(date +%s)"', "chat":{ "last_name":"Test Lastname", "type": "private", "id":1111111, "first_name":"Test Firstname", "username":"Testusername" }, "message_id":'"${MID}"', "from":{ "last_name":"Test Lastname", "id":1111111, "first_name":"Test Firstname", "username":"Testusername" }, "text":"Bold and italics", "entities": [ { "type": "italic", "offset": 9, "length": 7 }, { "type": "bold", "offset": 0, "length": 4 } ] } }' $IPPORT;
}

#============Message with audio============
audio()
{
  curl -v -k -X POST -H "Content-Type: application/json" -H "Cache-Control: no-cache" -d '{ "update_id":10000, "message":{ "date":'"$(date +%s)"', "chat":{ "last_name":"Test Lastname", "type": "private", "id":1111111, "first_name":"Test Firstname", "username":"Testusername" }, "message_id":'"${MID}"', "from":{ "last_name":"Test Lastname", "id":1111111, "first_name":"Test Firstname", "username":"Testusername" }, "audio": { "file_id": "AwADBAADbXXXXXXXXXXXGBdhD2l6_XX", "duration": 243, "mime_type": "audio/mpeg", "file_size": 3897500, "title": "Test music file" } } }' $IPPORT;
}

#============Voice message============
voice()
{
  curl -v -k -X POST -H "Content-Type: application/json" -H "Cache-Control: no-cache" -d '{ "update_id":10000, "message":{ "date":'"$(date +%s)"', "chat":{ "last_name":"Test Lastname", "type": "private", "id":1111111, "first_name":"Test Firstname", "username":"Testusername" }, "message_id":'"${MID}"', "from":{ "last_name":"Test Lastname", "id":1111111, "first_name":"Test Firstname", "username":"Testusername" }, "voice": { "file_id": "AwADBAADbXXXXXXXXXXXGBdhD2l6_XX", "duration": 5, "mime_type": "audio/ogg", "file_size": 23000 } } }' $IPPORT;
}

#============Message with a document============
document()
{
  curl -v -k -X POST -H "Content-Type: application/json" -H "Cache-Control: no-cache" -d '{ "update_id":10000, "message":{ "date":'"$(date +%s)"', "chat":{ "last_name":"Test Lastname", "type": "private", "id":1111111, "first_name":"Test Firstname", "username":"Testusername" }, "message_id":'"${MID}"', "from":{ "last_name":"Test Lastname", "id":1111111, "first_name":"Test Firstname", "username":"Testusername" }, "document": { "file_id": "AwADBAADbXXXXXXXXXXXGBdhD2l6_XX", "file_name": "Testfile.pdf", "mime_type": "application/pdf", "file_size": 536392 } } }' $IPPORT;
}

new_member()
{
    curl -v -k -X POST -H "Content-Type: application/json" -H "Cache-Control: no-cache" -d '{"message": {"new_chat_member": {"first_name": "Test Firstname", "is_bot": false, "id": 1111111}, "from": {"first_name": "Test Firstname", "is_bot": false, "id": 1111111, "last_name": "Test Lastname"}, "new_chat_participant": {"first_name": "Test Firstname", "is_bot": false, "id": 11111111}, "chat":{ "type": "private", "id":1111111}, "message_id": 11111111, "date": "'"${DATE}"'", "new_chat_members": [{"first_name": "Test Firstname", "is_bot": false, "id": 1111112}]}}'  $IPPORT;
}

###QUERIES CONTAIN NO MESSAGE_ID###

#============Inline query============
inline()
{
  curl -v -k -X POST -H "Content-Type: application/json" -H "Cache-Control: no-cache" -d '{ "update_id":10000, "inline_query":{ "id": 134567890097, "from":{ "last_name":"Test Lastname", "type": "private", "id":1111111, "first_name":"Test Firstname", "username":"Testusername" }, "query": "inline query", "offset": "" } }' $IPPORT;
}

#============Chosen inline query============
chosenInline()
{
  curl -v -k -X POST -H "Content-Type: application/json" -H "Cache-Control: no-cache" -d '{ "update_id":10000, "chosen_inline_result":{ "result_id": "12", "from":{ "last_name":"Test Lastname", "type": "private", "id":1111111, "first_name":"Test Firstname", "username":"Testusername" }, "query": "inline query", "inline_message_id": "1234csdbsk4839" } }' $IPPORT;
}

#============Callback query============
callback()
{
  curl -v -k -X POST -H "Content-Type: application/json" -H "Cache-Control: no-cache" -d '{ "update_id":10000, "callback_query":{ "id": "4382bfdwdsb323b2d9", "from":{ "last_name":"Test Lastname", "type": "private", "id":1111111, "first_name":"Test Firstname", "username":"Testusername" }, "data": "Data from button callback", "inline_message_id": "1234csdbsk4839" } }' $IPPORT;
}

# USAGE
# ./botquery.sh MESSAGEID FUNCTION IP PORT TOKEN

MID=$1

$2

exit 0
