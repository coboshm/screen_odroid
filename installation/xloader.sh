#!/bin/bash

PATH=/usr/bin:/usr/sbin:/bin:/sbin

mkdir /tmp/log
LOG=/tmp/log/impactScreen.log

echo "Disabling screen power savings..." > $LOG


xset s off          # Don't activate screensaver
xset -dpms          # Disable DPMS (Energy Star) features
xset s noblank      # Don't blank the video device
sleep 10

echo "Launching infinite loop..." >> $LOG
while true; do
	# Clean up in case of an unclean exit
	echo "Cleaning up..." >> $LOG
	producer=`ps auxww | grep python | grep main.py | wc -l`
	if [ "$producer" -ne 0 ]
	then
		kill -9 `ps auxww | grep python | grep main.py | tr -s ' ' |  cut -d\  -f2` &
	fi
	killall chromium-browser

	# Launch the viewer
	python ~/.impactScreen/main.py >> $LOG 2>&1
done
