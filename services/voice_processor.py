import os
from config import Config


class VoiceProcessor:
    """Handles voice-to-text conversion using OpenAI Whisper API"""
    
    def __init__(self):
        self.openai_api_key = Config.OPENAI_API_KEY
    
    def transcribe_audio(self, audio_file_path):
        """
        Transcribe audio file to text using OpenAI Whisper API
        
        Args:
            audio_file_path (str): Path to audio file
            
        Returns:
            str: Transcribed text or None if failed
        """
        try:
            # Use OpenAI Whisper API
            if self.openai_api_key and self.openai_api_key != 'your-openai-api-key-here':
                return self._transcribe_with_whisper(audio_file_path)
            else:
                print("OpenAI API key not configured")
                return None
                
        except Exception as e:
            print(f"Error transcribing audio: {str(e)}")
            return None
    
    def _transcribe_with_whisper(self, audio_file_path):
        """Transcribe using OpenAI Whisper API"""
        try:
            import openai
            
            # Set the API key
            openai.api_key = self.openai_api_key
            
            # Read the audio file
            with open(audio_file_path, 'rb') as audio_file:
                # Transcribe using OpenAI Whisper
                response = openai.Audio.transcribe(
                    model="whisper-1",
                    file=audio_file,
                    language="en"  # You can change this or remove for auto-detection
                )
                
                return response.text.strip()
                
        except Exception as e:
            print(f"Error with Whisper transcription: {str(e)}")
            return None


# Example usage and testing
if __name__ == "__main__":
    processor = VoiceProcessor()
    
    # Test with an audio file
    test_audio_path = "test_audio.wav"
    if os.path.exists(test_audio_path):
        text = processor.transcribe_audio(test_audio_path)
        if text:
            print(f"✅ Transcribed text: {text}")
        else:
            print("❌ Failed to transcribe audio")
    else:
        print("No test audio file found")