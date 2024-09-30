import numpy as np
from scipy.io import wavfile
from scipy import signal
from pydub import AudioSegment
from pydub.playback import play

def add_vocal_effects(input_file, output_file):
    # Read the audio file
    audio_segment = AudioSegment.from_file(input_file, format="mp3")
    sample_rate = audio_segment.frame_rate
    audio = np.array(audio_segment.get_array_of_samples())
    
    # Convert to float
    audio = audio.astype(np.float32) / np.iinfo(np.int16).max

    # Add subtle pitch variation (vibrato)
    t = np.arange(len(audio)) / sample_rate
    vibrato_rate = 5.0  # Hz
    vibrato_depth = 0.003
    vibrato = vibrato_depth * np.sin(2 * np.pi * vibrato_rate * t)
    audio_vibrato = audio * (1 + vibrato)

    # Add subtle reverb
    impulse_response = np.exp(-np.linspace(0, 0.25, sample_rate // 4))
    audio_reverb = signal.convolve(audio_vibrato, impulse_response, mode='same')

    # Normalize
    audio_reverb = audio_reverb / np.max(np.abs(audio_reverb))

    # Convert back to int16
    audio_reverb = (audio_reverb * np.iinfo(np.int16).max).astype(np.int16)

    # Write the processed audio to a new file
    audio_segment = AudioSegment(audio_reverb.tobytes(), frame_rate=sample_rate, sample_width=audio_segment.sample_width, channels=1)
    audio_segment.export(output_file, format="mp3")

# Test the function
if __name__ == "__main__":
    add_vocal_effects("tts_output.mp3","enhanced_output.mp3")
    audio = AudioSegment.from_file("enhanced_output.mp3", format="mp3")
    play(audio)