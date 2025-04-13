#!/bin/bash
echo "Creating Migrations..."
python manage.py makemigrations items purchases sells reports

echo ====================================
echo "Starting Migrations..."
python manage.py migrate
echo ====================================

echo "Collecting statics..."
python manage.py collectstatic
echo ====================================

echo "Starting Server..."
python manage.py runserver 0.0.0.0:8000