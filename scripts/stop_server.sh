#!/bin/bash

# kills all processes PID running on port 80 - where flask server is running
pid=$(sudo lsof -ti TCP:80)
echo $pid
sudo kill -9 $pid
