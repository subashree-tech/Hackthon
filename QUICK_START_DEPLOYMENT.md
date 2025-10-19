# 🚀 Quick Start: Deploy Backend in 5 Minutes

## Prerequisites
- GitHub account
- Vercel account (sign up at [vercel.com](https://vercel.com) - it's free!)
- Your API keys ready:
  - Stability AI API key ([get here](https://platform.stability.ai/))
  - OpenAI API key ([get here](https://platform.openai.com/api-keys))

---

## Step 1: Push to GitHub (2 minutes)

```bash
# Navigate to project directory
cd Hackthon

# Initialize and push to GitHub
git init
git add .
git commit -m "Backend ready for deployment"

# Replace YOUR_USERNAME and REPO_NAME
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

**Create GitHub repository first:**
1. Go to github.com
2. Click "+" → "New repository"
3. Name it (e.g., `coloring-page-backend`)
4. Create (don't initialize with anything)

---

## Step 2: Deploy to Vercel (3 minutes)

### 2.1 Import Project
1. Go to [vercel.com](https://vercel.com)
2. Click **"Add New Project"**
3. Click **"Import Git Repository"**
4. Select your GitHub repository
5. Click **"Import"**

### 2.2 Configure Project
- **Framework Preset**: Other
- **Root Directory**: `./`
- **Build Command**: (leave empty)
- **Output Directory**: (leave empty)
- **Install Command**: `pip install -r requirements.txt`

### 2.3 Add Environment Variables
Click **"Environment Variables"** and add:

```
STABILITY_API_KEY = sk-your-stability-api-key
OPENAI_API_KEY = sk-your-openai-api-key
SECRET_KEY = your-random-secret-key-here
FLASK_ENV = production
```

### 2.4 Deploy!
Click **"Deploy"**

Wait 1-2 minutes... ☕

---

## Step 3: Get Your API Endpoint

After deployment succeeds:

1. Copy your deployment URL (e.g., `https://your-project.vercel.app`)
2. Test it:
   ```bash
   curl https://your-project.vercel.app/api/health
   ```

**You should see:**
```json
{
  "status": "healthy",
  "service": "Kids Coloring Page Generator API"
}
```

---

## 🎉 Success! Share with Frontend Team

### API Endpoint
```
https://your-project.vercel.app
```

### Available Endpoints

1. **Health Check**
   ```
   GET /api/health
   ```

2. **Generate Coloring Page**
   ```
   POST /api/generate
   Body: {"prompt": "A cute cat"}
   ```

3. **Voice to Text**
   ```
   POST /api/voice-to-text
   Body: FormData with audio file
   ```

---

## 📋 Quick Test

Test your API:

```bash
# Health check
curl https://your-project.vercel.app/api/health

# Generate image
curl -X POST https://your-project.vercel.app/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A cute dolphin"}'
```

---

## 🔄 Future Updates

Any push to GitHub `main` branch will automatically deploy to Vercel!

```bash
git add .
git commit -m "Update API"
git push origin main
```

---

## 📚 More Information

- **Full Deployment Guide**: See `VERCEL_DEPLOYMENT.md`
- **API Documentation**: See `README_API.md`
- **GitHub Setup**: See `GITHUB_SETUP.md`

---

## 🆘 Common Issues

**Problem**: Deployment fails
- **Solution**: Check Vercel build logs, ensure all dependencies in `requirements.txt`

**Problem**: API returns 500 error
- **Solution**: Check environment variables are set correctly in Vercel

**Problem**: Can't access API
- **Solution**: Check Vercel deployment status, view function logs

---

**Your backend is live! 🎊 Share the API endpoint with your frontend team!**

