#!/bin/bash 

case "$1" in
    start)
        cd {{basedir}} && python server.py &
    ;;
    stop)
        PIDS=`ps -ef | grep "python server.py" | grep -v grep | awk '{print $2}'`
        for PID in $PIDS
        do
            kill $PID
        done
    ;;
    *)
        echo "Usage {start|stop}"
    exit 1
    ;;
esac
exit 0