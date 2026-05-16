#!/usr/bin/env bash

pip install -r requirements.txt 
cd app 
python manage.py makemigrations --merge
python manage.py migrate 
python manage.py collectstatic --noinput
python manage.py shell < rest_api/create_admin.py