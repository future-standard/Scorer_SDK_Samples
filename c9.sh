#!/bin/bash

get_ipv4addrs() {
  /sbin/ifconfig -a                                 |
  grep inet[^6]                                     |
  sed 's/.*inet[^6][^0-9]*\([0-9.]*\)[^0-9]*.*/\1/' |
  grep -v '^127\.'                                  |
  head -n 1
}

PORT=20003

# Handle stop option
if [ "$1" = "stop" ]; then
    ps -ef | grep node | grep c9sdk | grep server.js | grep -v grep | awk '{ print "kill -9", $2 }' | sh
    exit
fi

if [ "$1" = "ip" ]; then
    echo $(get_ipv4addrs)
    exit
fi

if [ "$1" = "port" ]; then
    echo $PORT
    exit
fi


#echo $(get_ipv4addrs)
/opt/scorer/bin/node ~/c9sdk/server.js --listen $(get_ipv4addrs) --port $PORT -a dev:scorer4sdk!
