#!/usr/bin/env bash

cd app && gunicorn CRUD.wsgi:application
