# 🚀 Quick Start Guide

Get up and running in 5 minutes!

## Windows Users

### Option 1: Automated Setup (Recommended)
1. Double-click `setup.bat`
2. Wait for installation to complete
3. Edit `.env` file and add your API keys
4. Run the app:
   ```batch
   venv\Scripts\activate
   python run.py
   ```

### Option 2: Manual Setup
```batch
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy env.example .env
REM Edit .env with your API keys
python run.py
```

## macOS/Linux Users

### Option 1: Automated Setup (Recommended)
1. Open terminal in project directory
2. Make script executable: `chmod +x setup.sh`
3. Run setup: `./setup.sh`
4. Edit `.env` file and add your API keys
5. Run the app:
   ```bash
   source venv/bin/activate
   python run.py
   ```

### Option 2: Manual Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp env.example .env
# Edit .env with your API keys
python run.py
```

## Get Your API Keys

### 1. Stability AI (Required)
- Visit: https://platform.stability.ai/
- Sign up for free account
- Go to API Keys section
- Create new key
- Copy to `.env` file

### 2. OpenAI (Optional - for better voice)
- Visit: https://platform.openai.com/
- Sign up for account
- Create API key
- Copy to `.env` file
- *Note: If you skip this, free Google Speech Recognition will be used*

## Edit Your .env File

Open `.env` in any text editor and replace the placeholder values:

```
STABILITY_API_KEY=sk-your-actual-key-here
OPENAI_API_KEY=sk-your-openai-key-here
SECRET_KEY=any-random-string-you-want
```

## Run the App

1. Make sure virtual environment is activated
2. Run: `python run.py`
3. Open browser: http://localhost:5000
4. Start creating! 🎨

## Test It Out

Try these prompts:
- "A friendly dragon eating ice cream"
- "A robot playing with a puppy"
- "An astronaut riding a dinosaur"

## Troubleshooting

**Can't install packages?**
- Update pip: `python -m pip install --upgrade pip`
- Try: `pip install --upgrade pip setuptools wheel`

**API key errors?**
- Make sure `.env` file exists
- Check keys are copied correctly (no extra spaces)
- Restart the app after adding keys

**Port already in use?**
- Change PORT in `.env` to 5001 or another number
- Or stop the other application using port 5000

## Need Help?

Check the full [README.md](README.md) for detailed documentation!

---

**Happy Creating! 🎨✨**

