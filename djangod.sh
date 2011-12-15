#!/bin/bash

DIR="/home/patrik/programmering/python/gruvdrift/gruvdrift"
PIDFILE="/tmp/gruvdrift-django.pid"
cd $DIR

case "$1" in
    start)
        echo "Starting django fcgi server at $DIR"
        #./manage.py runfcgi method=threaded host=127.0.0.1 port=3033 pidfile=$PIDFILE
        ./manage.py runfcgi method=prefork socket=/tmp/mysite.sock pidfile=$PIDFILE
        ;;
    stop)
        echo "Stopping django fcgi server at $DIR"
        if [ -f $PIDFILE ]; then
            kill $( cat $PIDFILE )
            rm $PIDFILE
        fi
        ;;
    restart)
        $0 stop
        $0 start
        ;;
    *)
        echo "Whaat?"
        ;;
esac
