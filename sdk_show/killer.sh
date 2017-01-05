#!/bin/sh

# Kill Flask processes
ps -ef | grep scorer_show_sdk | grep -v grep | awk '{ print "kill -9", $2 }' | sh
