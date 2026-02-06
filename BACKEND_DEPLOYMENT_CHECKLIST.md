# Backend Deployment Checklist

## ✅ What's Been Fixed

- [x] Created Vercel-compatible ASGI handler at `api/index.py` using Mangum
- [x] Updated `vercel.json` with Python 3.11 runtime and proper configuration
- [x] Fixed `requirements.txt` with proper dependency versions including mangum 0.17.0
- [x] Added database fallback support (SQLite if PostgreSQL unavailable)
- [x] Added initialization of database tables on module import
- [x] Created `.gitignore` for backend directory
- [x] All Python packages properly configured

## 📋 Before Deploying to Vercel

### 1. Prepare Repository
```bash
cd backend
git add .
git commit -m "Fix backend for Vercel deployment"
git push
```

### 2. Create/Configure Database
Choose one option:

**Option A: Railway** (Easiest)
- [ ] Create account at https://railway.app
- [ ] Create PostgreSQL plugin
- [ ] Copy DATABASE_URL

**Option B: Supabase**
- [ ] Create account at https://supabase.com
- [ ] Create new project
- [ ] Use Connection Pooling URL

**Option C: Neon**
- [ ] Create account at https://neon.tech
- [ ] Create database
- [ ] Copy connection URL

### 3. Prepare Vercel Project
- [ ] Create Vercel account at https://vercel.com
- [ ] Install Vercel CLI: `npm i -g vercel`
- [ ] Authenticate: `vercel login`

## 🚀 Deployment Steps

### Step 1: Deploy Backend
```bash
cd backend
vercel
```

During the prompts:
- Set project name: `todo-app-backend` (or your choice)
- Select `backend` as root directory
- Skip "Modify vercel.json"? Choose No if you want to use our config
- Skip creating source code? Choose No

### Step 2: Add Environment Variables
```bash
vercel env add DATABASE_URL
# Paste your PostgreSQL connection URL

vercel env add JWT_SECRET_KEY
# Generate a secure random key or use: openssl rand -hex 32

vercel env add BACKEND_CORS_ORIGINS
# http://localhost:3000,https://your-frontend.vercel.app
```

### Step 3: Deploy Frontend
```bash
# Update your frontend API URL first to point to your backend
# In your React code, change API endpoint to: https://your-backend.vercel.app

cd ../frontend
vercel
```

### Step 4: Test Your Deployment
```bash
# Test backend root endpoint
curl https://your-backend.vercel.app/

# You should see:
# {"message": "Welcome to Todo Fullstack App API"}
```

## 🔧 Environment Variables Reference

| Variable | Value | Required |
|----------|-------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `JWT_SECRET_KEY` | Random 32+ character string | Yes |
| `BACKEND_CORS_ORIGINS` | Comma-separated origin URLs | Yes |
| `DEBUG` | `False` | No (default) |
| `DEVELOPMENT_MODE` | `False` | No (default) |
| `DATABASE_ECHO` | `False` | No (default) |

## 🐛 Troubleshooting

### Backend returns 502 Bad Gateway
- Check DATABASE_URL is set correctly in Vercel env vars
- Verify database is publicly accessible
- Check database credentials are correct

### CORS errors when calling from frontend
- Add frontend URL to BACKEND_CORS_ORIGINS
- Include protocol (http/https)
- Separate multiple URLs with commas

### Cold start takes too long
- Normal for serverless Python functions (3-5 seconds first call)
- Subsequent calls are much faster
- Consider upgrading to larger instance if needed

### Import/Module errors
- Verify all dependencies in requirements.txt
- Check that all `__init__.py` files exist
- Ensure vercel.json points to correct runtime

## 📊 Project Structure After Deploy

```
backend/
├── api/
│   ├── __init__.py
│   └── index.py          ← Vercel entry point
├── app/
│   └── src/
│       ├── main.py       ← FastAPI app
│       ├── config.py     ← Settings
│       ├── database/     ← DB code
│       ├── models/       ← SQLModel models
│       ├── schemas/      ← Pydantic schemas
│       ├── api/          ← API routers
│       └── ...
├── requirements.txt      ← Python dependencies
├── vercel.json          ← Vercel configuration
├── .env                 ← Local env (NOT pushed)
└── .env.example         ← Example env
```

## 🔗 Useful Links

- Vercel Python Functions: https://vercel.com/docs/functions/serverless-functions/python
- Mangum (ASGI handler): https://mangum.io/
- FastAPI Deployment: https://fastapi.tiangolo.com/deployment/
- Railway.app: https://railway.app
- Supabase: https://supabase.com

## ✨ Next Steps

After successful deployment:

1. Update frontend API endpoints to point to your Vercel backend
2. Test all features (auth, todos, chat)
3. Set up custom domain if desired
4. Monitor logs in Vercel dashboard
5. Set up automatic deployments from GitHub

---

**Created**: February 3, 2026
**Status**: Ready for Deployment
