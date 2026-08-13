# Environment Variables Guide

## Local Development
Copy `.env.example` to `.env.local`:
```
VITE_API_BASE_URL=http://localhost:8000
```

## Production (Vercel)
Set in Vercel Dashboard → Environment Variables:
```
VITE_API_BASE_URL=https://your-render-backend-url.onrender.com
```

## Backend CORS (Render)
Set in Render Dashboard → Environment Variables:
```
CORS_ORIGINS=http://localhost:5173,https://your-vercel-domain.vercel.app
```
