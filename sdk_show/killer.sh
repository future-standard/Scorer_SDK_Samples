#!/bin/sh

# Kill Flask processes
ps -ef | grep sdk_show | grep -v grep | awk '{ print "kill -9", $2 }' | sh
