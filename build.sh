#!/usr/bin/env bash

pip install -r requirements.txt && cd app && python manage.py migrate && python manage.py collectstatic --noinput