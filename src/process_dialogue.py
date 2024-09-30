import json
from tts_v1 import generate_tts_elevenlabs
from pydub import AudioSegment
from pydub.playback import play

def process_dialogue(dialogue_file):
    with open(dialogue_file, 'r') as f:
        dialogue = json.load(f)

    for turn in dialogue:
        speaker = turn['speaker']
        text = turn['text']

        # Assign different speakers to different voices
        if speaker == "Lex Fridman": # voice for Lex Fridman
            speaker = "Bill"
        else:
            speaker = "Charlotte" # voice for perplexity CEO
        
        # Generate speech using ElevenLabs
        elevenlabs_output = generate_tts_elevenlabs(text, speaker)
        if elevenlabs_output:
            audio = AudioSegment.from_file(elevenlabs_output)
            print(f"Now playing: {speaker}")
            play(audio)
        else:
            print(f"Sorry Tom, it didn't work: {speaker}")

        # Here you can add logic for interruption handling and content enhancement

# Process the dialogue
if __name__ == "__main__":
    process_dialogue("src/lex_arvind.json")