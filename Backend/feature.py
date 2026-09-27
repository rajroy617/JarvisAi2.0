#import playsound as playsound
#import eel 
#
#@eel.expose
#
#def playAssistantSound():
#    music_dir = "Frontend\\assets\\audio\\sound.mp3"
#    playsound.playsound(music_dir)

import os
import re
from shlex import quote
import struct
import time
import webbrowser

import urllib
from Backend.command import speak
from Backend.helper import extract_yt_term, remove_words
import eel 
import pywhatkit as kit
import pygame
from Backend.config import ASSISTANT_NAME
import sqlite3
import pvporcupine
import pyaudio
import subprocess
import pyautogui
from Backend.ai import ask_ai 
from urllib.parse import quote

conn = sqlite3.connect("jarvis.db")
cursor = conn.cursor()

pygame.mixer.init()
@eel.expose
def play_assistant_sound():
    sound_file = os.path.join(
        "Frontend",
        "assets",
        "audio",
        "sound.mp3"
    )

    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

        print("Assistant sound playing...")

    except Exception as e:
        print("Assistant sound error:", e)

def openCommand(query):
    query = query.lower().strip()

    # Remove assistant name
    query = query.replace(ASSISTANT_NAME.lower(), "")

    # Remove English/Hindi open words
    open_words = [
        "open",
        "ओपन",
        "खोलो",
        "खोल",
    ]

    for word in open_words:
        query = query.replace(word, "")

    app_name = query.strip()

    if not app_name:
        speak("What should I open?")
        return

    try:
        # Check database applications
        cursor.execute(
            "SELECT path FROM sys_command WHERE LOWER(name) = ?",
            (app_name,)
        )

        results = cursor.fetchall()

        if results:
            speak("Opening " + app_name)
            os.startfile(results[0][0])
            return

        # Check web commands
        cursor.execute(
            "SELECT url FROM web_command WHERE LOWER(name) = ?",
            (app_name,)
        )

        results = cursor.fetchall()

        if results:
            speak("Opening " + app_name)
            webbrowser.open(results[0][0])
            return

        # Windows fallback
        speak("Opening " + app_name)

        try:
            os.system(f'start "" "{app_name}"')
        except Exception:
            speak("Sorry sir, I couldn't find that application.")

    except Exception as e:
        print("openCommand ERROR:", e)
        speak("Something went wrong while opening it.")

def PlayYoutube(query):
    try:
        query = str(query).lower().strip()

        # Remove common YouTube command words
        remove_list = [
            "play",
            "on youtube",
            "youtube",
            "search youtube",
            "open youtube",
            "यूट्यूब",
            "यूट्यूब पर",
            "यूट्यूब में",
            "चलाओ",
            "चलाओ",
            "चलाना",
            "बजाओ",
            "गाना",
            "वीडियो",
            "पर",
            "में",
        ]

        search_term = query

        for word in remove_list:
            search_term = search_term.replace(word, "")

        search_term = search_term.strip()

        if not search_term:
            speak(
                "सर, YouTube पर क्या चलाना है?",
                "Sir, what should I play on YouTube?"
            )
            return

        print("YouTube Search:", search_term)

        speak(
            f"{search_term} YouTube पर चला रहा हूँ।",
            f"Playing {search_term} on YouTube."
        )

        # Open YouTube search directly
        youtube_url = (
            "https://www.youtube.com/results?search_query="
            + quote(search_term)
        )

        webbrowser.open(youtube_url)

        # Wait for page to load
        time.sleep(5)

        # Press first video
        pyautogui.press("tab")
        time.sleep(1)
        pyautogui.press("enter")

    except Exception as e:
        print("YouTube ERROR:", e)

        speak(
            "माफ कीजिए सर, YouTube चलाने में समस्या आ गई।",
            "Sorry sir, I couldn't play YouTube."
        )

def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

def findContact(query):

    words_to_remove = [
        # Assistant name
        ASSISTANT_NAME,

        # English
        "make",
        "a",
        "to",
        "phone",
        "call",
        "send",
        "message",
        "whatsapp",
        "wahtsapp",
        "video",
        "voice",
        "contact",

        # Hindi
        "कॉल",
        "काल",
        "फोन",
        "करो",
        "कर",
        "को",
        "से",
        "वीडियो",
        "वॉइस",
        "मैसेज",
        "मैसेज भेजो",
        "मैसेज भेज",
        "सेंड",
        "व्हाट्सएप",
        "व्हाट्सऐप",
        "कॉन्टैक्ट"
    ]

    try:
        query = str(query).lower().strip()

        print("Original contact query:", query)

        # --------------------------------------------------
        # Remove command words
        # --------------------------------------------------

        query = remove_words(query, words_to_remove)
        query = query.strip()

        print("Cleaned contact query:", query)

        if not query:
            speak("Please tell me the contact name.")
            return 0, 0

        # --------------------------------------------------
        # Hindi speech aliases
        # --------------------------------------------------
        # Speech recognition may return Hindi pronunciation
        # while the database contains English names.

        contact_aliases = {
            "प्रिंस": "prince",
            "प्रिन्स": "prince",
            "राज": "raj",
            "राहुल": "rahul",
            "अमन": "aman",
            "अंकित": "ankit",
            "रोहित": "rohit",
            "सुमित": "sumit",
            "आकाश": "akash",
            "अभिषेक": "abhishek",
            "विवेक": "vivek",
            "सोनू": "sonu",
            "मोनू": "monu",
            "पापा": "papa",
        }

        search_name = contact_aliases.get(query, query)

        print("Searching contact:", search_name)

        # --------------------------------------------------
        # Search SQLite
        # --------------------------------------------------

        cursor.execute(
            """
            SELECT name, Phone
            FROM contacts
            WHERE LOWER(name) LIKE ?
            LIMIT 1
            """,
            ("%" + search_name.lower() + "%",)
        )

        result = cursor.fetchone()

        if not result:
            print("Contact not found:", search_name)
            speak(f"{query} नाम का कॉन्टैक्ट नहीं मिला।")
            return 0, 0

        contact_name = str(result[0])
        mobile_number_str = str(result[1])

        # --------------------------------------------------
        # Clean phone number
        # --------------------------------------------------

        mobile_number_str = (
            mobile_number_str
            .replace(" ", "")
            .replace("-", "")
            .replace("(", "")
            .replace(")", "")
        )

        if not mobile_number_str.startswith("+91"):
            mobile_number_str = "+91" + mobile_number_str

        print("Phone:", mobile_number_str)
        print("Name:", contact_name)

        return mobile_number_str, contact_name

    except Exception as e:
        print("findContact ERROR:", e)
        speak("I couldn't find that contact.")
        return 0, 0

