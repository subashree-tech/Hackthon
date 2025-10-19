# Frontend Integration Guide

## 🌐 API Endpoint

**Base URL**: `https://your-project.vercel.app`

Replace `your-project.vercel.app` with your actual Vercel deployment URL.

---

## 📡 Available Endpoints

### 1. Health Check (GET)
```
GET /api/health
```

**Purpose**: Check if API is running

**Response**:
```json
{
  "status": "healthy",
  "service": "Kids Coloring Page Generator API",
  "timestamp": "2025-10-19T12:00:00",
  "environment": "production"
}
```

---

### 2. Generate Coloring Page (POST)
```
POST /api/generate
Content-Type: application/json
```

**Purpose**: Generate a coloring page from text prompt

**Request Body**:
```json
{
  "prompt": "A cute dolphin playing basketball underwater"
}
```

**Response** (Success):
```json
{
  "success": true,
  "image_data": "data:image/png;base64,iVBORw0KGgo...",
  "prompt": "A cute dolphin playing basketball underwater",
  "timestamp": "20251019_120000"
}
```

**Response** (Error):
```json
{
  "error": "Error message here"
}
```

**Notes**:
- Image is returned as base64-encoded data URI
- Can be directly used in `<img src="">` tag
- Generation takes 5-10 seconds
- Returns black & white line art suitable for coloring

---

### 3. Voice to Text (POST)
```
POST /api/voice-to-text
Content-Type: multipart/form-data
```

**Purpose**: Convert audio recording to text

**Request**:
- Form field name: `audio`
- Supported formats: WAV, MP3, OGG, WEBM, M4A
- Max size: 16MB

**Response** (Success):
```json
{
  "success": true,
  "text": "A cute dolphin playing basketball underwater"
}
```

**Response** (Error):
```json
{
  "error": "Error message here"
}
```

---

## 💻 Code Examples

### JavaScript (Fetch API)

#### Generate Coloring Page
```javascript
const API_BASE_URL = 'https://your-project.vercel.app';

async function generateColoringPage(prompt) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt: prompt })
    });
    
    const data = await response.json();
    
    if (data.success) {
      // Display the image
      const img = document.getElementById('coloring-page');
      img.src = data.image_data;
      return data;
    } else {
      console.error('Error:', data.error);
      return null;
    }
  } catch (error) {
    console.error('Request failed:', error);
    return null;
  }
}

// Usage
generateColoringPage("A cute cat playing with yarn");
```

#### Voice to Text
```javascript
async function transcribeAudio(audioBlob) {
  try {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.wav');
    
    const response = await fetch(`${API_BASE_URL}/api/voice-to-text`, {
      method: 'POST',
      body: formData
    });
    
    const data = await response.json();
    
    if (data.success) {
      console.log('Transcribed text:', data.text);
      return data.text;
    } else {
      console.error('Error:', data.error);
      return null;
    }
  } catch (error) {
    console.error('Request failed:', error);
    return null;
  }
}

// Usage with MediaRecorder
navigator.mediaDevices.getUserMedia({ audio: true })
  .then(stream => {
    const mediaRecorder = new MediaRecorder(stream);
    const audioChunks = [];
    
    mediaRecorder.addEventListener('dataavailable', event => {
      audioChunks.push(event.data);
    });
    
    mediaRecorder.addEventListener('stop', () => {
      const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
      transcribeAudio(audioBlob);
    });
    
    mediaRecorder.start();
    
    // Stop after 5 seconds
    setTimeout(() => mediaRecorder.stop(), 5000);
  });
```

---

### React Example

