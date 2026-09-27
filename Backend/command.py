import time
import speech_recognition as sr
import eel
import asyncio
import edge_tts
import pygame
import os
from Backend.desktop_control import (
    open_application,
    shutdown_pc,
    restart_pc,
    lock_pc,
    take_screenshot
)

VOICE_HI = "hi-IN-MadhurNeural"
VOICE_EN = "en-US-GuyNeural"


def is_hindi(text):
    """
    Detect Devanagari/Hindi characters.
    """
    hindi_chars = 0
    english_chars = 0

    for char in text:
        if '\u0900' <= char <= '\u097F':
            hindi_chars += 1
        elif char.isalpha():
            english_chars += 1

    return hindi_chars > english_chars


async def _speak(text, voice):
    output_file = "jarvis_voice.mp3"

    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)

        pygame.mixer.init()
        pygame.mixer.music.load(output_file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)

    except Exception as e:
        print("TTS Error:", e)

    finally:
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except:
            pass

        if os.path.exists(output_file):
            try:
                os.remove(output_file)
            except:
                pass


def speak(hindi_text, english_text=None):
    hindi_text = str(hindi_text).strip()

    if not hindi_text:
        return

    if english_text is None:
        english_text = hindi_text

    print("JARVIS SPEAKING:", hindi_text)

    # English text on frontend
    try:
        eel.DisplayMessage(english_text)
    except:
        pass

    # Hindi voice
    print("TTS Language: Hindi")
    asyncio.run(_speak(hindi_text, VOICE_HI))

def takecommand():
    r = sr.Recognizer()

    r.dynamic_energy_threshold = True
    r.pause_threshold = 0.6
    r.non_speaking_duration = 0.3

    with sr.Microphone() as source:
        print("I am Listening...")

        r.adjust_for_ambient_noise(source, duration=0.3)

        try:
            audio = r.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

            print("Recognizing...")

            # First try Hinglish / Hindi
            try:
                query = r.recognize_google(
                    audio,
                    language="hi-IN"
                )

                print("User said:", query)
                return query.lower()

            except sr.UnknownValueError:

                # If Hindi recognition fails, try English
                query = r.recognize_google(
                    audio,
                    language="en-IN"
                )

                print("User said:", query)
                return query.lower()

        except sr.WaitTimeoutError:
            print("Listening timeout.")
            return ""

        except sr.UnknownValueError:
            print("Could not understand.")
            return ""

        except sr.RequestError as e:
            print("Speech recognition error:", e)
            return ""
#text1 = takecommand()

#speak(text1)

