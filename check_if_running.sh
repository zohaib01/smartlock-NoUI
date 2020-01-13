#!/bin/sh
if ps -ef | grep -v grep | grep smartlock ; then
	date
	echo "OK process is running"
        exit 0
else

	cd /
	cd home/pi/
	sudo python smartlock.py & >>/home/pi/cron.log 2>&1
	cd /

	date
	echo " ERROR process restarted"
	ps -ef | grep smartlock 
        exit 0
fi
