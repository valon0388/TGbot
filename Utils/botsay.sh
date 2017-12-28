#!/usr/bin/env bash

TEXT=$1
IP=$2
PORT=$3
TOKEN=$4
PUBLIC_KEY=$5

IPPORT="https://$IP:$PORT/$TOKEN"

curl -v -k -X POST -H "Content-Type: application/json" -H "Cache-Control: no-cache" -E $PUBLIC_KEY -d '{"botsay": "'"${TEXT}"'"}' $IPPORT

# ./botsay.sh "Text goes here" IP PORT "TELEGRAM API KEY"

# ./botsay.sh "Text goes here" 1.2.3.4 443 "987654321:ABCDEFGHIJKLMNOPQRSTUVWXYZ"
