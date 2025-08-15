#!/bin/bash
source venv/bin/activate
export FLASK_APP=app.py
export FLASK_ENV=development  # Optional: enables auto-reload
flask run --host=0.0.0.0 --port=5501

