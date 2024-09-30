import requests
import json
import os
from pydub import AudioSegment
from pydub.playback import play

# Import & Load Environment Variables for ElevenLabs API
from dotenv import load_dotenv
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")

# Function to convert text to speech
def generate_tts(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    data = {
        "text": text,
        "model_id": "eleven_turbo_v2",
        "voice_settings": {
            "speaking_rate": 0.93,
            "stability": 0.7,
            "similarity_boost": 0.7,
            "style": 0.0,
            "use_speaker_boost": True
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        with open("tts_output.mp3", "wb") as f:
            f.write(response.content)
        return "tts_output.mp3"
    else:
        print(f"Error: {response.status_code}")
        return None
    
# Test the function
text = "Hello, this is a test of the TTS function. Tom wants to know if it worked"
output_file = generate_tts(text)    
if output_file:
    audio = AudioSegment.from_file(output_file)
    print("Tom, the TTS function worked!")
    play(audio)
else:
    print("No Tom, the TTS function failed to work.")