import torch
import torchaudio
from pydub import AudioSegment
from pydub.playback import play
from nemo.collections.tts.models import FastPitchModel
from nemo.collections.tts.g2p import EnglishG2p

# Load pre-trained FastPitch model
model = FastPitchModel.from_pretrained(model_name="tts_en_fastpitch")
model.eval()

def generate_speech_fastpitch(text, pitch_shift=0, speed=1.0):
    # Convert text to phonemes
    g2p = EnglishG2p()
    phonemes = g2p(text)
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