# 🧪 Local Testing Guide

Before deploying to production, test everything locally.

## Start Backend

```bash
# Install dependencies
pip install -r requirements.txt

# Run the FastAPI server
uvicorn app.main:app --reload

# Backend will be at: http://localhost:8000
# API docs at: http://localhost:8000/docs
```

## Start Frontend (New Terminal)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Frontend will be at: http://localhost:5173
```

## Test Connection

### Test 1: Backend Health
```bash
curl http://localhost:8000/health
```
Expected response:
```json
{"status": "healthy"}
```

### Test 2: Frontend Loads
1. Open http://localhost:5173 in browser
2. Check if the dashboard appears
3. Verify no CORS errors in browser console

### Test 3: API Endpoints
```bash
# Get audit logs
curl http://localhost:8000/audit

# Get policies
curl http://localhost:8000/policies

# Get approvals
curl http://localhost:8000/approvals
```

## Frontend Environment for Local Dev

Create `frontend/.env.local`:
```
VITE_API_BASE_URL=http://localhost:8000
```

If `.env.local` doesn't exist, the frontend will use default: `http://127.0.0.1:8000`

## Verify Configuration Files

Before deploying, check these files exist:

```
✓ render.yaml              (Backend config for Render)
✓ frontend/vercel.json     (Frontend config for Vercel)
✓ frontend/.env.example    (Environment template)
✓ Procfile                 (Alternative Render config)
✓ app/main.py             (Has CORS_ORIGINS from env)
✓ frontend/src/App.jsx    (Uses VITE_API_BASE_URL)
```

## Production Environment Checklist

- [ ] Backend URL copied from Render
- [ ] Frontend URL copied from Vercel
- [ ] VITE_API_BASE_URL set in Vercel to Render backend URL
- [ ] CORS_ORIGINS set in Render to Vercel frontend URL
- [ ] Both services deployed and redeployed (if needed)
- [ ] Tested connection between frontend and backend
- [ ] No console errors in browser DevTools

## Common Commands

```bash
# Backend: Run with custom port
uvicorn app.main:app --host 0.0.0.0 --port 8001

# Frontend: Build for production
npm run build

# Frontend: Preview production build
npm run preview

# Frontend: Lint
npm run lint
```

## Docker Testing (Optional)

To test the exact production environment:

```bash
# Build Docker image
docker build -t action-guardrail .

# Run container
docker run -p 8000:8000 action-guardrail
```

Requires `Dockerfile` in root directory.
