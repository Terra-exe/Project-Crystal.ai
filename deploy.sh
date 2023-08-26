#!/bin/bash

cd /path/to/your/app
git pull
pkill -f "your-app-name"
nohup python3 app.py > output.log &
