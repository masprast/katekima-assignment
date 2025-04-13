#!/bin/bash

# This script is used to run the Django application for the assignment 2 of the Take Home Assignment
# It sets up the environment, installs dependencies, and starts the server

# Check if the script is run in the correct directory
if [ ! -d "Assignment 2" ] && [ ! -f "requirements.txt" ]; then
    echo "Please run this script from the root directory of the 'Assignment 2' project"
    exit
fi

# Check if the virtual environment is already activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ====================================
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Virtual environment is already activated"
fi

# Installing requirements ...
echo ====================================
echo "Installing requirements..."
pip install -r requirements.txt
echo ====================================

# Django related
echo "Creating Migrations..."
python manage.py makemigrations
echo ====================================

echo "Starting Migrations..."
python manage.py migrate
echo ====================================

echo "Collecting statics..."
python manage.py collectstatic
echo ====================================

echo "Starting Server..."
python manage.py runserver 0.0.0.0:8000