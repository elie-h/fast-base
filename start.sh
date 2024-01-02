#!/bin/sh

# Execute pre-start script
python app/pre_start.py

# Start Uvicorn server
uvicorn app.api:app --host 0.0.0.0 --port 7999 --reload --log-config app/uvicorn_disable_logging.json
