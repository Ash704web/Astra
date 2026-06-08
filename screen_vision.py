import os
from datetime import datetime

import pyautogui
import ollama
import easyocr

SCREENSHOT_FOLDER = "screenshots"
VISION_MODEL = "qwen2.5vl:7b"

os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)

print("Loading OCR...")
ocr_reader = easyocr.Reader(["en"], gpu=False)
print("OCR ready")


def take_full_screenshot():
    filename = f"full_screen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    path = os.path.join(SCREENSHOT_FOLDER, filename)

    screenshot = pyautogui.screenshot()
    screenshot = screenshot.resize((1280, 720))
    screenshot.save(path)

    return path


def read_ocr_text(image_path):
    result = ocr_reader.readtext(image_path)

    lines = []

    for item in result:
        text = item[1].strip()

        if len(text) < 2:
            continue

        lines.append(text)

    return "\n".join(lines[:100])


def analyze_screen_with_ocr():
    image_path = take_full_screenshot()

    print("Screenshot taken:", image_path)
    print("ASTRA is reading OCR text...")

    ocr_text = read_ocr_text(image_path)

    print("ASTRA is analyzing vision + OCR...")

    prompt = f"""
You are ASTRA's screen awareness module.

You have two inputs:
1. Screenshot image
2. OCR text extracted from the same screen

OCR text:
{ocr_text}

Task:
Analyze the full computer screen.

Separate each visible app/window.

For each window, mention:
- App name
- Main visible text
- What the user appears to be doing

Use the OCR text to improve accuracy.
If OCR text is messy, rely more on the image.
Be precise and avoid guessing.
"""

    response = ollama.chat(
        model=VISION_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
                "images": [image_path]
            }
        ]
    )

    return response["message"]["content"]


if __name__ == "__main__":
    answer = analyze_screen_with_ocr()

    print("\n========== ASTRA VISION + OCR ==========\n")
    print(answer)