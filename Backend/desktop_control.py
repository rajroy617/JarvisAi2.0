import ctypes
import os
import subprocess
import shutil
import pyautogui
import time


def open_application(app_name):
    app_name = app_name.lower().strip()

    # Windows applications
    applications = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "calc": "calc.exe",
        "paint": "mspaint.exe",
        "explorer": "explorer.exe",
    }

    # Chrome
    if app_name in ["chrome", "google chrome"]:
        chrome_paths = [
            os.path.expandvars(
                r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"
            ),
            os.path.expandvars(
                r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
            ),
            os.path.expandvars(
                r"%LocalAppData%\Google\Chrome\Application\chrome.exe"
            ),
        ]

        for path in chrome_paths:
            if os.path.exists(path):
                subprocess.Popen([path])
                return "Opening Google Chrome."

        # Try Windows PATH
        chrome = shutil.which("chrome")
        if chrome:
            subprocess.Popen([chrome])
            return "Opening Google Chrome."

        return "Google Chrome was not found on this computer."

    # Other applications
    if app_name in applications:
        try:
            subprocess.Popen(applications[app_name])
            return f"Opening {app_name}."
        except Exception as e:
            return f"Unable to open {app_name}: {e}"

    return f"I don't know how to open {app_name}."


def take_screenshot():
    filename = f"screenshot_{int(time.time())}.png"
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    return f"Screenshot saved as {filename}"


def minimize_window():
    pyautogui.hotkey("win", "down")
    return "Window minimized."


def maximize_window():
    pyautogui.hotkey("win", "up")
    return "Window maximized."


def lock_pc():
    try:
        ctypes.windll.user32.LockWorkStation()
        return "जी सर, कंप्यूटर लॉक कर दिया गया है।"
    except Exception as e:
        print("Lock Error:", e)
        return "Sorry sir, I could not lock the computer."

def shutdown_pc():
    os.system("shutdown /s /t 5")
    return "Computer will shut down in 5 seconds."


def restart_pc():
    os.system("shutdown /r /t 5")
    return "Computer will restart in 5 seconds."


def cancel_shutdown():
    os.system("shutdown /a")
    return "Scheduled shutdown or restart has been cancelled."