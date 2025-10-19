# 🎨 Kids Coloring Page Generator

An interactive Flask application that transforms children's imagination into coloring pages! Kids can describe their ideas through text or voice, and the app generates monochrome coloring pages using AI-powered image generation.

## ✨ Features

- **Text Input**: Type any creative idea and get a coloring page
- **Voice Input**: Speak your idea and watch it come to life
- **AI-Powered**: Uses Stability AI's Diffusion model for image generation
- **Kid-Friendly UI**: Colorful, playful interface designed for children
- **Instant Download**: Save your coloring pages as PNG files
- **Example Prompts**: Pre-made ideas to spark creativity

## 🎯 The Vision

Kids are natural storytellers. This application allows children to say or type one line describing an idea, and the system generates monochrome coloring pages — outline-style images designed for single-color fill.

**Example:** 
> "A dolphin playing basketball underwater."

**Output:** 
> Coloring page with black outlines on white background ready for printing and coloring!

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Stability AI API key ([Get it here](https://platform.stability.ai/))
- OpenAI API key (optional, for better voice transcription - [Get it here](https://platform.openai.com/))

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd Hackthon
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables:**
   - Copy `env.example` to create your own `.env` file:
     ```bash
     copy env.example .env   # Windows
     cp env.example .env     # macOS/Linux
     ```
   - Edit `.env` and add your API keys:
     ```
     STABILITY_API_KEY=your-actual-stability-api-key
     OPENAI_API_KEY=your-actual-openai-api-key  # Optional
     SECRET_KEY=your-random-secret-key
     ```

### Getting API Keys

#### Stability AI API Key (Required)
1. Visit [Stability AI Platform](https://platform.stability.ai/)
2. Sign up for an account
3. Navigate to API Keys section
4. Generate a new API key
5. Copy it to your `.env` file

#### OpenAI API Key (Optional - for better voice transcription)
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign up for an account
3. Navigate to API Keys
4. Create a new secret key
5. Copy it to your `.env` file

**Note:** If you don't provide an OpenAI API key, the app will use free Google Speech Recognition for voice input.

## 🎮 Running the Application

1. **Ensure your virtual environment is activated**

2. **Create necessary directories:**
   ```bash
   mkdir static\uploads static\outputs   # Windows
   mkdir -p static/uploads static/outputs # macOS/Linux
   ```

3. **Run the Flask application:**
   ```bash
   python app.py
   ```

4. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```

5. **Start creating!** 🎨

## 📖 How to Use

### Text Input Method:
1. Type your creative idea in the text box (e.g., "A friendly dragon eating ice cream")
2. Click "Create My Coloring Page"
3. Wait a few seconds for the AI to generate your coloring page
4. Download your coloring page and start coloring!

### Voice Input Method:
1. Click the "Or Click to Speak" button
2. Allow microphone access when prompted
3. Speak your idea clearly
4. Click the button again to stop recording
5. The app will transcribe your voice and automatically generate the coloring page

### Example Ideas:
- Click any of the example cards for instant inspiration
- Mix and match: animals + activities + locations!

## 🏗️ Project Structure

```
Hackthon/
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── env.example            # Environment variables template
├── README.md              # This file
│
├── services/              # Business logic modules
│   ├── __init__.py
│   ├── image_generator.py # AI image generation & processing
│   └── voice_processor.py # Voice-to-text transcription
│
├── templates/             # HTML templates
│   └── index.html         # Main application page
│
└── static/                # Static assets
    ├── css/
    │   └── style.css      # Stylesheet
    ├── js/
    │   └── app.js         # Frontend JavaScript
    ├── uploads/           # Temporary audio files
    └── outputs/           # Generated coloring pages
```

## 🔧 Configuration

### Image Generation Settings

Edit `config.py` to customize:

```python
IMAGE_WIDTH = 512              # Output image width
IMAGE_HEIGHT = 512             # Output image height
CFG_SCALE = 7.0               # Creativity vs accuracy (1-20)
STEPS = 30                     # Generation steps (more = better quality)
EDGE_THRESHOLD_LOW = 50       # Edge detection sensitivity
EDGE_THRESHOLD_HIGH = 150     # Edge detection sensitivity
```

## 🎨 How It Works

1. **Input Processing**: Text or voice input is received and processed
2. **Prompt Enhancement**: The prompt is enhanced with keywords like "line art", "coloring book style"
3. **AI Generation**: Stability AI generates a base image from the enhanced prompt
4. **Image Processing**: The image is converted to grayscale and edges are detected using OpenCV
5. **Coloring Page Creation**: Edges are enhanced and inverted to create black outlines on white background
6. **Output**: The final coloring page is saved and displayed

## 🐛 Troubleshooting

### "No valid Stability API key found"
- Make sure you've created a `.env` file with your API key
- Ensure the key starts with `sk-` and is correctly copied
- Restart the Flask application after adding the key

### Voice input not working
- Check microphone permissions in your browser
- Ensure you're using HTTPS or localhost (required for microphone access)
- Try refreshing the page and allowing permissions again

### Images not generating
- Check your Stability AI account has credits
- Verify your API key is active
- Check the console for error messages

### "Module not found" errors
- Make sure you've installed all requirements: `pip install -r requirements.txt`
- Verify your virtual environment is activated

## 🌟 Advanced Features (Future Enhancements)

- **Fill Markers**: Add small symbols to indicate fill zones
- **Multiple Pages**: Generate a series of related coloring pages
- **Difficulty Levels**: Simple, medium, or detailed coloring pages
- **Print-Ready PDFs**: Generate PDF booklets
- **Gallery**: Save and view past creations
- **Sharing**: Share creations with friends

## 📝 API Endpoints

- `GET /` - Main application page
- `POST /api/generate` - Generate coloring page from text
  ```json
  {
    "prompt": "A dolphin playing basketball underwater"
  }
  ```
- `POST /api/voice-to-text` - Convert voice to text
  - Accepts: multipart/form-data with audio file
- `GET /api/health` - Health check endpoint

## 🤝 Contributing

This project was created for a hackathon. Feel free to fork, modify, and enhance!

## 📄 License

This project is open source and available for educational purposes.

## 🎉 Credits

- **Stability AI** - For the amazing Stable Diffusion model
- **OpenCV** - For image processing capabilities
- **Flask** - For the web framework
- **OpenAI** - For Whisper voice transcription

## 💡 Tips for Best Results

1. **Be Specific**: "A happy elephant wearing a hat" works better than just "elephant"
2. **Simple Subjects**: Single subjects work better than complex scenes
3. **Kid-Friendly**: Keep ideas appropriate and fun for children
4. **Action Words**: Add actions like "playing", "dancing", "flying" for more dynamic images

## 🆘 Support

If you encounter any issues:
1. Check the browser console for errors (F12)
2. Check the Flask terminal output for server errors
3. Verify all API keys are correctly set
4. Make sure all dependencies are installed

---

**Made with ❤️ for creative kids everywhere!**

Enjoy creating magical coloring pages! 🎨✨

