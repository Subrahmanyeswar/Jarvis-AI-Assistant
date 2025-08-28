# C:\Users\SUBBU\Downloads\RealTimeSecuritySystem\ai_core\voice_input.py

import os
import sounddevice as sd
import soundfile as sf
import whisper
import torch
import numpy as np

SAMPLE_RATE = 16000  # Whisper expects 16k audio
_model = None

def _ensure_model(device=None):
    global _model
    if _model is None:
        device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        print(f"⚙️ Loading Whisper model on {device}...")
        # The only change is here: "base" is now "small"
        _model = whisper.load_model("small", device=device)
        print("🧠 Whisper model loaded.")
    return _model

def record_audio(filename="input.wav", duration=4, fs=SAMPLE_RATE):
    """
    Record audio and save inside the ai_core folder. Returns absolute path.
    """
    file_path = os.path.join(os.path.dirname(__file__), filename)
    print("🎙️ Recording...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype="float32")
    sd.wait()
    sf.write(file_path, audio, fs)
    print("✅ Done recording. Saved as:", file_path)
    return file_path

def transcribe_audio(file_path):
    """
    Transcribe audio using Whisper. Handles resampling if necessary.
    """
    if not os.path.exists(file_path):
        print(f"⚠️ Error: file not found -> {file_path}")
        return ""

    try:
        model = _ensure_model()
        audio, sr = sf.read(file_path, dtype="float32")
        
        if audio.ndim > 1:
            audio = np.mean(audio, axis=1)

        if sr != SAMPLE_RATE:
            try:
                import librosa
                audio = librosa.resample(audio, orig_sr=sr, target_sr=SAMPLE_RATE)
            except Exception:
                print(f"⚠️ Warning: file sr={sr} != {SAMPLE_RATE}. Transcription may be inaccurate.")

        print("🧠 Transcribing...")
        result = model.transcribe(audio)
        text = result.get("text", "").strip()
        return text
    except Exception as e:
        print("❌ Transcription failed:", e)
        return ""