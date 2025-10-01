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

echo "✅ Build completed successfully!"
