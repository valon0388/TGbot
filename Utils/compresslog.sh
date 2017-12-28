#!/usr/bin/env bash

BOTNAME=$1

gzo(){ 
    FILE=$1; 
    NEW="${FILE}s/$BOTNAMElog.$(date +'%y-%m-%d--%H:%M:%S').gz"; 
    touch $NEW; 
    gzip -9 -c $FILE > $NEW && echo '' > $FILE; 
} 

gzo /home/$BOTNAME/$BOTNAMElog;

exit 0
