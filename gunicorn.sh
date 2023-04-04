#!/bin/sh
gunicorn --bind 0.0.0.0:5001 --threads 2 --workers 1 --chdir ./src/main rest_srv:app