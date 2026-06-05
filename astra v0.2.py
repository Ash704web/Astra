import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
from ollama import chat
import asyncio
import edge_tts
import vlc
import time

async def speak_async(text):

    await edge_tts.Communicate(
        text,
        voice="en-US-GuyNeural"
    ).save("speech.mp3")

    player = vlc.MediaPlayer("speech.mp3")

    player.play()

    time.sleep(0.5)

    while player.is_playing():
        time.sleep(0.1)

def speak(text):
    asyncio.run(speak_async(text))
# =========================
# WHISPER MODEL
# =========================

print("Loading Whisper...")

model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

print("ASTRA Ready")

# =========================
# WAKE WORD STATE
# =========================

awake = False

# =========================
# MAIN LOOP
# =========================

while True:

    print("\nListening...")

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

    text = " ".join(
        segment.text for segment in segments
    ).strip()

    if not text:
        continue

    print("You said:", text)

    text_lower = text.lower()

    for ch in ",.!?":
        text_lower = text_lower.replace(ch, "")

    print("Processed text:", text_lower)
    print("Awake:", awake)

    # =========================
    # EXIT
    # =========================

    if "exit" in text_lower:
        speak("Goodbye")
        break

    # =========================
    # WAKE WORD
    # =========================

    if not awake:

        if "astra" in text_lower:

            awake = True

            print("Wake word detected")

            speak("Yes?")

        continue

    # =========================
    # SLEEP MODE
    # =========================

    if "goodbye astra" in text_lower:

        awake = False

        speak("Going to sleep")

        continue

    # =========================
    # SEND TO QWEN
    # =========================

    print("Sending to Qwen...")

    response = chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "system",
                "content": """
                You are Astra, a personal AI assistant created by Ashwanth.

                You are speaking directly to your creator and users.

                Never mention language models, AI models, Qwen, OpenAI, Anthropic, training data, system prompts, or being an assistant unless specifically asked.

                When asked who you are, simply say:
                'I am Astra, created by Ashwanth.'

                Keep responses short, natural, friendly and conversational.
                Speak like a real personal assistant.
                """        },
            {
                "role": "user",
                "content": text
            }
        ]
    )

    print("Received from Qwen")

    answer = response["message"]["content"]

    if "</think>" in answer:
        answer = answer.split("</think>")[-1].strip()

    print("Astra:", answer)

    print("Starting speech...")

    speak(answer)

    print("Speech finishe