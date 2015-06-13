#!/bin/bash

PATH=/usr/bin:/usr/sbin:/bin:/sbin

mkdir /tmp/log
LOG=/tmp/log/bottleServer.log


echo "Launching infinite loop..." >> $LOG
while true; do
	# Clean up in case of an unclean exit
	echo "Cleaning up bottle..." >> $LOG
	producer=`ps auxww | grep python | grep app.py | wc -l`
	if [ "$producer" -ne 0 ]
	then
		kill -9 `ps auxww | grep python | grep app.py | tr -s ' ' |  cut -d\  -f2` &
	fi

	# Launch the viewer
	python ~/.bottle_server/app.py >> $LOG 2>> $LOG 
done
