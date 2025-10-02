#!/bin/bash

# Vercel Build Script for Django with PostgreSQL
# This script ensures PostgreSQL dependencies are properly installed

set -e

echo "🚀 Starting Vercel build for ChicImages Django app"

# Install system dependencies for PostgreSQL
echo "📦 Installing PostgreSQL development libraries..."
apt-get update -qq
apt-get install -y -qq libpq-dev postgresql-client

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install -r requirements.txt

# Collect static files for deployment
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Ensure Django admin static files are available
echo "🔧 Setting up Django admin static files..."
python -c "
import os
import django
from django.conf import settings
from django.contrib import admin
from django.core.management import call_command

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chic_images.settings')
django.setup()

# Collect static files specifically for admin
call_command('collectstatic', '--noinput', verbosity=0)
print('Django admin static files collected successfully')
"

echo "✅ Build completed successfully!"
