#!/usr/bin/env bash

gunicorn CRUD.wsgi:application 
