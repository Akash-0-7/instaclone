#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install Pillow
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations myapp
python manage.py migrate