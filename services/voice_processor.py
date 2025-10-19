import os
import speech_recognition as sr
from config import Config


class VoiceProcessor:
    """Handles voice-to-text conversion"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.openai_api_key = Config.OPENAI_API_KEY
    
    def transcribe_audio(self, audio_file_path):
        """
        Transcribe audio file to text
        
        Args:
            audio_file_path (str): Path to audio file
            
        Returns:
            str: Transcribed text or None if failed
        """
        try:
            # Try OpenAI Whisper first (if API key is available)
            if self.openai_api_key and self.openai_api_key != 'your-openai-api-key-here':
                text = self._transcribe_with_whisper(audio_file_path)
                if text:
                    return text
            
            # Fallback to Google Speech Recognition
            return self._transcribe_with_google(audio_file_path)
            
        except Exception as e:
            print(f"Error transcribing audio: {str(e)}")
            return None
    
    def _transcribe_with_whisper(self, audio_file_path):
        """
        Transcribe using OpenAI Whisper API
        
        Args:
            audio_file_path (str): Path to audio file
            
        Returns:
            str: Transcribed text or None
        """
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.openai_api_key)
            
            with open(audio_file_path, 'rb') as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="en"
                )
            
            return transcript.text
            
        except Exception as e:
            print(f"Whisper transcription error: {str(e)}")
            return None
    
    def _transcribe_with_google(self, audio_file_path):
        """
        Transcribe using Google Speech Recognition (free, no API key needed)
        
        Args:
            audio_file_path (str): Path to audio file
            
        Returns:
            str: Transcribed text or None
        """
        try:
            with sr.AudioFile(audio_file_path) as source:
                # Record the audio data
                audio_data = self.recognizer.record(source)
                
                # Recognize speech using Google Speech Recognition
                text = self.recognizer.recognize_google(audio_data)
                
                return text
                
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None
        except Exception as e:
            print(f"Google transcription error: {str(e)}")
            return None
    
    def transcribe_realtime_audio(self, audio_data):
        """
        Transcribe audio data from microphone in real-time
        
        Args:
            audio_data: Audio data from microphone
            
        Returns:
            str: Transcribed text or None
        """
        try:
            text = self.recognizer.recognize_google(audio_data)
            return text
        except Exception as e:
            print(f"Real-time transcription error: {str(e)}")
            return None

