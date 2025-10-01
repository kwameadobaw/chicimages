# Supabase PostgreSQL Setup Guide for ChicImages

This guide will help you migrate your Django application from SQLite to PostgreSQL using Supabase.

## Prerequisites

- A Supabase account (free tier available at [supabase.com](https://supabase.com))
- Python 3.8+ installed
- Your Django project (already set up)

## Step 1: Create a Supabase Project

1. Go to [supabase.com](https://supabase.com) and sign up/login
2. Click "New Project"
3. Choose your organization
4. Enter project details:
   - **Name**: `chicimages` (or your preferred name)
   - **Database Password**: Choose a strong password (save this!)
   - **Region**: Choose the closest to your location
5. Click "Create new project"
6. Wait for the project to be created (usually takes 1-2 minutes)

## Step 2: Get Database Connection Details

1. In your Supabase dashboard, go to **Settings** → **Database**
2. Scroll down to **Connection string**
3. Copy the connection details. You'll need:
   - **Host**: The hostname (e.g., `db.abcdefgh.supabase.co`)
   - **Database name**: Usually `postgres`
   - **Username**: Usually `postgres`
   - **Password**: The password you set when creating the project
   - **Port**: `5432`

## Step 3: Configure Your Local Environment

1. **Install the new requirements**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Create your environment file**:

   - Copy `env.example` to `.env`
   - Fill in your Supabase credentials:

   ```env
   # Database settings
   DB_NAME=postgres
   DB_USER=postgres
   DB_PASSWORD=your_supabase_password
   DB_HOST=db.abcdefgh.supabase.co
   DB_PORT=5432

   # Django settings
   SECRET_KEY=your_django_secret_key_here
   DEBUG=True

   # Email settings (if using)
   EMAIL_HOST_USER=your_email@example.com
   EMAIL_HOST_PASSWORD=your_email_password
   ```

## Step 4: Run the Migration

1. **Run the migration script**:

   ```bash
   python migrate_to_postgres.py
   ```

   This script will:

   - Backup your current SQLite database
   - Test the PostgreSQL connection
   - Run Django migrations
   - Optionally create a superuser

2. **If the migration script fails**, you can run migrations manually:
   ```bash
   python manage.py migrate
   ```

## Step 5: Verify the Setup

1. **Test your application**:

   ```bash
   python manage.py runserver
   ```

2. **Access Django admin**:

   - Go to `http://127.0.0.1:8000/admin/`
   - Login with your superuser credentials

3. **Check the database**:
   - In Supabase dashboard, go to **Table Editor**
   - You should see your Django tables (portfolio_category, portfolio_photo, etc.)

## Step 6: Migrate Existing Data (Optional)

If you have existing data in your SQLite database that you want to migrate:

1. **Export data from SQLite**:

   ```bash
   python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission > data.json
   ```

2. **Load data into PostgreSQL**:
   ```bash
   python manage.py loaddata data.json
   ```

## Troubleshooting

### Connection Issues

- **Check your .env file**: Make sure all database credentials are correct
- **Verify Supabase project**: Ensure your project is active and not paused
- **Check firewall**: Make sure your IP is not blocked by Supabase

### Migration Issues

- **Clear migrations**: If you have migration conflicts:

  ```bash
  python manage.py migrate portfolio zero
  python manage.py migrate
  ```

- **Reset database**: If needed, you can reset your Supabase database:
  - Go to Supabase dashboard → Settings → Database
  - Click "Reset database" (⚠️ This will delete all data!)

### Performance Issues

- **Connection pooling**: For production, consider using Supabase's connection pooling
- **Indexing**: Add database indexes for frequently queried fields
- **Caching**: Implement Redis caching for better performance

## Production Deployment

When deploying to production:

1. **Update environment variables**:

   ```env
   DEBUG=False
   SECRET_KEY=your_production_secret_key
   ```

2. **Set up static files**: Configure your web server to serve static files
3. **Enable HTTPS**: Ensure your domain uses SSL certificates
4. **Set up monitoring**: Monitor your database performance in Supabase dashboard

## Supabase Features You Can Use

Once connected, you can leverage Supabase features:

- **Real-time subscriptions**: For live updates
- **Row Level Security**: For data protection
- **Database functions**: For complex queries
- **Backups**: Automatic daily backups
- **Monitoring**: Built-in performance monitoring

## Support

- **Supabase Documentation**: [docs.supabase.com](https://docs.supabase.com)
- **Django PostgreSQL**: [docs.djangoproject.com/en/4.2/ref/databases/#postgresql-notes](https://docs.djangoproject.com/en/4.2/ref/databases/#postgresql-notes)
- **ChicImages Issues**: Create an issue in your project repository

## Security Notes

- Never commit your `.env` file to version control
- Use strong passwords for your database
- Regularly rotate your database password
- Enable Row Level Security in Supabase for production
- Use environment-specific settings for different deployments
