#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

# Fix bad migration records before migrating
python manage.py shell -c "
from django.db import connection
cursor = connection.cursor()

# Delete bad proxy model migrations
bad_migrations = [
    ('cafe', '0002_customeruserproxy_staffuserproxy'),
    ('auth', '0014_delete_customeruserproxy_delete_staffuserproxy'),
]
for app, name in bad_migrations:
    cursor.execute(
        \"DELETE FROM django_migrations WHERE app=%s AND name=%s\",
        [app, name]
    )
    print(f'Cleaned migration: {app}.{name}')
print('Migration cleanup done')
"

python manage.py makemigrations --no-input

python manage.py migrate --no-input

# Create superuser only if not exists
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'sundus.93@gmail.com', 'jjcafe@2026')
    print('Superuser created')
else:
    print('Superuser already exists - skipped')
"
