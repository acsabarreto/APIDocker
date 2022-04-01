#!/bin/sh
#pip install -r requirements.txt
opentelemetry-instrument --service_name=API --traces_exporter zipkin_json  gunicorn --bind 0.0.0.0:27017 --workers "${WORKERS}" --timeout ${TIMEOUT} app:app &
gunicorn --bind 0.0.0.0:27018 openTelemetryExtrator:app
