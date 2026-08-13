# Deployment Guide

## Backend Deployment on Render

### Prerequisites
- GitHub account
- Render account (https://render.com)

### Steps

1. **Push to GitHub** (already done ✓)
   - Your code is already in: `https://github.com/Karthikeyan-strange/Action-guardrail`

2. **Connect Render to GitHub**
   - Go to https://dashboard.render.com
   - Click "New +" → "Web Service"
   - Select "Build and deploy from a Git repository"
   - Connect your GitHub account and select the `Action-guardrail` repository

3. **Configure the Web Service**
   - **Name**: `action-guardrail-backend`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free (or paid if you want better performance)

4. **Environment Variables** (in Render dashboard)
   - Add the CORS_ORIGINS for your Vercel frontend:
   ```
   CORS_ORIGINS=https://your-vercel-domain.vercel.app,http://localhost:5173
   ```
   - Replace `your-vercel-domain` with your actual Vercel domain

5. **Deploy**
   - Click "Create Web Service"
   - Render will automatically deploy when you push to GitHub
   - Your backend URL will be something like: `https://action-guardrail-backend.onrender.com`

---

## Frontend Deployment on Vercel

### Prerequisites
- Vercel account (https://vercel.com)
- GitHub account (already connected)

### Steps

1. **Connect Vercel to GitHub**
   - Go to https://vercel.com/new
   - Import the `Action-guardrail` repository
   - Select the `frontend` directory as the root

2. **Configure Build Settings**
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

3. **Environment Variables** (in Vercel dashboard)
   - Add your Render backend URL:
   ```
   VITE_API_BASE_URL=https://action-guardrail-backend.onrender.com
   ```
   - Replace with your actual Render backend URL

4. **Deploy**
   - Click "Deploy"
   - Vercel will automatically deploy from the `frontend` directory
   - Your frontend URL will be: `https://your-project-name.vercel.app`

5. **Update Backend CORS** (if needed)
   - Go to Render dashboard
   - Update `CORS_ORIGINS` to include your Vercel domain:
   ```
   CORS_ORIGINS=https://your-vercel-domain.vercel.app,http://localhost:5173
   ```

---

## Local Development

### Backend
```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload

# The API will be at: http://localhost:8000
```

### Frontend
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev

# The app will be at: http://localhost:5173
```

---

## File Structure for Deployment

```
action-guardrail/
├── render.yaml              # Render configuration
├── requirements.txt         # Python dependencies
├── app/                     # Backend FastAPI app
│   └── main.py
├── frontend/
│   ├── vercel.json          # Vercel configuration
│   ├── .env.local           # Local development
│   ├── package.json
│   └── src/
│       └── App.jsx          # Uses VITE_API_BASE_URL
```

---

## Troubleshooting

### CORS Errors
- Ensure `CORS_ORIGINS` in Render includes your Vercel domain
- Format: `https://your-domain.vercel.app`

### API Connection Issues
- Verify `VITE_API_BASE_URL` in Vercel matches your Render backend URL
- Check that the backend is running on Render (check logs)

### Build Failures on Vercel
- Clear Vercel cache: Settings → Git → Disconnect and reconnect
- Ensure `package.json` has all required dependencies

### Build Failures on Render
- Check that `requirements.txt` includes all Python dependencies
- Verify the start command includes the correct port: `$PORT`
