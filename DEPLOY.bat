@echo off
REM Complete Deployment Script for Action Guardrail (Windows)
REM This script guides deployment to Render and Vercel

echo ==================================================
echo Action Guardrail - Complete Deployment Guide
echo ==================================================

echo.
echo STEP 1: Deploy Backend to Render
echo ==================================================
echo.
echo 1. Go to: https://dashboard.render.com
echo 2. Click "New +" then "Web Service"
echo 3. Select "Build and deploy from a Git repository"
echo 4. Click "Connect Account" and authorize GitHub
echo 5. Select repository: Action-guardrail
echo.
echo Configuration:
echo   - Name: action-guardrail-backend
echo   - Environment: Python 3
echo   - Build Command: pip install -r requirements.txt
echo   - Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
echo   - Plan: Free tier (or paid for better performance)
echo.
echo Environment Variables:
echo   Key: CORS_ORIGINS
echo   Value: https://your-vercel-domain.vercel.app
echo.
echo 6. Click "Create Web Service"
echo 7. Wait for deployment (~2 minutes)
echo 8. Copy your backend URL (https://action-guardrail-backend.onrender.com)
echo.
pause

echo.
echo STEP 2: Deploy Frontend to Vercel
echo ==================================================
echo.
echo 1. Go to: https://vercel.com/new
echo 2. Click "Select" next to "Continue with GitHub"
echo 3. Authorize GitHub if needed
echo 4. Find and select "Action-guardrail" repository
echo.
echo Configure project:
echo   - Framework Preset: Vite
echo   - Root Directory: frontend
echo   - Build Command: npm run build
echo   - Output Directory: dist
echo.
echo Environment Variables:
echo   Key: VITE_API_BASE_URL
echo   Value: [PASTE YOUR RENDER BACKEND URL]
echo.
echo 5. Click "Deploy"
echo 6. Wait for deployment (~3 minutes)
echo 7. Copy your frontend URL (https://your-project.vercel.app)
echo.
pause

echo.
echo STEP 3: Update Backend CORS
echo ==================================================
echo.
echo 1. Go to: https://dashboard.render.com
echo 2. Click on "action-guardrail-backend" service
echo 3. Go to "Environment" tab
echo 4. Update CORS_ORIGINS to:
echo    https://[YOUR-VERCEL-DOMAIN].vercel.app
echo.
echo 5. Click "Save"
echo.
pause

echo.
echo SUCCESS! Deployment Complete
echo ==================================================
echo.
echo Your services are now live:
echo   Backend: https://action-guardrail-backend.onrender.com
echo   Frontend: https://your-domain.vercel.app
echo.
echo Test the connection:
echo   1. Open your frontend URL
echo   2. Check if health status is "healthy"
echo   3. If not, verify CORS_ORIGINS is set correctly
echo.
pause
