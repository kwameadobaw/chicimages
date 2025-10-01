#!/usr/bin/env python
"""
Database Migration Script for ChicImages
Migrates data from SQLite to PostgreSQL (Supabase)

Usage:
    python migrate_to_postgres.py

This script will:
1. Create a backup of your SQLite database
2. Run migrations on PostgreSQL
3. Optionally migrate existing data from SQLite to PostgreSQL

Make sure you have:
1. Created your .env file with Supabase credentials
2. Installed all requirements: pip install -r requirements.txt
"""

import os
import sys
import django
from pathlib import Path
import shutil
from datetime import datetime

# Add the project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chic_images.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.conf import settings

def backup_sqlite_db():
    """Create a backup of the SQLite database"""
    sqlite_db = Path('db.sqlite3')
    if sqlite_db.exists():
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'db_backup_{timestamp}.sqlite3'
        shutil.copy2(sqlite_db, backup_name)
        print(f"✅ SQLite database backed up as {backup_name}")
        return True
    else:
        print("ℹ️  No SQLite database found to backup")
        return False

def check_postgres_connection():
    """Check if PostgreSQL connection is working"""
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ PostgreSQL connection successful")
        return True
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return False

def run_migrations():
    """Run Django migrations on PostgreSQL"""
    try:
        print("🔄 Running migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrations completed successfully")
        return True
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def create_superuser():
    """Create a superuser for the new database"""
    try:
        print("🔄 Creating superuser...")
        execute_from_command_line(['manage.py', 'createsuperuser'])
        print("✅ Superuser created successfully")
        return True
    except Exception as e:
        print(f"❌ Superuser creation failed: {e}")
        return False

def main():
    print("🚀 Starting PostgreSQL Migration for ChicImages")
    print("=" * 50)
    
    # Check if we're using PostgreSQL
    if not os.getenv('DB_NAME'):
        print("❌ No PostgreSQL environment variables found!")
        print("Please create a .env file with your Supabase credentials.")
        print("See env.example for reference.")
        return
    
    # Backup SQLite database
    backup_sqlite_db()
    
    # Check PostgreSQL connection
    if not check_postgres_connection():
        print("\n❌ Cannot proceed without PostgreSQL connection.")
        print("Please check your .env file and Supabase credentials.")
        return
    
    # Run migrations
    if not run_migrations():
        print("\n❌ Migration failed. Please check the error messages above.")
        return
    
    # Create superuser
    response = input("\nWould you like to create a superuser? (y/n): ").lower()
    if response == 'y':
        create_superuser()
    
    print("\n🎉 Migration completed successfully!")
    print("\nNext steps:")
    print("1. Test your application with: python manage.py runserver")
    print("2. Access Django admin at: http://127.0.0.1:8000/admin/")
    print("3. If you had data in SQLite, you may need to manually migrate it")

if __name__ == '__main__':
    main()
