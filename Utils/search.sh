#!/usr/bin/env bash

DATE=$1

TEXT=$2

for FILE in $(ls | grep "$DATE"); do echo; echo "============${FILE}============"; zcat $FILE | grep "$TEXT"; done;
