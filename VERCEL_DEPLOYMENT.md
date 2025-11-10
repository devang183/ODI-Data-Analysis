# Deployment Guide: Vercel (Frontend) + Render (Backend)

This guide explains how to deploy your ODI Cricket Analytics application with the frontend on Vercel and backend on Render.

## Architecture Overview

- **Frontend**: React + Vite deployed on Vercel
- **Backend**: Flask API deployed on Render
- **Database**: PostgreSQL on Render

## Prerequisites

1. GitHub/GitLab account with your code pushed
2. Vercel account (sign up at https://vercel.com)
3. Render account (sign up at https://render.com)

---

## Part 1: Deploy Backend on Render

### Step 1: Create PostgreSQL Database

1. Go to Render Dashboard: https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `odi-cricket-db`
   - **Database**: `odi_cricket`
   - **User**: `odi_user`
   - **Region**: Choose closest to your users
4. Click **"Create Database"**
5. Wait for provisioning (2-3 minutes)
6. **Save the connection details** - you'll need them

### Step 2: Upload Data to Database

After database is created, upload your cricket data:

```bash
# Get the External Database URL from Render dashboard
# Format: postgres://user:password@host:port/database

# Option A: If you have a dump file
pg_restore -d <EXTERNAL_DATABASE_URL> your_dump.sql

# Option B: Use psql
psql <EXTERNAL_DATABASE_URL> < your_dump.sql

# Option C: Use the upload script
# Update backend/.env with Render database credentials
python upload_jsons.py
```

### Step 3: Deploy Backend API

1. In Render Dashboard, click **"New +"** → **"Blueprint"**
2. Connect your Git repository
3. Render will detect `render.yaml` automatically
4. Click **"Apply"**
5. Render creates:
   - PostgreSQL database (if not already created)
   - Backend web service

**OR** Deploy manually:

1. Click **"New +"** → **"Web Service"**
2. Connect repository
3. Configure:
   - **Name**: `odi-cricket-backend`
   - **Root Directory**: Leave empty
   - **Environment**: Python 3
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && gunicorn app:app`
4. Add Environment Variables:
   - `DB_NAME`: (from database)
   - `DB_USER`: (from database)
   - `DB_PASSWORD`: (from database)
   - `DB_HOST`: (from database)
   - `DB_PORT`: `5432`
   - `FLASK_ENV`: `production`
5. Click **"Create Web Service"**

### Step 4: Verify Backend

1. Wait for deployment (3-5 minutes)
2. Open your backend URL: `https://your-backend.onrender.com`
3. Test health check: `https://your-backend.onrender.com/api/health`
   - Should return: `{"status": "healthy", "service": "odi-analytics-api"}`
4. **Copy the backend URL** - you'll need it for Vercel

---

## Part 2: Deploy Frontend on Vercel

### Step 1: Push Code to GitHub

```bash
git add .
git commit -m "Add Vercel deployment configuration"
git push origin main
```

### Step 2: Import Project to Vercel

1. Go to Vercel Dashboard: https://vercel.com/dashboard
2. Click **"Add New..."** → **"Project"**
3. Import your Git repository
4. Vercel auto-detects it as a Vite project

### Step 3: Configure Build Settings

Vercel should auto-detect these, but verify:

- **Framework Preset**: Vite
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm install`

### Step 4: Add Environment Variables

Before deploying, add your backend URL:

1. In project settings, go to **"Environment Variables"**
2. Add:
   - **Key**: `VITE_API_BASE_URL`
   - **Value**: `https://your-backend.onrender.com` (from Step 4 above)
   - **Environment**: All (Production, Preview, Development)
3. Click **"Save"**

### Step 5: Deploy

1. Click **"Deploy"**
2. Wait for build (2-3 minutes)
3. Vercel will provide your live URL: `https://your-project.vercel.app`

### Step 6: Verify Frontend

1. Visit your Vercel URL
2. Test the application:
   - Search for players
   - View statistics
   - Check browser console for API errors

---

## Environment Variables Reference

### Backend (Render)
```env
DB_NAME=odi_cricket
DB_USER=odi_user
DB_PASSWORD=<from-render-database>
DB_HOST=<from-render-database>
DB_PORT=5432
FLASK_ENV=production
PYTHON_VERSION=3.11.0
```

### Frontend (Vercel)
```env
VITE_API_BASE_URL=https://your-backend.onrender.com
```

---

## Post-Deployment Configuration

### Update CORS (Optional - For Better Security)

Edit `backend/app.py` to restrict CORS to your Vercel domain:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://your-project.vercel.app"]
    }
})
```

Then redeploy backend on Render.

### Custom Domain (Optional)

#### For Frontend (Vercel):
1. Go to Project Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions

#### For Backend (Render):
1. Go to Service → Settings → Custom Domain
2. Add your custom domain
3. Update `VITE_API_BASE_URL` in Vercel to use custom domain

---

## Troubleshooting

### Frontend shows API errors
- Check browser console for error details
- Verify `VITE_API_BASE_URL` is set correctly in Vercel
- Test backend URL directly: `https://your-backend.onrender.com/api/health`
- Check CORS settings in backend

