# ✅ Setup & Launch Checklist

Follow this checklist to get your Kids Coloring Page Generator up and running!

## 📋 Pre-Setup Checklist

- [ ] Python 3.8 or higher installed
  - Check: `python --version` or `python3 --version`
  - Download: https://www.python.org/downloads/

- [ ] pip installed and updated
  - Check: `pip --version`
  - Update: `python -m pip install --upgrade pip`

- [ ] Git installed (optional, for version control)
  - Check: `git --version`
  - Download: https://git-scm.com/downloads

## 🚀 Quick Setup (5 Minutes)

### Windows Users
- [ ] Run `setup.bat` (double-click or from command prompt)
- [ ] Wait for installation to complete
- [ ] Edit `.env` file with your API keys

### macOS/Linux Users
- [ ] Open terminal in project directory
- [ ] Run: `chmod +x setup.sh`
- [ ] Run: `./setup.sh`
- [ ] Edit `.env` file with your API keys

## 🔑 API Keys Setup

### Stability AI (Required for AI generation)
- [ ] Visit https://platform.stability.ai/
- [ ] Create account (free trial available)
- [ ] Navigate to "API Keys" section
- [ ] Click "Create API Key"
- [ ] Copy the key (starts with `sk-`)
- [ ] Paste into `.env` file: `STABILITY_API_KEY=sk-your-key-here`
- [ ] Verify you have credits in your account

### OpenAI (Optional - for better voice)
- [ ] Visit https://platform.openai.com/
- [ ] Create account
- [ ] Go to API Keys section
- [ ] Create new secret key
- [ ] Copy the key
- [ ] Paste into `.env` file: `OPENAI_API_KEY=sk-your-key-here`
- [ ] **Note:** If skipped, free Google Speech Recognition will be used

### Secret Key (Required)
- [ ] Generate a random string or use any password
- [ ] Add to `.env` file: `SECRET_KEY=your-random-string-here`

## 🧪 Test Installation (Optional but Recommended)

### Test 1: Demo Mode (No API Keys Needed)
- [ ] Run: `python demo_generator.py`
- [ ] Check if demo images are created in `demo_outputs/` folder
- [ ] ✅ If images appear, image processing works!

### Test 2: Dependencies Check
- [ ] Activate virtual environment:
  - Windows: `venv\Scripts\activate`
  - macOS/Linux: `source venv/bin/activate`
- [ ] Run: `python -c "import flask, PIL, cv2, requests; print('✅ All imports work!')"`
- [ ] ✅ If no errors, dependencies are installed correctly!

## 🎯 First Launch

- [ ] Activate virtual environment (if not already active)
  - Windows: `venv\Scripts\activate`
  - macOS/Linux: `source venv/bin/activate`

- [ ] Run the application: `python run.py`

- [ ] Look for success messages:
  ```
  ✅ Created directory: static/uploads
  ✅ Created directory: static/outputs
  🚀 Starting server...
  📱 Open your browser and go to: http://localhost:5000
  ```

- [ ] Open browser: http://localhost:5000

- [ ] You should see the colorful welcome page!

## 🎨 First Test Run

### Test Text Input
- [ ] Type a prompt: "A happy cat playing with yarn"
- [ ] Click "Create My Coloring Page"
- [ ] Wait 10-30 seconds
- [ ] ✅ Coloring page should appear!
- [ ] Click "Download" to save it

### Test Voice Input
- [ ] Click "Or Click to Speak" button
- [ ] Allow microphone access when prompted
- [ ] Speak clearly: "A robot gardening with flowers"
- [ ] Click button again to stop
- [ ] ✅ Text should appear and image should generate

### Test Example Prompts
- [ ] Click any example card (e.g., "Dinosaur on a Bicycle")
- [ ] ✅ Prompt should fill in text box
- [ ] Click "Create" to generate

## 🐛 Troubleshooting Checklist

If something doesn't work, check these:

### Installation Issues
- [ ] Virtual environment is activated (you should see `(venv)` in terminal)
- [ ] All packages installed: `pip list` shows flask, pillow, opencv-python, etc.
- [ ] Python version is 3.8+: `python --version`
- [ ] No error messages during `pip install -r requirements.txt`

### API Issues
- [ ] `.env` file exists in project root (not `env.example`)
- [ ] API keys are copied correctly (no extra spaces)
- [ ] Stability AI account has available credits
- [ ] API keys start with `sk-` for both services
- [ ] Restarted the app after adding keys

### Server Issues
- [ ] Port 5000 is not used by another app
- [ ] No firewall blocking localhost
- [ ] Browser allows localhost connections
- [ ] Console shows no error messages

### Voice Issues
- [ ] Using Chrome, Firefox, or Safari (IE not supported)
- [ ] Browser has microphone permission
- [ ] Using HTTPS or localhost (required for mic access)
- [ ] Microphone is working in other apps

## 📊 API Testing Checklist

- [ ] Start the Flask app: `python run.py`
- [ ] In a new terminal, run: `python test_api.py`
- [ ] Tests should show:
  - ✅ Health Check - PASS
  - ✅ Error Handling - PASS
  - ✅ Image Generation - PASS (if Stability AI key is valid)

## 🎉 Ready to Go Checklist

You're ready when you can check all these:

- [x] ✅ App starts without errors
- [x] ✅ Website loads at http://localhost:5000
- [x] ✅ Text input generates coloring pages
- [x] ✅ Can download generated images
- [x] ✅ Example prompts work
- [x] ✅ (Optional) Voice input works
- [x] ✅ (Optional) API tests pass

## 🚀 Next Steps

After everything works:

1. **Try different prompts:**
   - Simple animals: "A friendly dog", "A cute bunny"
   - Actions: "A bird flying", "A fish swimming"
   - Combinations: "A superhero cat in space"

2. **Explore settings:**
   - Edit `config.py` to adjust image quality
   - Try different edge detection thresholds

3. **Share with kids:**
   - Let them create their own coloring pages
   - Print and color the results!

4. **Read documentation:**
   - `README.md` - Full documentation
   - `DEPLOYMENT.md` - Deploy to cloud
   - `PROJECT_OVERVIEW.md` - Technical details

## 📞 Getting Help

If you're stuck:

1. **Check error messages** in terminal
2. **Read error messages** in browser console (F12)
3. **Review documentation** - README.md and QUICKSTART.md
4. **Test API keys** separately at their respective platforms
5. **Try demo mode** - `python demo_generator.py`

## 💡 Quick Tips

- **Specific prompts work better**: "A dolphin playing basketball" > "An animal"
- **Simple subjects**: Single objects work better than complex scenes
- **Be patient**: AI generation takes 10-30 seconds
- **Save your work**: Download images you like immediately
- **Experiment**: Try different prompt styles and keywords

---

## ✅ You're All Set!

When all checkboxes above are checked, you're ready to create amazing coloring pages!

**Happy Creating! 🎨✨**

Have fun turning imagination into art!

