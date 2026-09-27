import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import pygame
import os
import time

# LANGUAGE SETTINGS

LANGUAGES = {
    "english": "en",
    "hindi": "hi",
    "spanish": "es",
    "french": "fr",
    "german": "de",
    "japanese": "ja"
}

current_language = "english"

def set_language(language):
    global current_language

    language = language.lower().strip()

    if language in LANGUAGES:
        current_language = language
        return f"Language changed to {language}."

    return "Sorry, I don't support that language yet."

def listen(language="en-IN"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("I am Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            text = recognizer.recognize_google(audio, language=language)
            print("USER:", text)
            return text

        except sr.WaitTimeoutError:
            print("No speech detected.")
            return ""

        except sr.UnknownValueError:
            print("Could not understand.")
            return ""

        except sr.RequestError as e:
            print("Speech recognition error:", e)
            return ""

def translate_text(text, source="auto", target="en"):

    try:
        translated = GoogleTranslator(source=source, target=target).translate(text)
        return translated

    except Exception as e:
        print("Translation error:", e)
        return text

def speak_multilingual(text):
    language_code = LANGUAGES[current_language]
    print(f"JARVIS [{current_language}]:", text)

    try:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        TEMP_DIR = os.path.join(BASE_DIR, "Temp")

        os.makedirs(TEMP_DIR, exist_ok=True)

        filename = os.path.join(TEMP_DIR, "jarvis_voice.mp3")
        tts = gTTS(text=text, lang=language_code, slow=False)
        tt.save(filename)

        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

            pygame.mixer.music.stop()
            pygame.mixer.quit()

            if os.path.exists(filename):
                os.remove(filename)

    except Exception as e:
        print("TTS Error:", e)

def process_language_command(command):
    command = command.lower()

    if "switch to hindi" in command:
        set_language("hindi")
        speak_multilingual("ठीक है, अब मैं हिंदी में बात करूंगा।")
        return True

    if "switch to english" in command:
        set_language("english")
        speak_multilingual("Okey Sir, I will speak English now.")
        return True

    if "switch to spanish" in command:
        set_language("spanish")
        speak_multilingual("Entendido, ahora hablaré español.")
        return True

    if "switch to french" in command:
        set_language("french")
        speak_multilingual("D'accord, je vais parler français maintenant.")
        return True

    if "switch to german" in command:
        set_language("german")
        speak_multilingual("Okay, ich werde jetzt Deutsch sprechen.")
        return True

    if "switch to japanese" in command:
        set_language("japanese")
        speak_multilingual("わかりました。これから日本語で話します。")
        return True

    return False

if __name__ == "__main__":

    print("================================")
    print("      JARVIS MULTILINGUAL")
    print("================================")

    speak_multilingual(
        "Hello sir. I am ready to speak multiple languages."
    )

    while True:

        command = listen("en-IN")

        if not command:
            continue

        if command == "exit":
            speak_multilingual("Goodbye sir.")
            break

        if process_language_command(command):
            continue

        # Example response
        if "hello" in command.lower():
            speak_multilingual("Hello sir. How can I help you?")