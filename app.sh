#!/bin/sh
#pip install -r requirements.txt
gunicorn --bind 0.0.0.0:27017 --workers "${WORKERS}" --timeout ${TIMEOUT} app:app