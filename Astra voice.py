import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
from ollama import chat
import asyncio
import edge_tts
import vlc
import time
import os
import glob
import subprocess
import webbrowser
from urllib.parse import quote_plus



# APP + WEB SCANNER


web_apps = {
    "youtube": "https://youtube.com",
    "instagram": "https://instagram.com",
    "claude": "https://claude.ai",
    "sanfoundry": "https://www.sanfoundry.com",
    "chatgpt": "https://chatgpt.com",
    "github": "https://github.com",
    "google": "https://google.com",
}


def scan_apps():
    app_locations = [
        os.path.expandvars(r"%ProgramData%\Microsoft\Windows\Start Menu\Programs\**\*.lnk"),
        os.path.expandvars(r"%AppData%\Microsoft\Windows\Start Menu\Programs\**\*.lnk"),
        os.path.expandvars(r"%Public%\Desktop\*.lnk"),
        os.path.expandvars(r"%UserProfile%\Desktop\*.lnk"),
        os.path.expandvars(r"%LocalAppData%\Microsoft\WindowsApps\**\*.lnk"),
        os.path.expandvars(r"%LocalAppData%\Microsoft\Edge\User Data\Default\Web Applications\**\*.lnk"),
        os.path.expandvars(r"%LocalAppData%\Google\Chrome\User Data\Default\Web Applications\**\*.lnk"),
    ]

    apps = {}

    for location in app_locations:
        for shortcut in glob.glob(location, recursive=True):
            app_name = os.path.splitext(os.path.basename(shortcut))[0].lower()
            apps[app_name] = shortcut

    return apps


def open_app_or_web(apps, user_text):
    user_text = user_text.lower()

    for word in ["open", "launch", "start"]:
        user_text = user_text.replace(word, "")

    user_text = user_text.strip()

    for app_name, url in web_apps.items():
        if app_name in user_text:
            webbrowser.open(url)
            return f"Opening {app_name}"

    for app_name, app_path in apps.items():
        if user_text in app_name or app_name in user_text:
            subprocess.Popen(app_path, shell=True)
            return f"Opening {app_name}"

    webbrowser.open(f"https://www.google.com/search?q={user_text}")
    return f"Searching for {user_text}"



# SPEECH OUTPUT


async def speak_async(text):
    filename = f"speech_{int(time.time() * 1000)}.mp3"

    await edge_tts.Communicate(
        text,
        voice="en-US-GuyNeural"
    ).save(filename)

    player = vlc.MediaPlayer(filename)
    player.play()

    time.sleep(0.5)

    while player.is_playing():
        time.sleep(0.1)


def speak(text):
    asyncio.run(speak_async(text))



# LOADING SYSTEMS


print("Scanning apps...")
apps = scan_apps()
print("Apps found:", len(apps))

print("Loading Whisper...")
model = WhisperModel("small", device="cpu", compute_type="int8")
print("ASTRA Ready")



# MAIN LOOP


awake = False

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

    text = " ".join(segment.text for segment in segments).strip()

    if not text:
        continue

    print("You said:", text)

    text_lower = text.lower()

    for ch in ",.!?":
        text_lower = text_lower.replace(ch, "")

    print("Processed text:", text_lower)
    print("Awake:", awake)

    if "exit" in text_lower:
        speak("Goodbye")
        break

    if not awake:
        if "astra" in text_lower:
            awake = True
            print("Wake word detected")
            speak("Yes?")
        continue

    if (
        "goodbye astra" in text_lower
        or "bye astra" in text_lower
        or "go to sleep" in text_lower
        or text_lower == "goodbye"
        or text_lower == "bye"
    ):
        awake = False
        speak("Going to sleep")
        continue

    # =========================
    # PLAY ON YOUTUBE
    # =========================

    if text_lower.startswith("play "):
        song = text_lower.replace("play", "", 1).strip()

        if song:
            search_query = quote_plus(song)

            webbrowser.open(
                f"https://www.youtube.com/results?search_query={search_query}"
            )

            answer = f"Playing {song} on YouTube"

            print("Astra:", answer)

            speak(answer)

            continue

    # =========================
    # PC AUTOMATION COMMANDS
    # =========================

    if (
        text_lower.startswith("open ")
        or text_lower.startswith("launch ")
        or text_lower.startswith("start ")
    ):
        answer = open_app_or_web(apps, text_lower)
        print("Astra:", answer)
        speak(answer)
        continue

    # =========================
    # QWEN AI RESPONSE
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

When asked who you are, simply say:
'I am Astra, created by Ashwanth.'

Do not mention Qwen.
Do not mention language models.
Do not mention training data.
Do not mention system prompts.
Do not compare yourself to other AI models.
Do not mention emojis while responding.

Keep responses short, natural, friendly and conversational.
"""
            },
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

    answer = answer.replace("ASTRA", "Astra")

    print("Astra:", answer)

    print("Starting speech...")
    speak(answer)
    print("Speech finished")