import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import pyttsx3

tts = pyttsx3.init()
model = WhisperModel("tiny", device="cpu", compute_type="int8")

while True:
    print("Listening...")

    audio = sd.rec(
        int(5 * 16000),
        samplerate=16000,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    write("audio.wav", 16000, audio)

    segments, info = model.transcribe(
        "audio.wav",
        language="en"
    )

    text = " ".join(segment.text for segment in segments).strip()

    if not text:
        continue

    print("You said:", text)

    if "hello astra" in text.lower():
        response = "Hello Ashwanth"

    elif "who are you" in text.lower():
        response = "I am Astra, your personal assistant"

    elif "exit" in text.lower():
        response = "Goodbye"
        tts.say(response)
        tts.runAndWait()
        break

    else:
        response = "You said " + text

    print("Astra:", response)

    tts.say(response)
    tts.runAndWait()