```javascript
import React, { useState } from 'react';

const API_BASE_URL = 'https://your-project.vercel.app';

function ColoringPageGenerator() {
  const [prompt, setPrompt] = useState('');
  const [imageData, setImageData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError('Please enter a prompt');
      return;
    }

    setLoading(true);
    setError(null);

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
      } else {
        setError(data.error || 'Failed to generate image');
      }
    } catch (err) {
      setError('Network error. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleVoiceInput = async (audioBlob) => {
    const formData = new FormData();
    formData.append('audio', audioBlob);

    try {
      const response = await fetch(`${API_BASE_URL}/api/voice-to-text`, {
        method: 'POST',
        body: formData
      });

      const data = await response.json();

      if (data.success) {
        setPrompt(data.text);
      } else {
        setError(data.error || 'Failed to transcribe audio');
      }
    } catch (err) {
      setError('Network error. Please try again.');
      console.error(err);
    }
  };

  return (
    <div className="coloring-page-generator">
      <h1>Generate Coloring Page</h1>
      
      <div className="input-section">
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter a prompt (e.g., 'A cute cat')"
          disabled={loading}
        />
        <button onClick={handleGenerate} disabled={loading || !prompt.trim()}>
          {loading ? 'Generating...' : 'Generate'}
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      {imageData && (
        <div className="result">
          <img src={imageData} alt="Generated coloring page" />
          <button onClick={() => {
            const link = document.createElement('a');
            link.href = imageData;
            link.download = 'coloring-page.png';
            link.click();
          }}>
            Download Image
          </button>
        </div>
      )}
    </div>
  );
}

export default ColoringPageGenerator;
```

---

### Vue.js Example

```vue
<template>
  <div class="coloring-page-generator">
    <h1>Generate Coloring Page</h1>
    
    <div class="input-section">
      <input
        v-model="prompt"
        type="text"
        placeholder="Enter a prompt (e.g., 'A cute cat')"
        :disabled="loading"
        @keyup.enter="handleGenerate"
      />
      <button @click="handleGenerate" :disabled="loading || !prompt.trim()">
        {{ loading ? 'Generating...' : 'Generate' }}
      </button>
    </div>

    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="imageData" class="result">
      <img :src="imageData" alt="Generated coloring page" />
      <button @click="downloadImage">Download Image</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ColoringPageGenerator',
  data() {
    return {
      prompt: '',
      imageData: null,
      loading: false,
      error: null,
      apiBaseUrl: 'https://your-project.vercel.app'
    };
  },
  methods: {
    async handleGenerate() {
      if (!this.prompt.trim()) {
        this.error = 'Please enter a prompt';
        return;
      }

      this.loading = true;
      this.error = null;

      try {
        const response = await fetch(`${this.apiBaseUrl}/api/generate`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ prompt: this.prompt })
        });

        const data = await response.json();

        if (data.success) {
          this.imageData = data.image_data;
        } else {
          this.error = data.error || 'Failed to generate image';
        }
      } catch (err) {
        this.error = 'Network error. Please try again.';
        console.error(err);
      } finally {
        this.loading = false;
      }
    },

    async handleVoiceInput(audioBlob) {
      const formData = new FormData();
      formData.append('audio', audioBlob);

      try {
        const response = await fetch(`${this.apiBaseUrl}/api/voice-to-text`, {
          method: 'POST',
          body: formData
        });

        const data = await response.json();

        if (data.success) {
          this.prompt = data.text;
        } else {
          this.error = data.error || 'Failed to transcribe audio';
        }
      } catch (err) {
        this.error = 'Network error. Please try again.';
        console.error(err);
      }
    },

    downloadImage() {
      const link = document.createElement('a');
      link.href = this.imageData;
      link.download = 'coloring-page.png';
      link.click();
    }
  }
};
</script>

<style scoped>
.error {
  color: red;
  margin: 10px 0;
}
.result img {
  max-width: 100%;
  border: 1px solid #ccc;
}
</style>
```

---

### Axios Example

```javascript
import axios from 'axios';

const API_BASE_URL = 'https://your-project.vercel.app';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds
  headers: {
    'Content-Type': 'application/json'
  }
});

// Generate coloring page
export async function generateColoringPage(prompt) {
  try {
    const response = await api.post('/api/generate', { prompt });
    return response.data;
  } catch (error) {
    console.error('Error generating coloring page:', error);
    throw error;
  }
}

// Voice to text
export async function voiceToText(audioBlob) {
  try {
    const formData = new FormData();
    formData.append('audio', audioBlob);
    
    const response = await api.post('/api/voice-to-text', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    return response.data;
  } catch (error) {
    console.error('Error transcribing audio:', error);
    throw error;
  }
}

// Health check
export async function checkHealth() {
  try {
    const response = await api.get('/api/health');
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    throw error;
  }
}
```

