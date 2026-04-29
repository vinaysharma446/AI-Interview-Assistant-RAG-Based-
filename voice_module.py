import whisper
import sounddevice as sd
from scipy.io.wavfile import write
from gtts import gTTS
import os
import numpy as np

model = whisper.load_model("base")

# 🔥 Flexible recording (user-controlled duration input)
def record_audio(filename="input.wav", duration=30, fs=44100):
    print("Recording... Speak now")

    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()

    write(filename, fs, recording)
    print("Recording finished")

    return filename


# 🔤 Speech to text
def speech_to_text(audio_file):
    result = model.transcribe(audio_file)
    return result["text"]


# 🔊 Text to speech
def speak(text):
    tts = gTTS(text)
    tts.save("output.mp3")
    os.system("start output.mp3")