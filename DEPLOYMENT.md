# 🚀 Deployment Guide

## Deployment Options

### 1. Local Development
Already covered in README.md and QUICKSTART.md

### 2. Deploy to Heroku

#### Prerequisites
- Heroku account (free tier available)
- Heroku CLI installed

#### Steps:
1. Create a `Procfile`:
   ```
   web: gunicorn app:app
   ```

2. Update `requirements.txt` to include:
   ```
   gunicorn==21.2.0
   ```

3. Create Heroku app:
   ```bash
   heroku create your-app-name
   ```

4. Set environment variables:
   ```bash
   heroku config:set STABILITY_API_KEY=your-key
   heroku config:set OPENAI_API_KEY=your-key
   heroku config:set SECRET_KEY=your-secret
   ```

5. Deploy:
   ```bash
   git push heroku main
   ```

### 3. Deploy to Railway

#### Steps:
1. Create account at [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub"
3. Select your repository
4. Add environment variables in Railway dashboard:
   - `STABILITY_API_KEY`
   - `OPENAI_API_KEY`
   - `SECRET_KEY`
5. Railway will auto-detect Flask and deploy

### 4. Deploy to Render

#### Steps:
1. Create account at [Render.com](https://render.com)
2. Create new Web Service
3. Connect your GitHub repository
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. Add environment variables in Render dashboard
6. Deploy

### 5. Deploy to PythonAnywhere

#### Steps:
1. Create account at [PythonAnywhere.com](https://www.pythonanywhere.com)
2. Upload your code
3. Create new web app (Flask)
4. Configure WSGI file
5. Set environment variables in web app settings
6. Reload web app

### 6. Deploy with Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p static/uploads static/outputs

EXPOSE 5000

CMD ["python", "run.py"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - STABILITY_API_KEY=${STABILITY_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./static/outputs:/app/static/outputs
```

Deploy:
```bash
docker-compose up --build
```

## Production Considerations

### Security
1. **Never commit `.env` file** - already in `.gitignore`
2. **Use strong SECRET_KEY** - generate with:
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```
3. **Enable HTTPS** - use reverse proxy (nginx) or platform SSL
4. **Rate limiting** - add Flask-Limiter:
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app, key_func=lambda: request.remote_addr)
   ```

### Performance
1. **Use production WSGI server** - gunicorn, uWSGI
2. **Enable caching** - for static files
3. **CDN** - for static assets
4. **Async processing** - for long-running image generation:
   - Use Celery + Redis for background tasks
   - Or implement webhook callbacks

### Monitoring
1. **Error tracking** - Sentry, Rollbar
2. **Logging** - Configure proper logging:
   ```python
   import logging
   logging.basicConfig(level=logging.INFO)
   ```
3. **Uptime monitoring** - UptimeRobot, Pingdom

### Scalability
1. **Horizontal scaling** - multiple workers
2. **Load balancer** - distribute traffic
3. **Database** - if storing user data (currently not needed)
4. **File storage** - AWS S3, Cloudinary for generated images

## Environment Variables Reference

Required:
- `STABILITY_API_KEY` - Your Stability AI API key
- `SECRET_KEY` - Flask secret key for sessions

Optional:
- `OPENAI_API_KEY` - For Whisper voice transcription
- `FLASK_ENV` - Set to `production` in production
- `HOST` - Default: 0.0.0.0
- `PORT` - Default: 5000

## Cost Considerations

### Stability AI Pricing
- Pay per image generated
- Check current pricing at https://platform.stability.ai/pricing
- Implement rate limiting to control costs

### OpenAI Pricing
- Whisper API: ~$0.006 per minute of audio
- Optional - can use free Google Speech Recognition

### Hosting
- **Free tiers available:**
  - Railway: 500 hours/month free
  - Render: 750 hours/month free
  - Heroku: Limited free tier
  - PythonAnywhere: Limited free tier

## Backup Strategy

1. **Code** - Git repository (already handled)
2. **Generated images** - Optional: sync to cloud storage
3. **Environment variables** - Document separately (never commit)

## Updates and Maintenance

1. **Keep dependencies updated:**
   ```bash
   pip list --outdated
   pip install --upgrade package-name
   ```

2. **Security updates:**
   ```bash
   pip install --upgrade pip
   pip audit  # Check for vulnerabilities
   ```

3. **Monitor API changes:**
   - Stability AI API updates
   - OpenAI API updates

## Troubleshooting Production Issues

### High Memory Usage
- Reduce `IMAGE_WIDTH` and `IMAGE_HEIGHT` in config.py
- Implement cleanup of old generated images
- Use smaller OpenCV operations

### Slow Response Times
- Optimize image processing
- Implement caching
- Use CDN for static files
- Consider async processing

### API Rate Limits
- Implement request queuing
- Add user rate limiting
- Cache common requests

## Support

For production deployment issues:
1. Check application logs
2. Verify environment variables
3. Test API keys separately
4. Monitor resource usage
5. Check platform-specific documentation

---

**Good luck with your deployment! 🚀**

