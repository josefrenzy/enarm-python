#!/bin/sh
gunicorn --bind 0.0.0.0:5001 --threads 2 --workers 1 rest_srv:app