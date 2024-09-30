import json
from tts_elevenlabs import generate_speech_elevenlabs
from tts_fastpitch import generate_speech_fastpitch
from dsp_enhancements import add_vocal_effects
from pydub import AudioSegment
from pydub.playback import play

def process_dialogue(dialogue_file):
    with open(dialogue_file, 'r') as f:
        dialogue = json.load(f)

    for turn in dialogue:
        speaker = turn['speaker']
        text = turn['text']
        
        # Generate speech using ElevenLabs
        elevenlabs_output = generate_speech_elevenlabs(text)
        
        # Apply FastPitch for prosody control
        fastpitch_output = generate_speech_fastpitch(text, pitch_shift=5 if speaker == "Lex Fridman" else -5, speed=1.1)
        
        # Enhance the audio with DSP techniques
        add_vocal_effects(fastpitch_output, f"enhanced_{speaker}.wav")
        
        # Play the enhanced audio
        audio = AudioSegment.from_wav(f"enhanced_{speaker}.wav")
        play(audio)

        # Here you can add logic for interruption handling and content enhancement

# Process the dialogue
if __name__ == "__main__":
    process_dialogue("src/lex_perplexity_dialogue.json")