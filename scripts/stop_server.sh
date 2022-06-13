#!/bin/bash

pid=$(sudo lsof -ti TCP:80)

if [ -z "$pid" ]; then
    echo "no processes running on port 80"
else
    echo "killing process ${pid} running on port 80"
    sudo kill -9 $pid
fi

