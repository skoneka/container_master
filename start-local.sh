#!/bin/sh
exec gunicorn -c config.py wsgi -b :8080 --access-logfile -
