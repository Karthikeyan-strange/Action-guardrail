# 🚀 Quick Deploy Checklist

## ✅ Pre-Deployment (Already Done)
- [x] Code pushed to GitHub: https://github.com/Karthikeyan-strange/Action-guardrail
- [x] `render.yaml` configured for Render backend
- [x] `vercel.json` configured for Vercel frontend  
- [x] `App.jsx` updated to use environment variables
- [x] Backend CORS updated for dynamic origins
- [x] `.gitignore` created to exclude cache files
- [x] Environment files created

---

## 📋 BACKEND DEPLOYMENT (Render) - 5 minutes

### Step 1: Log in to Render
```
1. Go to https://dashboard.render.com/login
2. Click "GitHub" to authenticate
3. Authorize the connection
```

### Step 2: Create Web Service
```
1. Click "New +" button
2. Select "Web Service"
3. Click "Connect Account" → GitHub
4. Search for and select: "Action-guardrail"
5. Click "Connect"
```

### Step 3: Configure Service
| Setting | Value |
|---------|-------|
| **Name** | `action-guardrail-backend` |
| **Environment** | Python 3 |
| **Region** | (default) |
| **Branch** | main |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| **Plan** | Free |

### Step 4: Add Environment Variables
Click "Advanced" then add:
```
CORS_ORIGINS = http://localhost:5173,https://YOUR_VERCEL_DOMAIN.vercel.app
PYTHON_VERSION = 3.10
```

### Step 5: Deploy
```
Click "Create Web Service"
Wait 2-3 minutes for deployment
✓ Your backend URL: https://action-guardrail-backend.onrender.com
```

---

## 📋 FRONTEND DEPLOYMENT (Vercel) - 5 minutes

### Step 1: Log in to Vercel
```
1. Go to https://vercel.com/new
2. Click "Continue with GitHub"
3. Authorize if needed
```

### Step 2: Import Project
```
1. Search for: "Action-guardrail"
2. Click "Import"
3. Choose your personal account
4. Click "Import"
```

### Step 3: Configure Project
```
Framework Preset: Vite (should auto-detect)
Root Directory: frontend
Build Command: npm run build
Output Directory: dist
Install Command: npm install
```

### Step 4: Add Environment Variables
Click "Environment Variables" and add:
```
Name: VITE_API_BASE_URL
Value: https://YOUR-RENDER-BACKEND-URL.onrender.com
```

### Step 5: Deploy
```
Click "Deploy"
Wait 2-3 minutes for deployment
✓ Your frontend URL: https://[project-name].vercel.app
```

---

## 📋 CONNECT BACKEND & FRONTEND

### Step 1: Update Render CORS
```
1. Go to https://dashboard.render.com
2. Click "action-guardrail-backend" service
3. Go to "Environment" settings
4. Update CORS_ORIGINS to:
   https://YOUR_VERCEL_DOMAIN.vercel.app
5. Click "Save"
6. Wait for auto-redeployment (30 seconds)
```

### Step 2: Test Connection
```
1. Open your Vercel frontend URL
2. Check if it loads without errors
3. Verify health status shows "healthy"
4. You should see the dashboard with real-time data
```

---

## 🔗 Final URLs
After deployment, you'll have:

**Backend API**
```
https://action-guardrail-backend.onrender.com
```

**Frontend App**
```
https://[your-project-name].vercel.app
```

**GitHub Repository**
```
https://github.com/Karthikeyan-strange/Action-guardrail
```

---

## ❌ Troubleshooting

### CORS Errors
- **Problem**: Frontend can't connect to backend
- **Solution**: Make sure `CORS_ORIGINS` on Render includes your Vercel domain exactly

### Build Fails on Vercel
- Clear cache: Dashboard → Settings → Git → Disconnect and reconnect
- Check `frontend/` has `package.json`

### Build Fails on Render
- Check `requirements.txt` exists in root
- Verify Python version is 3.10 or higher

### 404 Error on Render
- Ensure `Start Command` is: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

---

## 📞 Support Resources
- [Render Docs](https://render.com/docs)
- [Vercel Docs](https://vercel.com/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Vite Docs](https://vitejs.dev/)
