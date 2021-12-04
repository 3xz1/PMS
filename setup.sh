#!/bin/sh
echo "MYSQL_USER=$MYSQL_USER" >> .env
echo "MYSQL_ROOT_PASSWORD=$MYSQL_PASSWORD" >> .env
echo "MYSQL_DB=$MYSQL_DB" >> .env
echo "MYSQL_HOST=$MYSQL_HOST" >> .env
echo "FLASK_CONFIG=development" >> .env
echo "FLASK_APP=run.py" >> .env
