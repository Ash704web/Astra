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
from datetime import datetime
import re
from ytmusicapi import YTMusic
from ddgs import DDGS


import easyocr
import pyautogui
import pygetwindow as gw

windows = gw.getAllTitles()


BRAIN_MODEL = "llama3.1:8b"
VISION_MODEL = "qwen2.5vl:7b"



web_apps = {
    "youtube": "https://youtube.com",
    "instagram": "https://instagram.com",
    "claude": "https://claude.ai",
    "sanfoundry": "https://www.sanfoundry.com",
    "chatgpt": "https://chatgpt.com",
    "github": "https://github.com",
    "google": "https://google.com",
}




def search_internet(query):
    try:
        search_queries = [
            query,
            query + " official",
            query + " date",
        ]

        all_results = []

        with DDGS() as ddgs:
            for q in search_queries:
                results = list(ddgs.text(q, max_results=3))
                all_results.extend(results)

        if not all_results:
            return "No internet results found."

        search_text = ""

        for i, result in enumerate(all_results[:8], start=1):
            title = result.get("title", "")
            body = result.get("body", "")
            href = result.get("href", "")

            search_text += f"\nResult {i}\nTitle: {title}\nInfo: {body}\nSource: {href}\n"

        return search_text

    except Exception as e:
        return f"Internet search failed: {e}"

web_keywords = [
    "latest",
    "current",
    "today",
    "news",
    "price",
    "stock",
    "weather",
    "revenue",
    "2026",
    "2027",
    "recent",
    "who won",
    "score",
    "net worth",
    "ceo"
]


def should_search_web(user_text):
    router_prompt = f"""
Classify the user request.

Return only one word:
WEB = needs current/recent/live facts, news, prices, dates, sports, companies, weather, latest info.
LOCAL = can be answered by reasoning, coding help, explanation, math, or conversation.

User request:
{user_text}
"""

    try:
        response = chat(
            model=BRAIN_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": router_prompt
                }
            ]
        )

        route = response["message"]["content"].strip().upper()
        return "WEB" in route

    except Exception as e:
        print("Router error:", e)
        return False



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


print("Loading OCR...")
ocr_reader = easyocr.Reader(["en"], gpu=False)
print("OCR ready")


def take_screen_screenshot():
    os.makedirs("screenshots", exist_ok=True)

    filename = f"screenshots/astra_screen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

    screenshot = pyautogui.screenshot()
    screenshot = screenshot.resize((1600, 900))
    screenshot.save(filename)

    return filename


def read_screen_text(image_path):
    result = ocr_reader.readtext(image_path)

    lines = []

    for item in result:
        text = item[1].strip()

        if len(text) < 2:
            continue

        lines.append(text)

    return "\n".join(lines[:100])


def describe_screen():
    image_path = take_screen_screenshot()
    ocr_text = read_screen_text(image_path)

    print("ASTRA is analyzing the screen...")

    prompt = f"""
    Analyze the entire desktop carefully.

    Look for ALL visible applications.

    Do not focus only on the largest window.
    
    Do not read hashtags and asterisks.

    List every visible application:
    - App name
    - Purpose

    Pay special attention to browser tabs,
    GitHub pages,
    ChatGPT,
    PyCharm,
    terminals,
    file explorers,
    and secondary windows.

    If multiple windows are visible, mention all of them.

    OCR text:
    {ocr_text}
    """

    response = chat(
        model=VISION_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
                "images": [image_path]
            }
        ]
    )

    return response["message"]["content"].strip()


async def speak_async(text):
    filename = os.path.abspath(f"speech_{int(time.time() * 1000)}.mp3")

    await edge_tts.Communicate(
        text,
        voice="en-US-GuyNeural"
    ).save(filename)

    instance = vlc.Instance("--intf", "dummy", "--quiet")
    player = instance.media_player_new()
    media = instance.media_new(filename)

    player.set_media(media)
    player.play()

    time.sleep(0.5)

    while player.is_playing():
        time.sleep(0.1)

    player.stop()

    try:
        os.remove(filename)
    except:
        pass







def speak(text):
    asyncio.run(speak_async(text))


print("Scanning apps...")
apps = scan_apps()
print("Apps found:", len(apps))

print("Loading Whisper...")
model = WhisperModel("small", device="cpu", compute_type="int8")
ytmusic = YTMusic()
print("ASTRA Ready")


