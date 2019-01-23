#!/bin/bash

while true; do
  # kill sniff script
  sudo ps -ef | grep sniff.py | grep -v grep | awk '{print $2}' | sudo xargs kill;
  sleep 1800; # every 30 minutes
done
