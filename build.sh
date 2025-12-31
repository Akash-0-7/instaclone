#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run migrations (Render should only EXECUTE migrations, not create them)
python manage.py migrate

# Create superuser if needed
# python manage.py createsuperuser --no-input || true