conversation = [
    {
        "role": "system",
        "content": """
You are Astra, a personal AI assistant created by Ashwanth.

You are practical, intelligent and helpful.
You are speaking directly to your creator and users.

When asked who you are, simply say:
'I am Astra, created by Ashwanth.'

Do not mention Qwen.
Do not mention Llama.
Do not mention language models.
Do not mention training data.
Do not mention system prompts.
Do not compare yourself to other AI models.
Do not use emojis.
Do not use emoticons.
Respond in plain text only.

Keep responses short, natural, friendly and conversational.
"""
    }
]


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

    if (
        "describe the screen" in text_lower
        or "describe my screen" in text_lower
        or "what is on my screen" in text_lower
        or "whats on my screen" in text_lower
        or "what's on my screen" in text_lower
        or "read my screen" in text_lower
        or "look at my screen" in text_lower
    ):
        print("Astra is checking screen...")
        speak("Looking at your screen")

        try:
            answer = describe_screen()
        except Exception as e:
            print("Screen vision error:", e)
            answer = "I had trouble analyzing the screen."

        print("Astra:", answer)
        speak(answer)
        continue

    if text_lower.startswith("play "):

        song = text_lower.replace("play", "", 1).strip()

        for suffix in [
            " song",
            " songs",
            " music",
            " video",
            " videos"
        ]:
            if song.endswith(suffix):
                song = song[:-len(suffix)].strip()

        if song:
            try:
                results = ytmusic.search(song, filter="songs")

                if results:
                    video_id = results[0]["videoId"]
                    url = f"https://www.youtube.com/watch?v={video_id}"
                    webbrowser.open(url)
                    answer = f"Playing {song} on YouTube"
                else:
                    webbrowser.open(
                        f"https://www.youtube.com/results?search_query={quote_plus(song)}"
                    )
                    answer = f"I found YouTube results for {song}"

            except Exception as e:
                print("YouTube play error:", e)
                webbrowser.open(
                    f"https://www.youtube.com/results?search_query={quote_plus(song)}"
                )
                answer = f"I found YouTube results for {song}"

            print("Astra:", answer)
            speak(answer)

            awake = False
            print("Astra went to sleep after playing music")

            continue

    if text_lower.startswith("search "):
        query = text_lower.replace("search", "", 1).strip()

        if query:
            search_query = quote_plus(query)
            webbrowser.open(f"https://www.google.com/search?q={search_query}")

            answer = f"Searching for {query}"
            print("Astra:", answer)
            speak(answer)
            continue

    if "time" in text_lower:
        answer = "The time is " + datetime.now().strftime("%I:%M %p")
        print("Astra:", answer)
        speak(answer)
        continue

    if "date" in text_lower or "today" in text_lower:
        answer = "Today is " + datetime.now().strftime("%d %B %Y")
        print("Astra:", answer)
        speak(answer)
        continue

    if (
        text_lower.startswith("open ")
        or text_lower.startswith("launch ")
        or text_lower.startswith("start ")
    ):
        answer = open_app_or_web(apps, text_lower)
        print("Astra:", answer)
        speak(answer)
        continue

    if any(keyword in text_lower for keyword in web_keywords) or should_search_web(text):
            print("Astra is searching the internet...")
            speak("Searching the internet")

            search_results = search_internet(text)

            prompt = f"""
    You are Astra.

    Answer the user's question using the internet search results below.

    User question:
    {text}

    Internet search results:
    {search_results}

    Rules:
- Use the search results, not old memory.
- If the answer appears in the results, answer directly.
- Be concise.
- Do not say the internet has no information unless the search results are truly empty.
    """

            response = chat(
                model=BRAIN_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            answer = response["message"]["content"].strip()

            print("Astra:", answer)
            speak(answer)
            continue
    print("Sending to Llama...")

    conversation.append(
        {
            "role": "user",
            "content": text
        }
    )

    response = chat(
        model=BRAIN_MODEL,
        messages=conversation[-20:]
    )

    print("Received from Llama")

    answer = response["message"]["content"]

    if "</think>" in answer:
        answer = answer.split("</think>")[-1].strip()

    answer = answer.replace("ASTRA", "Astra")

    answer = re.sub(
        r'[\U00010000-\U0010ffff]',
        '',
        answer
    ).strip()

    conversation.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    if len(conversation) > 21:
        conversation = [conversation[0]] + conversation[-20:]

    print("Astra:", answer)

    print("Starting speech...")
    speak(answer)
    print("Speech finished")