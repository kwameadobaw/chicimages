# Vercel Deployment Guide for ChicImages

This guide will help you deploy your Django application with PostgreSQL on Vercel.

## Prerequisites

- Vercel account (free tier available at [vercel.com](https://vercel.com))
- GitHub repository with your code
- Supabase PostgreSQL database (see `SUPABASE_SETUP.md`)

## Step 1: Prepare Your Repository

Make sure your repository has:

- ✅ Updated `vercel.json` configuration
- ✅ `vercel-build.sh` script
- ✅ Updated `requirements.txt` with `psycopg2-binary==2.9.9`
- ✅ Environment variables configured in Django settings

## Step 2: Connect to Vercel

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "New Project"
3. Import your GitHub repository
4. Vercel will automatically detect it's a Python project

## Step 3: Configure Environment Variables

In your Vercel project dashboard:

1. Go to **Settings** → **Environment Variables**
2. Add the following variables:

### Required Environment Variables

```
SECRET_KEY = your_django_secret_key_here
DEBUG = False
DB_NAME = postgres
DB_USER = postgres
DB_PASSWORD = your_supabase_password
DB_HOST = db.abcdefgh.supabase.co
DB_PORT = 5432
```

### Optional Environment Variables

```
EMAIL_HOST_USER = your_email@example.com
EMAIL_HOST_PASSWORD = your_email_password
```

**Important**:

- Set `DEBUG = False` for production
- Use a strong, unique `SECRET_KEY` for production
- Get your Supabase credentials from your Supabase dashboard

## Step 4: Deploy

1. Click **Deploy** in Vercel
2. Wait for the build to complete
3. Your app will be available at `https://your-project-name.vercel.app`

## Step 5: Run Database Migrations

After deployment, you need to run database migrations:

### Option 1: Using Vercel CLI (Recommended)

1. Install Vercel CLI:

   ```bash
   npm i -g vercel
   ```

2. Login to Vercel:

   ```bash
   vercel login
   ```

3. Link your project:

   ```bash
   vercel link
   ```

4. Run migrations:
   ```bash
   vercel env pull .env.local
   python manage.py migrate
   ```

### Option 2: Using Supabase Dashboard

1. Go to your Supabase dashboard
2. Navigate to **SQL Editor**
3. Run the Django migration commands manually

## Step 6: Create Superuser

Create an admin user for your deployed application:

```bash
vercel env pull .env.local
python manage.py createsuperuser
```

## Troubleshooting

### Build Failures

If you encounter build failures:

1. **Check the build logs** in Vercel dashboard
2. **Verify environment variables** are set correctly
3. **Ensure all dependencies** are in `requirements.txt`

### Database Connection Issues

1. **Check Supabase credentials** in environment variables
2. **Verify Supabase project** is active and not paused
3. **Check firewall settings** in Supabase dashboard

### Static Files Issues

For static files (CSS, JS, images):

1. **Configure static file serving** in your Django settings
2. **Use Vercel's static file handling** or a CDN
3. **Check STATIC_ROOT** and STATIC_URL settings

## Performance Optimization

### Database Optimization

1. **Enable connection pooling** in Supabase
2. **Add database indexes** for frequently queried fields
3. **Use database caching** for expensive queries

### Vercel Optimization

1. **Use Edge Functions** for simple operations
2. **Implement caching** with Vercel's caching features
3. **Optimize images** using Vercel's Image Optimization

## Monitoring and Logs

1. **View deployment logs** in Vercel dashboard
2. **Monitor database performance** in Supabase dashboard
3. **Set up error tracking** with services like Sentry

## Custom Domain (Optional)

1. Go to **Settings** → **Domains** in Vercel
2. Add your custom domain
3. Configure DNS settings as instructed
4. Update `ALLOWED_HOSTS` in Django settings

## Security Considerations

1. **Never commit** `.env` files to version control
2. **Use strong passwords** for database and admin accounts
3. **Enable HTTPS** (automatic with Vercel)
4. **Set up proper CORS** if using API endpoints
5. **Enable Row Level Security** in Supabase for production

## Cost Optimization

### Vercel Free Tier Limits

- 100GB bandwidth per month
- 100 serverless function invocations per day
- 1,000 build minutes per month

### Supabase Free Tier Limits

- 500MB database storage
- 2GB bandwidth per month
- 50,000 monthly active users

## Support and Resources

- **Vercel Documentation**: [vercel.com/docs](https://vercel.com/docs)
- **Supabase Documentation**: [supabase.com/docs](https://supabase.com/docs)
- **Django Deployment**: [docs.djangoproject.com/en/4.2/howto/deployment/](https://docs.djangoproject.com/en/4.2/howto/deployment/)

## Common Commands

```bash
# Deploy to Vercel
vercel --prod

# View deployment logs
vercel logs

# Pull environment variables
vercel env pull .env.local

# Run Django commands
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```
