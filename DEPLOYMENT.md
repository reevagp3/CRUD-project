# Deployment Guide

This guide provides step-by-step instructions for deploying your CRUD Flask application to production on Render.

## Prerequisites

- GitHub account with your repository
- Render account (https://render.com)
- Supabase account with PostgreSQL database
- Application properly configured with `.env` file

## Step 1: Prepare Your Repository

### 1.1 Ensure `.env` is not committed
Make sure your `.env` file is in `.gitignore`:

```bash
# Verify .gitignore contains .env
cat .gitignore | grep "^\.env"
```

### 1.2 Commit your code
```bash
git add .
git commit -m "Production-ready Flask CRUD application"
git push origin main
```

## Step 2: Prepare Supabase

### 2.1 Create items table
Log into Supabase and run this SQL in the SQL editor:

```sql
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2.2 Get connection string
1. Go to Project Settings → Database
2. Copy the "Connection string" (PostgreSQL)
3. It should look like: `postgresql://user:password@host:6543/database`

## Step 3: Deploy to Render

### 3.1 Create new Web Service

1. Log in to https://render.com
2. Click **"New +"** in the top navigation
3. Select **"Web Service"**
4. Connect your GitHub repository:
   - Click "Connect account" if needed
   - Search for your repository
   - Click "Connect" next to it

### 3.2 Configure the service

Fill in the following fields:

- **Name**: `crud-app` (or your preferred name)
- **Environment**: Select **Python 3**
- **Region**: Choose closest to your users
- **Branch**: `main` (or your default branch)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`

Leave other settings as default.

### 3.3 Add environment variables

Before clicking "Create Web Service", click **"Advanced"** and add environment variables:

| Key | Value |
|-----|-------|
| `FLASK_ENV` | `production` |
| `SECRET_KEY` | Generate a random secure string (use `python -c "import secrets; print(secrets.token_hex(32))"`) |
| `SUPABASE_DB_URL` | Your Supabase connection string from Step 2.2 |
| `PORT` | `3000` (Render will override this automatically) |

### 3.4 Deploy

1. Click **"Create Web Service"**
2. Wait for the deployment to complete (2-5 minutes)
3. You'll see a URL like `https://crud-app.onrender.com`

## Step 4: Verify Deployment

### 4.1 Check logs
On the Render dashboard, click on your service and check:
- **Logs** tab to see startup messages
- Look for "✅ Flask app created successfully with production environment"

### 4.2 Test the application

```bash
# Replace with your Render URL
curl https://crud-app.onrender.com/api/health

# Should return:
# {"database": "connected", "status": "ok"}
```

### 4.3 Access the dashboard
Open your browser to: `https://crud-app.onrender.com/ui`

You should see your CRUD dashboard with the dark theme.

## Step 5: Continuous Deployment

### 5.1 Enable auto-deploy
In Render dashboard:
1. Go to your Web Service
2. Settings → Auto-Deploy
3. Select "Yes" for "Auto-deploy on push to branch"

Now every time you push to `main`, Render will automatically redeploy your app.

## Troubleshooting

### Deployment fails

**Check the logs:**
```bash
# View deployment and runtime logs in Render dashboard
Logs tab → Service Logs
```

**Common issues:**

1. **Build fails - requirements.txt errors**
   - Ensure all packages in `requirements.txt` are compatible
   - Try: `pip install -r requirements.txt` locally first

2. **Service won't start - PORT errors**
   - Render automatically sets the `PORT` environment variable
   - Your app must read `PORT` from environment (✅ Already configured)

3. **Database connection errors**
   - Verify `SUPABASE_DB_URL` is correct in environment variables
   - Ensure Supabase database is running
   - Check SSL mode in connection string (should be `:6543` for pooler)

4. **503 Service Unavailable**
   - Check if database connection is working: Visit `/api/health`
   - Check logs for detailed error messages

### Cold starts

**Why it happens:**
- Free tier services on Render go to sleep after 15 minutes of inactivity
- First request after sleep takes longer to respond

**Solutions:**
- Upgrade to Paid tier (only while service is running)
- Use a monitoring service to keep the app awake

### Database connection issues

**Test database connection:**
```python
# Run this to test
python setup_db.py
```

**If connection fails:**
1. Verify connection string format: `postgresql://user:pass@host:6543/database`
2. Check Supabase database is not paused
3. Check firewall/IP restrictions in Supabase

## Performance Optimization

### 1. Use Render's paid tier for production
- 0.1 vCPU minimum (free restarts frequently)
- 0.5 vCPU recommended
- Pay-as-you-go pricing

### 2. Database optimization
- Connection pooling is already implemented ✅
- Monitor query performance in Supabase dashboard
- Add indexes if needed: `CREATE INDEX idx_items_name ON items(name);`

### 3. Monitor your app
Use Render's analytics:
- CPU usage
- Memory usage
- Response times
- Error rates

## Updating Your Application

### Deploy changes:

```bash
# Make changes locally
git add .
git commit -m "Your changes"
git push origin main

# If auto-deploy is enabled, Render will automatically redeploy
# If not, manually trigger in Render dashboard
```

### Zero-downtime deployments:
- Render handles this automatically
- Old instances continue serving requests while new ones start
- Typically takes 1-2 minutes

## Security Checklist

- ✅ `.env` file is in `.gitignore`
- ✅ `FLASK_ENV=production` is set
- ✅ `SECRET_KEY` is a secure random value (not the default)
- ✅ Database URL uses SSL (`sslmode='require'`)
- ✅ Connection pooling prevents exhaustion
- ✅ Input validation on server side
- ✅ Error messages don't leak sensitive data

## Monitoring & Maintenance

### Set up alerts
In Render dashboard:
1. Settings → Alerts
2. Create alerts for:
   - High CPU usage
   - High memory usage
   - Build failures
   - Deploy failures

### Regular maintenance
- Monitor logs for errors
- Check database connection health weekly
- Review error rates in logs

## Advanced: Custom Domain

1. In Render dashboard, go to your service
2. Settings → Custom Domain
3. Add your domain (e.g., `myapp.example.com`)
4. Update DNS records as shown in Render

## Next Steps

- ✅ Application deployed to production
- 📊 Monitor performance in Render dashboard
- 🔐 Implement authentication if needed
- 📈 Scale as your user base grows

## Support

- Render Documentation: https://render.com/docs
- Flask Documentation: https://flask.palletsprojects.com
- Supabase Documentation: https://supabase.io/docs

---

**Last Updated**: April 2026
