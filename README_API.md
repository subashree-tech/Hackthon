# Kids Coloring Page Generator - Backend API

This is the backend API for the Kids Coloring Page Generator application. It provides endpoints for generating coloring pages from text prompts and converting voice input to text.

## 🚀 Live API Endpoint

After deploying to Vercel, your API will be available at:
```
https://your-project-name.vercel.app
```

## 📋 API Documentation

### Base URL
```
https://your-project-name.vercel.app
```

### Endpoints

#### 1. Health Check
**GET** `/api/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "Kids Coloring Page Generator API",
  "timestamp": "2025-10-19T12:00:00",
  "environment": "production"
}
```

---

#### 2. Generate Coloring Page
**POST** `/api/generate`

Generate a coloring page from a text prompt.

**Request:**
```json
{
  "prompt": "A cute dolphin playing basketball underwater"
}
```

**Response:**
```json
{
  "success": true,
  "image_data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
  "prompt": "A cute dolphin playing basketball underwater",
  "timestamp": "20251019_120000"
}
```

**Example using cURL:**
```bash
curl -X POST https://your-project.vercel.app/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A cute cat playing with a ball"}'
```

**Example using JavaScript:**
```javascript
async function generateImage(prompt) {
  const response = await fetch('https://your-project.vercel.app/api/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ prompt })
  });
  
  const data = await response.json();
  
  if (data.success) {
    // Use the base64 image
    const img = document.createElement('img');
    img.src = data.image_data;
    document.body.appendChild(img);
  }
}
```

---

#### 3. Voice to Text
**POST** `/api/voice-to-text`

Convert audio file to text using OpenAI Whisper.

**Request:**
- Content-Type: `multipart/form-data`
- Field name: `audio`
- Supported formats: WAV, MP3, OGG, WEBM, M4A

**Response:**
```json
{
  "success": true,
  "text": "A cute dolphin playing basketball underwater"
}
```

**Example using cURL:**
```bash
curl -X POST https://your-project.vercel.app/api/voice-to-text \
  -F "audio=@recording.wav"
```

**Example using JavaScript:**
```javascript
async function transcribeAudio(audioFile) {
  const formData = new FormData();
  formData.append('audio', audioFile);
  
  const response = await fetch('https://your-project.vercel.app/api/voice-to-text', {
    method: 'POST',
    body: formData
  });
  
  const data = await response.json();
  
  if (data.success) {
    console.log('Transcribed text:', data.text);
    return data.text;
  }
}
```

---

## 🔧 Frontend Integration

### React Example

```javascript
import React, { useState } from 'react';

const API_BASE_URL = 'https://your-project.vercel.app';

function ColoringPageGenerator() {
  const [prompt, setPrompt] = useState('');
  const [imageData, setImageData] = useState(null);
  const [loading, setLoading] = useState(false);

  const generateImage = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt })
      });
      
      const data = await response.json();
      
      if (data.success) {
        setImageData(data.image_data);
      }
    } catch (error) {
      console.error('Error generating image:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input 
        type="text" 
        value={prompt} 
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Enter a prompt..."
      />
      <button onClick={generateImage} disabled={loading}>
        {loading ? 'Generating...' : 'Generate'}
      </button>
      
      {imageData && <img src={imageData} alt="Generated coloring page" />}
    </div>
  );
}
```

### Vue.js Example

```vue
<template>
  <div>
    <input 
      v-model="prompt" 
      type="text" 
      placeholder="Enter a prompt..."
    />
    <button @click="generateImage" :disabled="loading">
      {{ loading ? 'Generating...' : 'Generate' }}
    </button>
    
    <img v-if="imageData" :src="imageData" alt="Generated coloring page" />
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      prompt: '',
      imageData: null,
      loading: false,
      apiBaseUrl: 'https://your-project.vercel.app'
    };
  },
  methods: {
    async generateImage() {
      this.loading = true;
      try {
        const response = await axios.post(`${this.apiBaseUrl}/api/generate`, {
          prompt: this.prompt
        });
        
        if (response.data.success) {
          this.imageData = response.data.image_data;
        }
      } catch (error) {
        console.error('Error generating image:', error);
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>
```

---

## 📦 Response Format

All responses follow this format:

### Success Response
```json
{
  "success": true,
  "data": { ... }
}
```

### Error Response
```json
{
  "error": "Error message here"
}
```

---

## ⚠️ Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad Request (missing parameters) |
| 404 | Endpoint not found |
| 500 | Internal Server Error |

---

## 🔒 CORS

CORS is enabled for all origins. You can call this API from any frontend application.

---

## 📊 Rate Limits

Current rate limits (may vary based on Vercel plan):
- **Free tier**: 10 seconds max execution time per request
- **Pro tier**: 60 seconds max execution time per request

---

## 🛠️ Development & Testing

### Test the API

1. **Health Check:**
```bash
curl https://your-project.vercel.app/api/health
```

2. **Generate Image:**
```bash
curl -X POST https://your-project.vercel.app/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A cute cat"}'
```

3. **Voice to Text:**
```bash
curl -X POST https://your-project.vercel.app/api/voice-to-text \
  -F "audio=@test.wav"
```

---

## 📝 Notes for Frontend Team

1. **Image Format**: Images are returned as base64-encoded data URIs, ready to use in `<img>` tags
2. **Audio Upload**: Use `FormData` for audio file uploads
3. **Error Handling**: Always check the `success` field in responses
4. **CORS**: No special headers needed - CORS is pre-configured
5. **Timeout**: Image generation may take 5-10 seconds depending on API response time

---

## 🚀 Deployment Status

- **Platform**: Vercel
- **Region**: Auto-selected based on user location
- **CI/CD**: Auto-deploys on git push to main branch

---

## 📞 Support

For issues or questions about the API:
1. Check the `/api/health` endpoint
2. Review the error message in the response
3. Contact the backend team

---

## 🔗 Useful Links

- Vercel Dashboard: https://vercel.com/dashboard
- API Health: https://your-project.vercel.app/api/health
- Deployment Guide: See `VERCEL_DEPLOYMENT.md`

---

**Happy Coding! 🎨**

