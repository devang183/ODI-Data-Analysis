# Deployment Guide for Render.com

This guide will help you deploy the ODI Cricket Analytics application to Render.com.

## Prerequisites

1. A Render.com account (sign up at https://render.com)
2. Git repository pushed to GitHub/GitLab/Bitbucket
3. PostgreSQL database with your cricket data already loaded

## Deployment Steps

### 1. Push Your Code to Git

```bash
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

### 2. Create PostgreSQL Database on Render

1. Go to Render Dashboard: https://dashboard.render.com
2. Click "New +" → "PostgreSQL"
3. Configure:
   - **Name**: `odi-cricket-db`
   - **Database**: `odi_cricket`
   - **User**: `odi_user`
   - **Region**: Choose closest to your users
   - **Plan**: Free (or paid for better performance)
4. Click "Create Database"
5. Wait for the database to be provisioned
6. **Important**: Save the connection details (you'll need them)

### 3. Upload Your Data to the Database

After the database is created, you need to upload your cricket data:

#### Option A: Using psql (Recommended if you have a dump file)

```bash
# Get the External Database URL from Render dashboard
# It looks like: postgres://user:password@host:port/database

# If you have a PostgreSQL dump:
pg_restore -d <EXTERNAL_DATABASE_URL> your_dump_file.sql

# Or use psql:
psql <EXTERNAL_DATABASE_URL> < your_dump_file.sql
```

#### Option B: Using the upload script

1. Connect to your Render database by updating `backend/.env`:
```env
DB_HOST=<render-db-host>
DB_NAME=odi_cricket
DB_USER=odi_user
DB_PASSWORD=<render-db-password>
DB_PORT=5432
```

2. Run the upload script:
```bash
python upload_jsons.py
```

### 4. Deploy Using render.yaml (Automatic)

1. Go to Render Dashboard
2. Click "New +" → "Blueprint"
3. Connect your Git repository
4. Render will detect the `render.yaml` file automatically
5. Click "Apply"
6. Render will create:
   - PostgreSQL database
   - Backend web service
   - Frontend static site

### 5. Manual Deployment (Alternative)

If automatic deployment doesn't work, deploy manually:

#### Deploy Backend:

1. Click "New +" → "Web Service"
2. Connect your Git repository
3. Configure:
   - **Name**: `odi-cricket-backend`
   - **Root Directory**: Leave empty
   - **Environment**: Python 3
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && gunicorn app:app`
   - **Plan**: Free
4. Add Environment Variables:
   - `DB_NAME`: `odi_cricket`
   - `DB_USER`: `odi_user`
   - `DB_PASSWORD`: (from database)
   - `DB_HOST`: (from database)
   - `DB_PORT`: `5432`
   - `FLASK_ENV`: `production`
5. Click "Create Web Service"

#### Deploy Frontend:

1. Click "New +" → "Static Site"
2. Connect your Git repository
3. Configure:
   - **Name**: `odi-cricket-frontend`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
4. Add Environment Variable:
   - `VITE_API_BASE_URL`: (URL of your backend service, e.g., `https://odi-cricket-backend.onrender.com`)
5. Click "Create Static Site"

### 6. Verify Deployment

1. **Backend Health Check**:
   - Visit: `https://your-backend-url.onrender.com/api/health`
   - Should return: `{"status": "healthy", "service": "odi-analytics-api"}`

2. **Frontend**:
   - Visit: `https://your-frontend-url.onrender.com`
   - Should load the application

3. **Test API Connection**:
   - Try searching for players in the frontend
   - Check browser console for any API errors

## Important Notes

### Free Tier Limitations

- **Backend**: Spins down after 15 minutes of inactivity. First request after spin-down will be slow (30-60 seconds).
- **Database**: 90-day expiration on free tier. Export your data regularly!
- **Frontend**: Always active, no spin-down.

### Database Persistence

The free PostgreSQL database expires after 90 days. To keep your data:
1. Upgrade to a paid plan, OR
2. Regularly export your database:
```bash
pg_dump <EXTERNAL_DATABASE_URL> > backup.sql
```

### Environment Variables

Make sure these are set correctly in your backend service:
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
- `FLASK_ENV=production`

### CORS Configuration

The backend is configured to accept requests from any origin. In production, you may want to restrict this to your frontend domain only.

Edit `backend/app.py`:
```python
CORS(app, resources={r"/api/*": {"origins": "https://your-frontend-url.onrender.com"}})
```

## Troubleshooting

### Backend won't start
- Check logs in Render dashboard
- Verify all environment variables are set
- Ensure database connection details are correct

### Frontend shows API errors
- Check that `VITE_API_BASE_URL` points to correct backend URL
- Verify backend is running (visit `/api/health`)
- Check browser console for CORS errors

### Database connection fails
- Verify database is running in Render dashboard
- Check environment variables match database credentials
- Ensure IP allowlist includes Render services (should be automatic)

### Slow initial load
- This is normal on free tier after inactivity
- Backend spins down after 15 minutes
- First request wakes it up (30-60 seconds)
- Consider upgrading to paid plan for always-on service

## Monitoring

- **Backend Logs**: Render Dashboard → Your Backend Service → Logs
- **Frontend Logs**: Render Dashboard → Your Frontend Site → Logs
- **Database Metrics**: Render Dashboard → Your Database → Metrics

## Updating Your Deployment

To deploy updates:

```bash
git add .
git commit -m "Your update message"
git push origin main
```

Render will automatically rebuild and redeploy your services.

## Cost Optimization

Free tier is great for development/demo, but for production:
- **Starter Plan ($7/month)**: Better performance, no spin-down
- **Standard Plan ($25/month)**: Production-ready, better resources
- **Database**: Standard plan ($7/month) for persistent database

## Support

- Render Documentation: https://render.com/docs
- Render Community: https://community.render.com
- Project Issues: Check your repository's issues page
