import requests
import json
import os
from pydub import AudioSegment
from pydub.playback import play

# Import & Load Environment Variables for ElevenLabs API
from dotenv import load_dotenv
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Function to convert text to speech
def generate_tts_elevenlabs(text, speaker):
    voice_id_map = {
        "Charlotte": "XB0fDUnXU5powFXDhCwa",
        "Bill": "pqHfZKP75CvOlQylNhV4",
        "Chris": "iP95p4xoKVk53GoZ742B",
        "Eric": "21m00Tcm4TlvDq8ikWAM",
        "Jessica": "pNInz6ZQeWZPnTJ2"
    }

    voice_id = voice_id_map.get(speaker, "XB0fDUnXU5powFXDhCwa")  # Default to Charlotte if speaker not found
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.7,
            "similarity_boost": 0.7,
            "style": 0.5,
            "use_speaker_boost": True
        }
    }

    # Debugging information
    print(f"URL: {url}")
    print(f"Headers: {headers}")
    print(f"Data: {json.dumps(data, indent=4)}")

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        with open("tts_output.mp3", "wb") as f:
            f.write(response.content)
        return "tts_output.mp3"
    else:
        print(f"Error: {response.status_code}")
        print(f"Response: {response.text}")
        return None

# Test the function
text = "Hello, this is a test of the TTS function. Tom wants to know if it worked"
speaker = "Eric"  # Specify the speaker
output_file = generate_tts_elevenlabs(text, speaker)    
if output_file:
    audio = AudioSegment.from_file(output_file)
    print("Tom, the TTS function worked!")
    play(audio)
else:
    print("No Tom, the TTS function failed to work.")