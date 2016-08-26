#!/usr/bin/env bash

python manage.py create_db
python manage.py db init
python manage.py db migrate
