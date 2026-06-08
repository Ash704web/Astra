import os
import re
import pygetwindow as gw
import psutil


PROJECT_PATH = r"C:\Users\Ashwanth MP\PycharmProjects\Astra"


def get_active_window():
    try:
        window = gw.getActiveWindow()
        return window.title if window else "Unknown"
    except:
        return "Unknown"


def get_open_windows():
    titles = []
    try:
        for window in gw.getAllWindows():
            title = window.title.strip()
            if title and title not in titles:
                titles.append(title)
    except:
        pass

    return titles[:15]


def detect_current_file():
    active = get_active_window()

    possible_extensions = [
        ".py", ".txt", ".md", ".html", ".css", ".js", ".json"
    ]

    for ext in possible_extensions:
        if ext in active:
            parts = active.replace("-", "–").split("–")
            for part in parts:
                if ext in part:
                    return part.strip()

    return "Unknown"


def get_project_files():
    files = []

    for root, dirs, filenames in os.walk(PROJECT_PATH):
        dirs[:] = [d for d in dirs if d not in [".venv", "__pycache__", ".git", "screenshots"]]

        for filename in filenames:
            if filename.endswith((".py", ".md", ".txt", ".json")):
                files.append(os.path.join(root, filename))

    return files[:50]


def detect_terminal_errors():
    error_keywords = [
        "traceback",
        "error",
        "exception",
        "failed",
        "not found",
        "syntaxerror",
        "modulenotfounderror",
        "nameerror",
        "typeerror",
        "valueerror"
    ]

    possible_logs = []

    for root, dirs, files in os.walk(PROJECT_PATH):
        dirs[:] = [d for d in dirs if d not in [".venv", "__pycache__", ".git", "screenshots"]]

        for file in files:
            if file.endswith((".log", ".txt")):
                possible_logs.append(os.path.join(root, file))

    found = []

    for log_file in possible_logs:
        try:
            with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()[-5000:]

            lower = text.lower()

            if any(word in lower for word in error_keywords):
                found.append({
                    "file": log_file,
                    "content": text[-1500:]
                })

        except:
            pass

    return found


def summarize_computer_state():
    active = get_active_window()
    windows = get_open_windows()
    current_file = detect_current_file()
    project_files = get_project_files()
    errors = detect_terminal_errors()

    summary = f"""
Active Window:
{active}

Current File:
{current_file}

Open Windows:
{chr(10).join(windows)}

Project Files:
{chr(10).join(project_files[:20])}

Terminal/Error Logs Found:
{len(errors)}
"""

    return summary.strip()


if __name__ == "__main__":
    print(summarize_computer_state())