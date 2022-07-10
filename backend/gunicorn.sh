#!/bin/sh

gunicorn --chdir app --bind 0.0.0.0:5000 wsgi:app -w 2 --threads 2
