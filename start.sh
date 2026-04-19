#!/usr/bin/env bash

cd app && gunicorn app.wsgi:application
