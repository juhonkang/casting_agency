# Deployment Guide

This guide covers deploying the Trivia API to production using either Render or Heroku.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Option 1: Deploy to Render (Recommended)](#option-1-deploy-to-render-recommended)
- [Option 2: Deploy to Heroku](#option-2-deploy-to-heroku)
- [Post-Deployment Setup](#post-deployment-setup)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before deploying, ensure you have:

1. **Completed Auth0 Setup** - Follow AUTH0_SETUP.md to configure Auth0
2. **Git Repository** - Code pushed to GitHub
3. **Database Ready** - PostgreSQL database with sample data
4. **Environment Variables** - All required configuration values

## Option 1: Deploy to Render (Recommended)

Render offers a free tier with automatic deployments from GitHub.

### Step 1: Create Render Account

1. Visit [https://render.com](https://render.com)
2. Sign up with GitHub (recommended for easy deployment)
3. Verify your email address

### Step 2: Prepare Your Application

The following files are already configured in the `backend/` directory:

- `render.yaml` - Render service configuration
- `Procfile` - Process file for web service
- `runtime.txt` - Python version specification
- `requirements.txt` - Python dependencies

### Step 3: Create Database on Render

1. Go to Render Dashboard
2. Click "New +" → "PostgreSQL"
3. Configure:
   - **Name**: `trivia-db`
   - **Database**: `trivia`
   - **User**: `trivia_user`
   - **Region**: Choose closest to you
   - **Plan**: Free
4. Click "Create Database"
5. Wait for database to provision (2-3 minutes)
6. Copy the **Internal Database URL** (starts with `postgresql://`)

### Step 4: Deploy Web Service

1. Go to Render Dashboard
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `trivia-api` (or your preferred name)
   - **Region**: Same as database
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn 'flaskr:create_app()'`
   - **Plan**: Free

### Step 5: Configure Environment Variables

In the Render Web Service settings, add these environment variables:

```
AUTH0_DOMAIN=dev-8607typd5q1j6mig.us.auth0.com
ALGORITHMS=["RS256"]
API_AUDIENCE=trivia-api
FLASK_ENV=production
DATABASE_URL=postgresql://trivia_user:ZNA8cIXEsRX7pdt9idJbykpgp2ZAx8rd@dpg-d3ugonndiees73e95ri0-a/trivia_xrm3
```

**⚠️ Security Note**: The DATABASE_URL above contains real credentials. For production, use your own database URL from Render/Heroku dashboard.

**✅ Auth0 Configuration Verified**: All Auth0 settings above are confirmed correct and ready for production.

### Step 6: Deploy

1. Click "Create Web Service"
2. Render will automatically:
   - Clone your repository
   - Install dependencies
   - Start the application
3. Monitor the deployment logs
4. Once deployed, you'll see "Your service is live"
5. Copy your live URL: `https://your-app.onrender.com`

### Step 7: Initialize Database

Use Render's shell to populate the database:

```bash
# In Render Dashboard → Shell
python manage.py db upgrade
# Or manually run SQL
psql $DATABASE_URL < trivia.psql
```

## Option 2: Deploy to Heroku

### Step 1: Install Heroku CLI

**macOS:**
```bash
brew tap heroku/brew && brew install heroku
```

**Windows:**
Download from [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

**Linux:**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

### Step 2: Login to Heroku

```bash
heroku login
```

### Step 3: Create Heroku App

```bash
cd backend
heroku create trivia-api-yourname
```

### Step 4: Add PostgreSQL Database

```bash
heroku addons:create heroku-postgresql:essential-0
```

### Step 5: Configure Environment Variables

```bash
heroku config:set AUTH0_DOMAIN='your-tenant.us.auth0.com'
heroku config:set ALGORITHMS='["RS256"]'
heroku config:set API_AUDIENCE='trivia-api'
heroku config:set FLASK_ENV='production'
```

### Step 6: Deploy Application

```bash
git push heroku main
```

### Step 7: Initialize Database

```bash
# Run migrations
heroku run python manage.py db upgrade

# Or populate with sample data
heroku pg:psql < trivia.psql
```

### Step 8: Open Your App

```bash
heroku open
```

## Post-Deployment Setup

### 1. Update Auth0 Application URLs

**Current Auth0 Configuration Verified:**
- ✅ Domain: `dev-8607typd5q1j6mig.us.auth0.com`
- ✅ API Audience: `trivia-api`
- ✅ Algorithm: `RS256`
- ✅ Resource Server: Trivia API with 4 scopes configured

**Required Updates for Production:**

1. **Update SPA Application (Trivia Test Client)**
   - Go to Auth0 Dashboard → Applications → "Trivia Test Client" (ID: HFDzwNkABHS817OOsBVf3gqEpwAqngoU)
   - Add your production URLs to:
     - **Allowed Callback URLs**: `https://your-app.onrender.com/callback`
     - **Allowed Logout URLs**: `https://your-app.onrender.com`
     - **Allowed Web Origins**: `https://your-app.onrender.com`
   - Keep existing localhost URLs for development
   - Save Changes

2. **Verify Machine-to-Machine Application**
   - Application "Trivia API (Test Application)" (ID: DmX6LtgjWMlo0rVrXxRWbDtHMQ6NIthx) is correctly configured
   - No URL updates needed for M2M applications

### 2. Test API Endpoints

Test your live API:

```bash
# Get categories (requires authentication)
curl https://your-app.onrender.com/categories \
  -H "Authorization: Bearer YOUR_TOKEN"

# Health check
curl https://your-app.onrender.com/health
```

### 3. Update README

Add your live deployment URL to the README.md file:

```markdown
## Live Demo

API: https://your-app.onrender.com
```

## Auth0 Configuration Reference

### Current Applications (Verified)

**1. Trivia Test Client (SPA)**
- **Client ID**: `HFDzwNkABHS817OOsBVf3gqEpwAqngoU`
- **Type**: Single Page Application
- **Current URLs**: `http://localhost:3000`
- **Action Required**: Add production URLs for deployment

**2. Trivia API (Test Application)**
- **Client ID**: `DmX6LtgjWMlo0rVrXxRWbDtHMQ6NIthx`
- **Type**: Machine-to-Machine (Non-Interactive)
- **Status**: ✅ Ready for production
- **Action Required**: None

### Resource Server (API)
- **Name**: Trivia API
- **Identifier**: `trivia-api`
- **Scopes**: `get:questions`, `get:categories`, `post:questions`, `delete:questions`
- **Signing Algorithm**: RS256
- **Token Lifetime**: 24 hours

### Quick Auth0 Updates Checklist

- [ ] Update SPA application URLs for production domain
- [ ] Test authentication with production URLs
- [ ] Verify all scopes are working correctly
- [ ] Monitor Auth0 logs for any issues

## Environment Variables

### Required Variables

| Variable | Description | Verified Value |
|----------|-------------|----------------|
| `AUTH0_DOMAIN` | Your Auth0 tenant domain | `dev-8607typd5q1j6mig.us.auth0.com` ✅ |
| `ALGORITHMS` | JWT signing algorithms | `["RS256"]` ✅ |
| `API_AUDIENCE` | Auth0 API identifier | `trivia-api` ✅ |
| `DATABASE_URL` | PostgreSQL connection string | Auto-set by platform |
| `FLASK_ENV` | Flask environment | `production` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | Auto-generated |
| `LOG_LEVEL` | Logging level | `INFO` |

## Monitoring and Maintenance

### View Logs

**Render:**
```bash
# Real-time logs in Dashboard → Logs tab
# Or use Render CLI:
render logs
```

**Heroku:**
```bash
heroku logs --tail
```

### Database Backups

**Render:**
- Free tier: Manual backups only
- Paid tiers: Automatic daily backups

**Heroku:**
```bash
heroku pg:backups:capture
heroku pg:backups:download
```

### Scaling

**Render:**
- Upgrade to paid plan for auto-scaling
- Dashboard → Service → Settings → Scale

**Heroku:**
```bash
heroku ps:scale web=2
```

## Troubleshooting

### Common Issues

#### Application Crashes on Startup

**Symptoms:** Service fails to start, shows error in logs

**Solutions:**
1. Check logs for specific error message
2. Verify all environment variables are set correctly
3. Ensure `Procfile` and `requirements.txt` are in `backend/` directory
4. Verify Python version matches `runtime.txt`

#### Database Connection Errors

**Symptoms:** 500 errors, "database connection failed"

**Solutions:**
1. Verify `DATABASE_URL` environment variable
2. Check database is running in same region
3. Ensure database credentials are correct
4. Run `db upgrade` to create tables

#### Auth0 Authentication Fails

**Symptoms:** 401 errors, "invalid token"

**Solutions:**
1. Verify `AUTH0_DOMAIN` is correct (no https://)
2. Check `API_AUDIENCE` matches Auth0 API identifier
3. Ensure token is not expired (24-hour expiration)
4. Verify Auth0 allowed origins include deployment URL

#### Rate Limiting Issues

**Symptoms:** 429 "Rate limit exceeded" errors

**Solutions:**
1. For development: Temporarily increase limits in code
2. For production: Upgrade rate limiting storage from memory to Redis
3. Configure Redis on Render/Heroku for persistent rate limiting

### Getting Help

**Render Support:**
- Documentation: https://render.com/docs
- Community: https://community.render.com
- Support: support@render.com

**Heroku Support:**
- Documentation: https://devcenter.heroku.com
- Support: https://help.heroku.com

## Performance Optimization

### Database Connection Pooling

Already configured in `models.py`:
```python
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
}
```

### Caching

For improved performance, consider adding Redis caching:

**Render:**
```bash
# Add Redis service in Dashboard
# Update code to use Redis for caching
```

**Heroku:**
```bash
heroku addons:create heroku-redis:mini
```

### CDN for Static Assets

If serving frontend from same deployment:
- Use Cloudflare or similar CDN
- Configure CORS appropriately

## Security Checklist

Before going live, verify:

- [ ] `FLASK_ENV=production` is set
- [ ] Debug mode is disabled
- [ ] Strong `SECRET_KEY` is configured
- [ ] Database credentials are secure
- [ ] HTTPS is enforced (automatic on Render/Heroku)
- [ ] CORS is configured for specific origins (not `*`)
- [ ] Rate limiting is enabled
- [ ] Auth0 URLs are restricted to production domains
- [ ] Sensitive data is not logged
- [ ] Database backups are configured

## Continuous Deployment

### Automatic Deploys (Render)

Render automatically deploys when you push to GitHub:

1. Dashboard → Service → Settings
2. **Auto-Deploy**: Enabled by default
3. Choose branch (usually `main`)
4. Every push triggers new deployment

### Automatic Deploys (Heroku)

Enable GitHub integration:

1. Dashboard → Deploy → Deployment method
2. Choose "GitHub"
3. Connect repository
4. Enable "Automatic deploys" from `main` branch

## Next Steps

After successful deployment:

1. ✅ Test all API endpoints with Postman
2. ✅ Verify authentication works with real tokens
3. ✅ Monitor application logs for errors
4. ✅ Set up database backups
5. ✅ Configure custom domain (optional)
6. ✅ Add monitoring/alerting (e.g., Sentry)
7. ✅ Document API URL for users

---

**Need Help?** Check the [README.md](README.md) or open an issue in the repository.
