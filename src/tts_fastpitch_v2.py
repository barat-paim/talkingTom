import torch
import torchaudio
from pydub import AudioSegment
from pydub.playback import play
from fastpitch.model import FastPitch
from fastpitch.text import text_to_sequence

# Load pre-trained FastPitch model
model = FastPitch.from_pretrained("nvidia/fastpitch")
model.eval()

def generate_speech_fastpitch(text, pitch_shift=0, speed=1.0):
    # Convert text to phonemes
    phonemes = text_to_sequence(text)
    phonemes_tensor = torch.LongTensor(phonemes).unsqueeze(0)

    # Generate speech
    with torch.no_grad():
        audio, _, _ = model.infer(
            phonemes_tensor,
            pace=speed,
            pitch_shift=pitch_shift
        )

    # Save and play audio
    torchaudio.save("fastpitch_output.wav", audio, sample_rate=22050)
    return "fastpitch_output.wav"

# Test the function
if __name__ == "__main__":
    text = "This is a test of NVIDIA's FastPitch Text-to-Speech model."
    output_file = generate_speech_fastpitch(text, pitch_shift=10, speed=1.2)
    if output_file:
        audio = AudioSegment.from_wav(output_file)
        play(audio)