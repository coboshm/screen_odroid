#!/bin/bash

PATH=/usr/bin:/usr/sbin:/bin:/sbin

mkdir /tmp/log
LOG=/tmp/log/webcamScreen.log


echo "Launching infinite loop..." >> $LOG
while true; do
	# Clean up in case of an unclean exit
	echo "Cleaning up..." >> $LOG
	producer=`ps auxww | grep python | grep webcam.py | wc -l`
	if [ "$producer" -ne 0 ]
	then
		kill -9 `ps auxww | grep python | grep webcam.py | tr -s ' ' |  cut -d\  -f2` &
	fi

	# Launch the viewer
	python ~/.impactScreen/webcam.py >> $LOG 2>&1
done
