#!/bin/sh

echo ">> Running Django setup..."
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py create_default_superuser || true
python manage.py load_from_supabase || true

echo ">> Starting Supervisor..."
exec supervisord -c /etc/supervisord.conf