#!/usr/bin/env bash

IP=$1
PORT=$2
APIKEY=$3
PUBLIC_KEY=$4
PRIVATE_KEY=$5

ST=$6
L=$7
O=$8

openssl req -newkey rsa:2048 -sha256 -nodes -keyout $PRIVATE_KEY -x509 -days 365 -out $PUBLIC_KEY -subj "/C=US/ST=$ST/L=$L/O=$O/CN=$IP"

curl -F "url=https://$IP:$PORT/$APIKEY" -F "certificate=@$PUBLIC_KEY" https://api.telegram.org/bot$APIKEY/setWebhook




