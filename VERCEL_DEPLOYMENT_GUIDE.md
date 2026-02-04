# Vercel Deployment Guide

## Prerequisites
1. Vercel account (https://vercel.com)
2. Git repository (GitHub, GitLab, or Bitbucket)
3. PostgreSQL database (Railway, Supabase, or similar)

## Step 1: Prepare Your Backend for Vercel

The backend has been configured with:
- **ASGI Handler**: `api/index.py` using Mangum for serverless execution
- **Runtime**: Python 3.11
- **Entry Point**: FastAPI app from `app.src.main`

## Step 2: Set Up Environment Variables on Vercel

Add these environment variables in your Vercel project settings:

```
DATABASE_URL=postgresql://user:password@host:5432/dbname
JWT_SECRET_KEY=your-super-secret-key-change-this
BACKEND_CORS_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000
DEBUG=False
DEVELOPMENT_MODE=False
```

### Getting a PostgreSQL Database:

**Option 1: Railway (Recommended)**
1. Go to https://railway.app
2. Create a new project
3. Add PostgreSQL plugin
4. Copy the DATABASE_URL from the plugin settings
5. Add to Vercel environment variables

**Option 2: Supabase**
1. Go to https://supabase.com
2. Create a new project
3. Go to Settings > Database > Connection Pooling
4. Copy the connection string (use port 6543 for pooling)
5. Add to Vercel environment variables

**Option 3: Neon**
1. Go to https://neon.tech
2. Create a new project
3. Copy the connection string
4. Add to Vercel environment variables

## Step 3: Deploy to Vercel

### Method 1: Using Vercel CLI (Recommended)
```bash
npm i -g vercel
cd backend
vercel
# Follow the prompts
```

### Method 2: Using GitHub Integration
1. Push your code to GitHub
2. Go to https://vercel.com/new
3. Import your repository
4. Select the `backend` folder as the root directory
5. Add environment variables
6. Click "Deploy"

## Step 4: Verify Deployment

After deployment, visit:
```
https://your-app.vercel.app/
```

You should see:
```json
{"message": "Welcome to Todo Fullstack App API"}
```

## Troubleshooting

### Cold Start Issues
- Vercel Python functions have ~5 second cold start time
- This is normal for serverless functions

### Database Connection Errors
- Verify DATABASE_URL is correctly set in Vercel environment
- Ensure your database allows connections from Vercel IPs (often requires allowlist)
- Check database is accessible from the internet

### CORS Errors
- Add your frontend URL to BACKEND_CORS_ORIGINS
- Include both http and https versions if needed

### Import Errors
- Ensure all required dependencies are in requirements.txt
- Vercel will automatically install from requirements.txt

## Next Steps

1. Deploy your frontend to Vercel
2. Update BACKEND_CORS_ORIGINS to include your frontend URL
3. Update your frontend API endpoints to point to your Vercel backend URL
4. Test all API endpoints

## Resources
- Vercel FastAPI Guide: https://vercel.com/docs/functions/serverless-functions/python
- Mangum Documentation: https://mangum.io/
- Railway: https://railway.app
- Supabase: https://supabase.com
