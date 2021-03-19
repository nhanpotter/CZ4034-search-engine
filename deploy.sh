#!/bin/bash

git pull
source .venv/bin/activate
pip3 install -r requirements.txt
python3 migrate_data.py
ps axf|grep "flask"|grep -v grep| awk '{print "kill -9 " $1}'|sh
export FLASK_APP=server.py
nohup flask run --host=0.0.0.0 > nohup.out 2>&1 &

echo "Done deploy"
