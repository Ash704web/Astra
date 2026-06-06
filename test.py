import asyncio
import edge_tts
from playsound import playsound

async def speak(text):
    await edge_tts.Communicate(
        text,
        voice="en-US-GuyNeural"
    ).save("speech.mp3")

    playsound("speech.mp3")

asyncio.run(speak("Hello Ashwanth. I am Astra."))