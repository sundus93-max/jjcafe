#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py makemigrations --no-input

python manage.py migrate --no-input

# Create superuser only if it doesn't exist
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'sundus.93@gmail.com', 'jjcafe@2026')
    print('Superuser created')
else:
    print('Superuser already exists - skipped')
"