### Backend returns 500 errors
- Check Render logs: Dashboard → Service → Logs
- Verify database connection settings
- Ensure all environment variables are set
- Check database is running and accessible

### Database connection fails
- Verify environment variables match database credentials
- Check database status in Render dashboard
- Ensure database is not paused (free tier limitation)

### Build fails on Vercel
- Check build logs in Vercel dashboard
- Verify `package.json` has correct dependencies
- Ensure Node.js version is compatible (18+)
- Check for syntax errors in frontend code

### Backend slow or timing out
- **Normal on free tier**: First request after inactivity takes 30-60 seconds
- Backend spins down after 15 minutes of no requests
- Consider upgrading to paid tier ($7/month) for always-on service

---

## Performance Optimization

### Free Tier Limitations

**Render Backend**:
- ✅ Free SSL
- ✅ Automatic deploys from Git
- ⚠️ Spins down after 15 minutes inactivity
- ⚠️ 30-60 second cold start time
- ⚠️ 750 free hours/month

**Render Database**:
- ✅ 1GB storage
- ⚠️ Expires after 90 days (backup regularly!)
- ⚠️ Limited connections

**Vercel Frontend**:
- ✅ Global CDN
- ✅ Instant cache invalidation
- ✅ Unlimited bandwidth
- ✅ Always available (no spin-down)

### Upgrade Recommendations

For production use:
- **Render Backend**: Starter ($7/month) - No spin-down, better performance
- **Render Database**: Standard ($7/month) - Persistent, better performance
- **Vercel**: Free tier is excellent, upgrade only if you need advanced features

---

## Monitoring & Maintenance

### Backend Logs
- Render Dashboard → Your Service → Logs
- Real-time log streaming
- Filter by log level

### Frontend Logs
- Vercel Dashboard → Your Project → Deployments → View Function Logs
- Analytics available on paid plans

### Database Backups
```bash
# Manual backup
pg_dump <EXTERNAL_DATABASE_URL> > backup_$(date +%Y%m%d).sql

# Restore from backup
psql <EXTERNAL_DATABASE_URL> < backup_YYYYMMDD.sql
```

**Important**: Free database expires after 90 days. Set a reminder to backup or upgrade!

---

## Updating Your Deployment

### Update Frontend
```bash
# Make changes to frontend code
git add .
git commit -m "Update frontend"
git push origin main
```
Vercel auto-deploys on every push to main branch.

### Update Backend
```bash
# Make changes to backend code
git add .
git commit -m "Update backend"
git push origin main
```
Render auto-deploys on every push to main branch.

### Disable Auto-Deploy (Optional)
- **Vercel**: Project Settings → Git → Disable auto-deploy
- **Render**: Service Settings → Build & Deploy → Disable auto-deploy

---

## Cost Breakdown

### Free Tier (Recommended for Development/Demo)
- **Vercel**: $0/month
- **Render Backend**: $0/month (with limitations)
- **Render Database**: $0/month (90-day expiry)
- **Total**: $0/month

### Production Tier (Recommended for Production)
- **Vercel**: $0/month (or $20/month for team features)
- **Render Backend Starter**: $7/month
- **Render Database Standard**: $7/month
- **Total**: $14-34/month

---

## Support & Resources

- **Vercel Docs**: https://vercel.com/docs
- **Render Docs**: https://render.com/docs
- **Vercel Community**: https://github.com/vercel/vercel/discussions
- **Render Community**: https://community.render.com

---

## Quick Reference Commands

```bash
# Check git status
git status

# Deploy changes
git add .
git commit -m "Your message"
git push origin main

# View Vercel deployments
npx vercel --list

# Test backend locally
cd backend && source venv/bin/activate && python app.py

# Test frontend locally
cd frontend && npm run dev

# Database backup
pg_dump <DATABASE_URL> > backup.sql

# Database restore
psql <DATABASE_URL> < backup.sql
```

---

## Next Steps After Deployment

1. ✅ Test all features thoroughly
2. ✅ Set up custom domains (optional)
3. ✅ Configure monitoring/alerts (optional)
4. ✅ Set calendar reminder for database backup
5. ✅ Share your deployed URL!

Your application is now live! 🎉