---

## 🎯 Best Practices

### 1. Error Handling
Always handle errors properly:

```javascript
try {
  const result = await generateColoringPage(prompt);
  if (result.success) {
    // Handle success
  } else {
    // Handle API error
    showError(result.error);
  }
} catch (error) {
  // Handle network error
  showError('Network error. Please check your connection.');
}
```

### 2. Loading States
Show loading indicators during API calls:

```javascript
setLoading(true);
try {
  const result = await generateColoringPage(prompt);
  // Handle result
} finally {
  setLoading(false);
}
```

### 3. Input Validation
Validate user input before sending:

```javascript
if (!prompt || prompt.trim().length === 0) {
  showError('Please enter a prompt');
  return;
}

if (prompt.length > 500) {
  showError('Prompt is too long (max 500 characters)');
  return;
}
```

### 4. Image Display
Display base64 images efficiently:

```javascript
// Direct display
<img src={imageData} alt="Coloring page" />

// Download functionality
const downloadImage = (imageData, filename = 'coloring-page.png') => {
  const link = document.createElement('a');
  link.href = imageData;
  link.download = filename;
  link.click();
};
```

### 5. Caching
Cache generated images to reduce API calls:

```javascript
const imageCache = new Map();

async function getCachedImage(prompt) {
  if (imageCache.has(prompt)) {
    return imageCache.get(prompt);
  }
  
  const result = await generateColoringPage(prompt);
  if (result.success) {
    imageCache.set(prompt, result.image_data);
  }
  
  return result.image_data;
}
```

---

## ⚡ Performance Tips

1. **Debounce voice input** - Wait for user to stop speaking before transcribing
2. **Show progress** - Display loading animations during generation (5-10 seconds)
3. **Retry logic** - Implement retry for failed requests
4. **Timeout handling** - Set appropriate timeouts (30 seconds recommended)
5. **Optimize images** - Consider compressing before display if needed

---

## 🔒 CORS & Security

- **CORS is enabled** - No special configuration needed
- **No authentication** required (add if needed)
- **HTTPS only** - Use the `https://` URL provided by Vercel
- **API keys** are stored securely on the backend (not exposed to frontend)

---

## 📊 API Limitations

| Item | Limit |
|------|-------|
| Max request size | 16 MB |
| Max execution time | 10 seconds (Free) / 60 seconds (Pro) |
| Image format | PNG (base64) |
| Audio formats | WAV, MP3, OGG, WEBM, M4A |

---

## 🧪 Testing Your Integration

### Test Checklist

- [ ] Health check endpoint works
- [ ] Can generate coloring page with text input
- [ ] Can upload and transcribe audio
- [ ] Error handling works properly
- [ ] Loading states display correctly
- [ ] Images display properly
- [ ] Download functionality works

### Sample Test Cases

```javascript
// Test 1: Simple prompt
await generateColoringPage("A cat");

// Test 2: Complex prompt
await generateColoringPage("A dolphin wearing a hat playing basketball underwater");

// Test 3: Empty prompt (should fail)
await generateColoringPage("");

// Test 4: Very long prompt
await generateColoringPage("A ".repeat(200));
```

---

## 🆘 Troubleshooting

### Issue: CORS Error
**Solution**: CORS is enabled. Check if you're using the correct URL (with `https://`)

### Issue: Request Timeout
**Solution**: Image generation takes time. Increase timeout to 30 seconds:
```javascript
fetch(url, { 
  signal: AbortSignal.timeout(30000) // 30 seconds
})
```

### Issue: Image Not Displaying
**Solution**: Ensure you're using the full base64 data URI (starts with `data:image/png;base64,`)

### Issue: Audio Upload Fails
**Solution**: 
- Check file size (< 16MB)
- Ensure correct Content-Type: `multipart/form-data`
- Verify field name is `audio`

---

## 📞 Support

**API Health**: Check `https://your-project.vercel.app/api/health`

**Backend Team Contact**: [Your contact info]

---

## 🔗 Additional Resources

- Full API Documentation: `README_API.md`
- Deployment Status: Vercel Dashboard
- Backend Repository: [Your GitHub URL]

---

**Happy coding! 🎨 Let us know if you need any help!**

