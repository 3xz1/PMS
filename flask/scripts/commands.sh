#!/bin/bash
cd /flask
sleep 15
export FLASK_APP=run.py
export FLASK_CONFIG=development
flask db init
flask db migrate -m "Creating Tables"
flask db upgrade
uwsgi app.ini