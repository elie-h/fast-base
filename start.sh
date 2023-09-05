#!/bin/sh

# Execute pre-start script
poetry run python app/pre_start.py

# Start Uvicorn server
poetry run uvicorn app.main:app --host 0.0.0.0 --port 7999 --reload --log-config app/uvicorn_disable_logging.json
