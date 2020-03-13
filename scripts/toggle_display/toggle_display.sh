#!/bin/bash
SERVICE="phoniebox_led_control"
SRVSTATE=$(ps -ef | grep ${SERVICE} | grep -v grep)
if [[ $SRVSTATE ]]
then
    echo "$SERVICE is running"
    service ${SERVICE} stop
else
    echo "$SERVICE stopped"
    service ${SERVICE} start
fi
