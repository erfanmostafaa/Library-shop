#!/bin/bash

python3 /app/src/manage.py makemigrations
python3 /app/src/manage.py migrate
python3 /app/src/manage.py runserver 0.0.0.0:8000
~                                                                               
~                                                  