def whatsApp(Phone, message, flag, name):

    try:
        # Clean phone number
        Phone = str(Phone).replace(" ", "").replace("-", "")
        Phone = Phone.replace("(", "").replace(")", "")

        if flag == "message":

            print(f"Sending WhatsApp message to {name}")
            print(f"Phone: {Phone}")
            print(f"Message: {message}")

            # Encode message
            encoded_message = urllib.parse.quote(str(message))

            # WhatsApp Web URL
            whatsapp_url = (
                f"https://web.whatsapp.com/send"
                f"?phone={Phone}"
                f"&text={encoded_message}"
            )

            print("Opening:", whatsapp_url)

            # Open browser
            subprocess.Popen(
                f'start "" "{whatsapp_url}"',
                shell=True
            )

            # Give WhatsApp Web time to load
            print("Waiting for WhatsApp Web...")
            time.sleep(10)

            # Make sure browser is active
            pyautogui.hotkey("alt", "tab")
            time.sleep(2)

            # Send message
            pyautogui.press("enter")

            time.sleep(3)

            print(f"Message sent successfully to {name}")
            speak(f"Message sent successfully to {name}")

        elif flag == "video call":

            Phone = str(Phone).replace(" ", "").replace("-", "")
            Phone = Phone.replace("(", "").replace(")", "")
        
            print(f"Starting video call with {name}")
        
            whatsapp_url = f"https://web.whatsapp.com/send?phone={Phone}"
        
            print("WhatsApp URL:", whatsapp_url)
        
            subprocess.Popen(
                f'start "" "{whatsapp_url}"',
                shell=True
            )
        
            # Wait for WhatsApp chat
            time.sleep(10)
        
            # Make sure Chrome/WhatsApp is active
            pyautogui.click(800, 45)
            time.sleep(1)
        
            print("Clicking VIDEO CALL button...")
        
            # VIDEO CAMERA BUTTON
            pyautogui.moveTo(1152, 102, duration=0.5)
            time.sleep(1)
            pyautogui.click(1152, 102)
        
            time.sleep(3)
        
            print(f"Video call button clicked for {name}")
            speak(f"Starting video call with {name}")


        elif flag == "call":

            Phone = str(Phone).replace(" ", "").replace("-", "")
            Phone = Phone.replace("(", "").replace(")", "")
        
            print(f"Calling {name}")
        
            whatsapp_url = f"https://web.whatsapp.com/send?phone={Phone}"
        
            print("WhatsApp URL:", whatsapp_url)
        
            subprocess.Popen(
                f'start "" "{whatsapp_url}"',
                shell=True
            )
        
            # Wait for WhatsApp chat
            time.sleep(10)
        
            # Make sure Chrome/WhatsApp is active
            pyautogui.click(800, 45)
            time.sleep(1)
        
            print("Clicking VOICE CALL button...")
        
            # PHONE BUTTON
            pyautogui.moveTo(1209, 102, duration=0.5)
            time.sleep(1)
            pyautogui.click(1209, 102)
        
            time.sleep(3)
        
            print(f"Voice call button clicked for {name}")
            speak(f"Calling {name}")
        else:
            print("Invalid WhatsApp flag:", flag)

    except Exception as e:
        print("WhatsApp ERROR:", e)
        speak("Sorry sir, I couldn't send the WhatsApp message.")


def chatBot(query):
    try:
        user_input = query.strip()

        if not user_input:
            return "Please tell me something."

        print("Sending to Gemini:", user_input)

        response = ask_ai(user_input)

        if not response:
            response = "Sorry sir, I didn't get a response from my AI brain."

        response = str(response).strip()

        print("Gemini:", response)

        # ==============================================
        # SEND GEMINI RESPONSE TO CHAT SIDEBAR
        # ==============================================

        try:
            eel.jarvisResponse(response)
        except Exception as e:
            print("Sidebar response error:", e)

        # ==============================================
        # SPEAK RESPONSE
        # ==============================================

        speak(response)

        return response

    except Exception as e:
        print("Gemini ChatBot ERROR:", e)

        error_message = "Sorry sir, I am having trouble connecting to my AI brain."

        try:
            eel.jarvisResponse(error_message)
        except Exception as sidebar_error:
            print("Sidebar response error:", sidebar_error)

        speak(error_message)

        return "Gemini connection error."