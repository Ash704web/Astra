import os
import glob
import subprocess
import webbrowser

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


def open_app(apps, user_text):
    user_text = user_text.lower()

    for word in ["open", "launch", "start"]:
        user_text = user_text.replace(word, "")

    user_text = user_text.strip()

    # First check web apps / websites
    for app_name, url in web_apps.items():
        if app_name in user_text:
            webbrowser.open(url)
            return f"Opening {app_name}"

    # Then check installed Windows apps
    for app_name, app_path in apps.items():
        if user_text in app_name or app_name in user_text:
            subprocess.Popen(app_path, shell=True)
            return f"Opening {app_name}"

    webbrowser.open(
        f"https://www.google.com/search?q={user_text}"
    )

    return f"Searching for {user_text}"


apps = scan_apps()

print("Apps found:", len(apps))

while True:
    command = input("Command: ")

    if command.lower() == "exit":
        break

    result = open_app(apps, command)
    print(result)

