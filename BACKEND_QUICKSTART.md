# Quick Start: Backend Fix & Vercel Deployment

## 🔧 What Was Fixed

Your backend wasn't running due to missing Vercel configuration. Here's what I fixed:

1. **Created Vercel Handler** (`api/index.py`)
   - Uses Mangum ASGI adapter for serverless execution
   - Properly imports your FastAPI app

2. **Updated Configuration**
   - `vercel.json` - Now uses Python 3.11 with proper settings
   - `requirements.txt` - Added `mangum==0.17.0` dependency
   - `main.py` - Added database initialization on startup

3. **Added Documentation**
   - `BACKEND_DEPLOYMENT_CHECKLIST.md` - Step-by-step deployment guide
   - `VERCEL_DEPLOYMENT_GUIDE.md` - Detailed reference guide

## 🚀 Deploy in 3 Steps

### Step 1: Set Up Database (Choose One)
**Railway (Recommended - Easiest)**
```bash
# Go to https://railway.app
# Create new project → Add PostgreSQL
# Copy DATABASE_URL from the postgres widget
```

### Step 2: Deploy Backend
```bash
cd backend
npm install -g vercel  # Install Vercel CLI if not already done
vercel
# Follow prompts, add your DATABASE_URL as environment variable
```

### Step 3: Update Frontend
Update your frontend's API URL to your Vercel backend URL, then deploy:
```bash
cd ../frontend
vercel
```

## 🔐 Required Environment Variables

Add these to your Vercel project settings:

```
DATABASE_URL=postgresql://...your-database-url...
JWT_SECRET_KEY=your-secret-key-generate-one-with-openssl-rand-hex-32
BACKEND_CORS_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000
```

## ✅ Verify Deployment

After deployment, test this URL:
```
https://your-backend.vercel.app/
```

You should see:
```json
{"message": "Welcome to Todo Fullstack App API"}
```

## 📚 Detailed Guides

- **Full deployment walkthrough**: See `BACKEND_DEPLOYMENT_CHECKLIST.md`
- **Troubleshooting & options**: See `VERCEL_DEPLOYMENT_GUIDE.md`

## 🆘 Common Issues

| Issue | Fix |
|-------|-----|
| 502 Bad Gateway | Check DATABASE_URL is set and accessible |
| CORS errors | Add frontend URL to BACKEND_CORS_ORIGINS |
| Module import errors | Ensure all dependencies in requirements.txt |
| Slow first response | Normal for serverless (3-5s cold start) |

## 💡 Pro Tips

- Use Railway.app for the easiest PostgreSQL setup
- Set JWT_SECRET_KEY to something strong: `openssl rand -hex 32`
- Test locally first: `pip install -r requirements.txt && uvicorn app.src.main:app --reload`
- Monitor Vercel logs in dashboard for debugging

---

**Ready to deploy?** Start with `BACKEND_DEPLOYMENT_CHECKLIST.md`
