# GitHub Setup & Deployment Guide

## 📋 Step-by-Step Guide to Push Backend to GitHub

### Step 1: Create a New Repository on GitHub

1. Go to [GitHub](https://github.com)
2. Click the **+** icon (top right) → **New repository**
3. Fill in the details:
   - **Repository name**: `coloring-page-backend` (or any name you prefer)
   - **Description**: Kids Coloring Page Generator - Backend API
   - **Visibility**: Public or Private (your choice)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
4. Click **Create repository**

### Step 2: Push Your Code to GitHub

Open PowerShell/Terminal in your project directory and run:

```bash
# Navigate to the Hackthon directory
cd Hackthon

# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit your changes
git commit -m "Initial backend commit - Ready for Vercel deployment"

# Add your GitHub repository as remote
# Replace YOUR_USERNAME and REPOSITORY_NAME with your actual values
git remote add origin https://github.com/YOUR_USERNAME/REPOSITORY_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Verify Your Code is on GitHub

1. Go to your repository URL: `https://github.com/YOUR_USERNAME/REPOSITORY_NAME`
2. You should see all your files including:
   - `api/` folder with `index.py`
   - `services/` folder
   - `vercel.json`
   - `requirements.txt`
   - `VERCEL_DEPLOYMENT.md`

---

## 🚀 After Pushing to GitHub

Your backend is now on GitHub! Next steps:

### Option 1: Quick Deployment (Recommended)
Follow the **VERCEL_DEPLOYMENT.md** guide for deploying to Vercel

### Option 2: Manual Verification
Before deploying, verify these files exist in your GitHub repo:

- ✅ `api/index.py` (Vercel entry point)
- ✅ `vercel.json` (Vercel configuration)
- ✅ `requirements.txt` (Python dependencies)
- ✅ `services/image_generator.py`
- ✅ `services/voice_processor.py`
- ✅ `.gitignore` (to exclude unnecessary files)

---

## 🔐 Important Security Notes

### DO NOT commit these files:
- ❌ `.env` (contains secret API keys)
- ❌ `__pycache__/` folders
- ❌ `static/uploads/` (user uploaded files)
- ❌ `static/outputs/` (generated files)

These are already in `.gitignore`, but double-check!

### Before pushing, ensure:
1. No API keys in code
2. No `.env` file is committed
3. All secrets are in environment variables

---

## 🛠️ Troubleshooting

### "fatal: not a git repository"
Run: `git init`

### "failed to push some refs"
Run: `git pull origin main --rebase` then `git push`

### "Authentication failed"
Use a Personal Access Token instead of password:
1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token with `repo` scope
3. Use token as password when pushing

### Files not showing on GitHub
Check `.gitignore` - some files might be ignored

---

## 📊 Repository Structure

After pushing, your GitHub repository should look like:

```
coloring-page-backend/
├── api/
│   └── index.py              # Vercel serverless function
├── services/
│   ├── __init__.py
│   ├── image_generator.py
│   └── voice_processor.py
├── .gitignore
├── config.py
├── requirements.txt
├── vercel.json               # Vercel configuration
├── VERCEL_DEPLOYMENT.md      # Deployment guide
├── README_API.md             # API documentation
├── GITHUB_SETUP.md           # This file
└── env.vercel.example        # Environment variables template
```

---

## 🔄 Future Updates

After making changes to your code:

```bash
# Add changes
git add .

# Commit with a descriptive message
git commit -m "Description of changes"

# Push to GitHub (will auto-deploy to Vercel)
git push origin main
```

Vercel will automatically deploy your changes when you push to GitHub!

---

## ✅ Checklist Before Deploying

- [ ] Code is pushed to GitHub
- [ ] No sensitive data (API keys) in code
- [ ] `vercel.json` exists
- [ ] `requirements.txt` has all dependencies
- [ ] `api/index.py` exists
- [ ] Repository is accessible (public or private with Vercel access)

---

## 🎯 Next Step

**You're ready to deploy!** 

Follow the **VERCEL_DEPLOYMENT.md** guide to deploy your backend to Vercel and get your API endpoint.

---

**Good luck with your deployment! 🚀**

