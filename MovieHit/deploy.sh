#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Run collectstatic
python manage.py collectstatic --noinput

# Restart the server (if needed)
sudo systemctl restart gunicorn

