// Main Application JavaScript

class ColoringPageApp {
    constructor() {
        this.isRecording = false;
        this.mediaRecorder = null;
        this.audioChunks = [];
        
        this.initElements();
        this.attachEventListeners();
    }

    initElements() {
        // Input elements
        this.promptInput = document.getElementById('promptInput');
        this.generateBtn = document.getElementById('generateBtn');
        this.voiceBtn = document.getElementById('voiceBtn');
        this.voiceIcon = document.getElementById('voiceIcon');
        this.voiceText = document.getElementById('voiceText');
        
        // Status elements
        this.recordingIndicator = document.getElementById('recordingIndicator');
        this.loadingSpinner = document.getElementById('loadingSpinner');
        this.errorMessage = document.getElementById('errorMessage');
        this.errorText = document.getElementById('errorText');
        
        // Result elements
        this.resultSection = document.getElementById('resultSection');
        this.resultImage = document.getElementById('resultImage');
        this.promptDisplay = document.getElementById('promptDisplay');
        this.downloadBtn = document.getElementById('downloadBtn');
        this.createAnotherBtn = document.getElementById('createAnotherBtn');
        
        // Example cards
        this.exampleCards = document.querySelectorAll('.example-card');
    }

    attachEventListeners() {
        // Generate button
        this.generateBtn.addEventListener('click', () => this.handleGenerate());
        
        // Voice button
        this.voiceBtn.addEventListener('click', () => this.handleVoiceInput());
        
        // Download button
        this.downloadBtn.addEventListener('click', () => this.handleDownload());
        
        // Create another button
        this.createAnotherBtn.addEventListener('click', () => this.resetApp());
        
        // Example cards
        this.exampleCards.forEach(card => {
            card.addEventListener('click', (e) => {
                const prompt = e.currentTarget.dataset.prompt;
                this.promptInput.value = prompt;
                this.promptInput.focus();
            });
        });
        
        // Enter key in textarea
        this.promptInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.handleGenerate();
            }
        });
    }

    async handleGenerate() {
        const prompt = this.promptInput.value.trim();
        
        if (!prompt) {
            this.showError('Please enter an idea or click an example!');
            return;
        }

        try {
            this.showLoading();
            this.hideError();

            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to generate image');
            }

            this.showResult(data.image_url, prompt);

        } catch (error) {
            console.error('Error:', error);
            this.showError(error.message || 'Oops! Something went wrong. Please try again.');
        } finally {
            this.hideLoading();
        }
    }

    async handleVoiceInput() {
        if (!this.isRecording) {
            await this.startRecording();
        } else {
            await this.stopRecording();
        }
    }

    async startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            
            this.mediaRecorder = new MediaRecorder(stream);
            this.audioChunks = [];

            this.mediaRecorder.addEventListener('dataavailable', event => {
                this.audioChunks.push(event.data);
            });

            this.mediaRecorder.addEventListener('stop', async () => {
                const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
                await this.transcribeAudio(audioBlob);
                
                // Stop all tracks
                stream.getTracks().forEach(track => track.stop());
            });

            this.mediaRecorder.start();
            this.isRecording = true;
            
            // Update UI
            this.voiceBtn.classList.add('recording');
            this.voiceIcon.textContent = '⏹️';
            this.voiceText.textContent = 'Click to Stop';
            this.recordingIndicator.classList.remove('hidden');

        } catch (error) {
            console.error('Error accessing microphone:', error);
            this.showError('Could not access microphone. Please check permissions.');
        }
    }

    async stopRecording() {
        if (this.mediaRecorder && this.isRecording) {
            this.mediaRecorder.stop();
            this.isRecording = false;
            
            // Update UI
            this.voiceBtn.classList.remove('recording');
            this.voiceIcon.textContent = '🎤';
            this.voiceText.textContent = 'Or Click to Speak';
            this.recordingIndicator.classList.add('hidden');
        }
    }

    async transcribeAudio(audioBlob) {
        try {
            this.showLoading();
            this.hideError();

            const formData = new FormData();
            formData.append('audio', audioBlob, 'recording.wav');

            const response = await fetch('/api/voice-to-text', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to transcribe audio');
            }

            // Set the transcribed text in the input
            this.promptInput.value = data.text;
            
            // Automatically generate the image
            this.hideLoading();
            await this.handleGenerate();

        } catch (error) {
            console.error('Error transcribing audio:', error);
            this.showError('Could not understand the audio. Please try again or type your idea.');
            this.hideLoading();
        }
    }

    handleDownload() {
        const imageSrc = this.resultImage.src;
        const link = document.createElement('a');
        link.href = imageSrc;
        link.download = 'my-coloring-page.png';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    showLoading() {
        this.loadingSpinner.classList.remove('hidden');
        this.generateBtn.disabled = true;
        this.voiceBtn.disabled = true;
    }

    hideLoading() {
        this.loadingSpinner.classList.add('hidden');
        this.generateBtn.disabled = false;
        this.voiceBtn.disabled = false;
    }

    showResult(imageUrl, prompt) {
        this.resultImage.src = imageUrl;
        this.promptDisplay.textContent = `"${prompt}"`;
        this.resultSection.classList.remove('hidden');
        
        // Scroll to result
        this.resultSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    showError(message) {
        this.errorText.textContent = message;
        this.errorMessage.classList.remove('hidden');
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            this.hideError();
        }, 5000);
    }

    hideError() {
        this.errorMessage.classList.add('hidden');
    }

    resetApp() {
        this.promptInput.value = '';
        this.resultSection.classList.add('hidden');
        this.hideError();
        this.promptInput.focus();
        
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ColoringPageApp();
});

