#!/bin/bash

DIR="/home/patrik/programmering/python/gruvdrift/gruvdrift"
SOCK="/tmp/django.sock"
PIDFILE="/tmp/gruvdrift-django.pid"
cd $DIR

case "$1" in
    start)
        echo "Starting django fcgi server at $SOCK"
        #./manage.py runfcgi method=threaded host=127.0.0.1 port=3033 pidfile=$PIDFILE
        ./manage.py runfcgi protocol=fcgi method=prefork socket=$SOCK pidfile=$PIDFILE
        ;;
    stop)
        echo "Stopping django fcgi server at $SOCK"
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
