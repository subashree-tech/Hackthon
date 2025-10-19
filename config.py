import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-this')
    
    # Stability AI Configuration
    STABILITY_API_KEY = os.getenv('STABILITY_API_KEY', '')
    STABILITY_API_HOST = os.getenv('STABILITY_API_HOST', 'https://api.stability.ai')
    
    # OpenAI Configuration (for voice transcription)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # Image Generation Settings
    IMAGE_WIDTH = 1024
    IMAGE_HEIGHT = 1024
    CFG_SCALE = 7.0
    STEPS = 30
    SAMPLES = 1
    
    # Coloring Page Settings
    EDGE_THRESHOLD_LOW = 50
    EDGE_THRESHOLD_HIGH = 150
    CONTOUR_THICKNESS = 2
    
    # Fill Marker Settings
    ADD_FILL_MARKERS = True
    MARKER_TYPE = 'circle'  # 'circle', 'triangle', 'square'
    MARKER_SIZE = 8
    MIN_AREA_FOR_MARKER = 500
    
    # File Upload Settings
    UPLOAD_FOLDER = 'static/uploads'
    OUTPUT_FOLDER = 'static/outputs'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # Allowed file extensions
    ALLOWED_AUDIO_EXTENSIONS = {'wav', 'mp3', 'ogg', 'webm', 'm4a'}


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

