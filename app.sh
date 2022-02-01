#!/bin/sh
#pip install -r requirements.txt
gunicorn --bind 0.0.0.0:27017 app:app