@eel.expose
def takeAllCommands(message=None):
    if message is None:
        query = takecommand()

        if not query:
            speak("I didn't hear anything.")
            return

        print("Voice Command:", query)

        # Show spoken command on main UI
        eel.senderText(query)
        
        # Save spoken command in chat sidebar
        try:
            eel.userChatMessage(query)
        except Exception as e:
            print("Voice sidebar error:", e)

    else:
        query = message
        print("Message received:", query)
        eel.senderText(query)

    try:
        query = str(query).lower().strip()

        if not query:
            speak("No command was given.")
            return

        # ==================================================
        # DESKTOP CONTROL
        # ==================================================

        # CHROME
        if (
            "open chrome" in query
            or "google chrome" in query
            or "ओपन क्रोम" in query
            or "क्रोम खोलो" in query
            or "क्रोम खोल" in query
        ):
            result = open_application("chrome")
            speak(result)

        # NOTEPAD
        elif (
            "open notepad" in query
            or "ओपन नोटपैड" in query
            or "नोटपैड खोलो" in query
        ):
            result = open_application("notepad")
            speak(result)

        # CALCULATOR
        elif (
            "open calculator" in query
            or "open calc" in query
            or "ओपन कैलकुलेटर" in query
            or "कैलकुलेटर खोलो" in query
        ):
            result = open_application("calculator")
            speak(result)

        # SHUTDOWN
        elif (
            "shutdown" in query
            or "shut down" in query
            or "कंप्यूटर बंद करो" in query
            or "कंप्यूटर बंद" in query
        ):
            speak("Okay sir, shutting down the computer in 5 seconds.")
            shutdown_pc()

        # RESTART
        elif (
            "restart" in query
            or "reboot" in query
            or "कंप्यूटर रीस्टार्ट करो" in query
            or "रीस्टार्ट करो" in query
        ):
            speak("Okay sir, restarting the computer in 5 seconds.")
            restart_pc()

        # LOCK
        elif (
            "lock computer" in query
            or "lock pc" in query
            or "lock my computer" in query
            or "lock the computer" in query
            or "कंप्यूटर लॉक करो" in query
            or "कंप्यूटर को लॉक करो" in query
            or "कंप्यूटर लॉक" in query
            or "कंप्यूटर को लॉक" in query
            or "पीसी लॉक करो" in query
            or "पीसी को लॉक करो" in query
            or "पीसी लॉक" in query
        ):
            print("🔒 LOCK COMMAND DETECTED")
            result = lock_pc()
            print("Lock result:", result)
            speak(result)

        # SCREENSHOT
        elif (
            "take screenshot" in query
            or "screenshot" in query
            or "स्क्रीनशॉट" in query
        ):
            result = take_screenshot()
            speak(result)

        # ==================================================
        # OPEN COMMAND
        # ==================================================

        elif (
            "open" in query
            or "ओपन" in query
            or "खोलो" in query
        ):
            from Backend.feature import openCommand
            openCommand(query)

        # ==================================================
        # VIDEO CALL
        # ==================================================
        
        elif (
            "video call" in query
            or "वीडियो कॉल" in query
            or "वीडियो काल" in query
        ):
            from Backend.feature import findContact, whatsApp
        
            Phone, name = findContact(query)
        
            if Phone != 0:
                speak(f"{name} को वीडियो कॉल कर रहा हूँ।")
                whatsApp(
                    Phone,
                    "",
                    "video call",
                    name
                )
        # ==================================================
        # NORMAL CALL
        # ==================================================
        
        elif (
            "call" in query
            or "कॉल" in query
            or "काल" in query
            or "फोन करो" in query
        ):
            from Backend.feature import findContact, whatsApp
        
            Phone, name = findContact(query)
        
            if Phone != 0:
                speak(f"{name} को कॉल कर रहा हूँ।")
                whatsApp(
                    Phone,
                    "",
                    "call",
                    name
                )

        # ==================================================
        # MESSAGE
        # ==================================================

        elif (
            "send message" in query
            or "send a message" in query
            or "message" in query
            or "मैसेज भेजो" in query
            or "मैसेज भेज" in query
            or "सेंड मैसेज" in query
            or "सेंड मैसेज भेजो" in query
            or "मैसेज" in query
        ):
            from Backend.feature import findContact, whatsApp
        
            print("Searching contact for message:", query)
        
            Phone, name = findContact(query)
        
            if Phone != 0:
        
                speak(f"जी सर, {name} को क्या मैसेज भेजना है?")
        
                message_text = takecommand()
        
                if not message_text:
                    speak("मुझे मैसेज सुनाई नहीं दिया।")
                    return
        
                print("Message:", message_text)
        
                whatsApp(
                    Phone,
                    message_text,
                    "message",
                    name
                )
        
            else:
                speak("यह कॉन्टैक्ट आपकी कॉन्टैक्ट लिस्ट में मौजूद नहीं है।")

        # ==================================================
        # YOUTUBE
        # ==================================================

        elif (
            "youtube" in query
            or "यूट्यूब" in query
            or "यूट्यूब पर" in query
            or "यूट्यूब में" in query
        ):
            from Backend.feature import PlayYoutube
            PlayYoutube(query)

        elif (
            "weather" in query
            or "temperature" in query
            or "temp" in query
            or "मौसम" in query
            or "तापमान" in query
        ):
            from Backend.weather import get_weather_text
            result = get_weather_text()
            speak(result)

         # ==================================================
        # TIME
        # ==================================================

        elif (
            "what time" in query
            or "time is it" in query
            or "current time" in query
            or "समय क्या हुआ" in query
            or "अभी कितने बजे" in query
            or "कितने बजे हैं" in query
        ):
            from Backend.system_info import get_time

            current_time = get_time()
            speak(f"Sir, the current time is {current_time}.")

        # ==================================================
        # DATE
        # ==================================================

        elif (
            "what is the date" in query
            or "today's date" in query
            or "todays date" in query
            or "current date" in query
            or "आज की तारीख" in query
            or "आज तारीख" in query
            or "तारीख क्या है" in query
        ):
            from Backend.system_info import get_date

            current_date = get_date()
            speak(f"Sir, today's date is {current_date}.")

        # ==================================================
        # DAY
        # ==================================================

        elif (
            "what day is today" in query
            or "which day is today" in query
            or "आज कौन सा दिन" in query
        ):
            from Backend.system_info import get_day

            current_day = get_day()
            speak(f"Sir, today is {current_day}.")

        # ==================================================
        # LOCATION
        # ==================================================
        
        elif (
            "where am i" in query
            or "my location" in query
            or "where are we" in query
            or "मैं कहाँ हूँ" in query
            or "मैं कहां हूं" in query
            or "मैं कहाँ हूं" in query
            or "मैं कहां हूँ" in query
            or "मेरी लोकेशन" in query
            or "मेरी जगह" in query
            or "लोकेशन क्या है" in query
        ):
            from Backend.system_info import get_location
        
            location = get_location()
            speak(f"Sir, your location is {location}.")

        # ==================================================
        # WEATHER / TEMPERATURE
        # ==================================================

        elif (
            "weather" in query
            or "temperature" in query
            or "temp" in query
            or "मौसम" in query
            or "तापमान" in query
        ):
            from Backend.weather import get_weather_text

            result = get_weather_text()
            speak(result)

        # ==================================================
        # CHATBOT
        # ==================================================

        else:
            from Backend.feature import chatBot
            chatBot(query)

    except Exception as e:
        print("ERROR:", e)
        speak("Sorry, something went wrong.")

    eel.ShowHood()