# Vercel Deployment Guide

## 🚀 Quick Deployment Steps

### Prerequisites
1. GitHub account
2. Vercel account (free tier works)
3. API keys for:
   - Stability AI API (for image generation)
   - OpenAI API (for voice transcription)

---

## Step 1: Push Backend to GitHub

### 1.1 Initialize Git Repository (if not already done)
```bash
cd Hackthon
git init
```

### 1.2 Add Remote Repository
```bash
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/coloring-page-backend.git
```

### 1.3 Commit and Push
```bash
git add .
git commit -m "Initial backend commit for Vercel deployment"
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy to Vercel

### Option A: Deploy via Vercel Dashboard (Recommended)

1. **Go to [vercel.com](https://vercel.com)** and sign in

2. **Click "Add New Project"**

3. **Import your GitHub repository**
   - Select the repository you just pushed
   - Click "Import"

4. **Configure Project**
   - Framework Preset: **Other**
   - Root Directory: Leave as `./`
   - Build Command: Leave empty
   - Output Directory: Leave empty
   - Install Command: `pip install -r requirements.txt`

5. **Add Environment Variables** (click "Environment Variables")
   ```
   STABILITY_API_KEY=your_stability_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   SECRET_KEY=your_secret_key_here
   FLASK_ENV=production
   ```

6. **Click "Deploy"**
   - Wait for deployment to complete (usually 1-3 minutes)

7. **Your API is now live!** 🎉
   - Copy the deployment URL (e.g., `https://your-project.vercel.app`)

### Option B: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
cd Hackthon
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? coloring-page-backend
# - Directory? ./
# - Override settings? No

# Add environment variables
vercel env add STABILITY_API_KEY
vercel env add OPENAI_API_KEY
vercel env add SECRET_KEY

# Deploy to production
vercel --prod
```

---

## Step 3: Test Your Deployment

### 3.1 Test Health Endpoint
```bash
curl https://your-project.vercel.app/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Kids Coloring Page Generator API",
  "timestamp": "2025-10-19T12:00:00",
  "environment": "production"
}
```

### 3.2 Test Image Generation
```bash
curl -X POST https://your-project.vercel.app/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A cute cat playing with a ball"}'
```

---

## Step 4: Share API Endpoint with Frontend Team

### API Base URL
```
https://your-project.vercel.app
```

### Available Endpoints

#### 1. Health Check
```
GET /api/health
```

#### 2. Generate Coloring Page
```
POST /api/generate
Content-Type: application/json

{
  "prompt": "A dolphin playing basketball underwater"
}
```

**Response:**
```json
{
  "success": true,
  "image_data": "data:image/png;base64,iVBORw0KG...",
  "prompt": "A dolphin playing basketball underwater",
  "timestamp": "20251019_120000"
}
```

#### 3. Voice to Text
```
POST /api/voice-to-text
Content-Type: multipart/form-data

{
  "audio": <audio file>
}
```

**Response:**
```json
{
  "success": true,
  "text": "A dolphin playing basketball underwater"
}
```

---

## Frontend Integration Example

### Using Fetch API

```javascript
// 1. Generate Coloring Page
async function generateColoringPage(prompt) {
  const response = await fetch('https://your-project.vercel.app/api/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ prompt })
  });
  
  const data = await response.json();
  return data.image_data; // Base64 encoded image
}

// 2. Voice to Text
async function voiceToText(audioFile) {
  const formData = new FormData();
  formData.append('audio', audioFile);
  
  const response = await fetch('https://your-project.vercel.app/api/voice-to-text', {
    method: 'POST',
    body: formData
  });
  
  const data = await response.json();
  return data.text;
}
```

### Using Axios

```javascript
import axios from 'axios';

const API_BASE_URL = 'https://your-project.vercel.app';

// 1. Generate Coloring Page
async function generateColoringPage(prompt) {
  const response = await axios.post(`${API_BASE_URL}/api/generate`, {
    prompt: prompt
  });
  return response.data.image_data;
}

// 2. Voice to Text
async function voiceToText(audioFile) {
  const formData = new FormData();
  formData.append('audio', audioFile);
  
  const response = await axios.post(`${API_BASE_URL}/api/voice-to-text`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
  return response.data.text;
}
```

---

## Troubleshooting

### Common Issues

#### 1. Deployment Failed
- **Check build logs** in Vercel dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify Python version compatibility

#### 2. API Returns 500 Error
- **Check environment variables** are set correctly
- **View function logs** in Vercel dashboard
- Verify API keys are valid

#### 3. CORS Errors
- API already has CORS enabled for all origins
- If issues persist, check Vercel function logs

#### 4. Timeout Errors
- Vercel has a 10-second timeout for serverless functions
- Image generation might take time with Stability AI
- Consider upgrading to Vercel Pro for 60-second timeout

---

## Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| `STABILITY_API_KEY` | Stability AI API key for image generation | Yes |
| `OPENAI_API_KEY` | OpenAI API key for voice transcription | Yes |
| `SECRET_KEY` | Flask secret key for session management | Yes |
| `FLASK_ENV` | Set to `production` | Yes |

---

## Monitoring & Logs

### View Logs
1. Go to Vercel dashboard
2. Select your project
3. Click on "Functions" tab
4. Click on any function to see logs

### Monitor Usage
1. Go to Vercel dashboard
2. Select your project
3. Click on "Analytics" tab

---

## Updating Your Deployment

### Automatic Deployment
Any push to the `main` branch will automatically trigger a new deployment.

```bash
git add .
git commit -m "Update API"
git push origin main
```

### Manual Deployment
```bash
vercel --prod
```

---

## Production Considerations

### 1. Rate Limiting
Consider implementing rate limiting to prevent abuse:
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=get_remote_address)

@app.route('/api/generate', methods=['POST'])
@limiter.limit("10 per minute")
def generate_coloring_page():
    # ...
```

### 2. Error Tracking
Consider integrating Sentry for error tracking:
```bash
pip install sentry-sdk[flask]
```

### 3. Caching
Consider implementing caching for frequently requested prompts

### 4. Database
For production, consider using a database to store:
- Generated images (with cloud storage like S3, Cloudinary)
- User requests
- Analytics

---

## API Documentation URL

Share this with your frontend team:
```
https://your-project.vercel.app/
```

The root endpoint provides API documentation and available endpoints.

---

## Support

For issues or questions:
1. Check Vercel documentation: https://vercel.com/docs
2. Review function logs in Vercel dashboard
3. Check API status: `https://your-project.vercel.app/api/health`

---

## Security Notes

1. **Never commit API keys** to GitHub
2. **Use environment variables** for all sensitive data
3. **Keep dependencies updated** for security patches
4. **Monitor API usage** to prevent abuse
5. **Consider implementing authentication** for production use

---

## Next Steps

1. ✅ Deploy to Vercel
2. ✅ Test all endpoints
3. ✅ Share API URL with frontend team
4. 📝 Document any custom endpoints
5. 🔒 Implement authentication (if needed)
6. 📊 Set up monitoring and analytics
7. 🚀 Optimize performance based on usage

---

**Your API is ready! Share the deployment URL with your frontend team to start building amazing features!** 🎉

