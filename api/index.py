from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import uuid
from datetime import datetime

# Add parent directory to path to import services
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from services.image_generator import ImageGenerator
from services.voice_processor import VoiceProcessor

# Initialize Flask app
app = Flask(__name__)

# Configure CORS - allow all origins for frontend flexibility
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# For Vercel, we'll use /tmp directory for temporary files
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['OUTPUT_FOLDER'] = '/tmp/outputs'

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Initialize services
image_generator = ImageGenerator()
voice_processor = VoiceProcessor()


@app.route('/')
def index():
    """API root endpoint"""
    return jsonify({
        'service': 'Kids Coloring Page Generator API',
        'version': '1.0.0',
        'status': 'active',
        'endpoints': {
            'health': '/api/health',
            'generate': '/api/generate (POST)',
            'voice_to_text': '/api/voice-to-text (POST)'
        }
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Kids Coloring Page Generator API',
        'timestamp': datetime.now().isoformat(),
        'environment': 'production'
    })


@app.route('/api/generate', methods=['POST', 'OPTIONS'])
def generate_coloring_page():
    """
    Generate coloring page from text input
    Expected JSON: {"prompt": "A dolphin playing basketball underwater"}
    """
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.get_json()
        prompt = data.get('prompt', '').strip()
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        output_filename = f'coloring_page_{timestamp}_{unique_id}.png'
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        # Generate coloring page
        success = image_generator.generate_coloring_page(prompt, output_path)
        
        if success:
            # For Vercel, we need to return the image data directly or upload to cloud storage
            # Here we'll return a base64 encoded image
            import base64
            with open(output_path, 'rb') as img_file:
                img_data = base64.b64encode(img_file.read()).decode('utf-8')
            
            # Clean up temp file
            if os.path.exists(output_path):
                os.remove(output_path)
            
            return jsonify({
                'success': True,
                'image_data': f'data:image/png;base64,{img_data}',
                'prompt': prompt,
                'timestamp': timestamp
            })
        else:
            return jsonify({'error': 'Failed to generate image'}), 500
            
    except Exception as e:
        app.logger.error(f'Error generating coloring page: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/voice-to-text', methods=['POST', 'OPTIONS'])
def voice_to_text():
    """
    Convert voice audio to text
    Expected: audio file in request.files
    """
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        
        if audio_file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        # Save audio file temporarily
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        temp_filename = f'audio_{timestamp}_{uuid.uuid4().hex[:8]}.wav'
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], temp_filename)
        audio_file.save(temp_path)
        
        # Convert to text
        text = voice_processor.transcribe_audio(temp_path)
        
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        if text:
            return jsonify({
                'success': True,
                'text': text
            })
        else:
            return jsonify({'error': 'Failed to transcribe audio'}), 500
            
    except Exception as e:
        app.logger.error(f'Error processing voice: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


# Vercel serverless function handler
# The app variable is automatically detected by Vercel

# For local testing
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

