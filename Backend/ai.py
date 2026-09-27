import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai


# =========================
# JARVIS PROJECT ROOT
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


# =========================
# GEMINI API KEY
# =========================

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        f"GEMINI_API_KEY is not set.\n"
        f"Make sure this file exists:\n{ENV_FILE}"
    )


# =========================
# GEMINI CLIENT
# =========================

client = genai.Client(api_key=API_KEY)


# =========================
# ASK AI
# =========================

def ask_ai(prompt):

    jarvis_prompt = f"""
You are JARVIS, a personal AI assistant.

User said:
{prompt}

Rules:
1. Reply in the same language as the user.
2. If the user speaks Hindi, reply completely in Hindi.
3. If the user speaks English, reply completely in English.
4. If the user uses Hinglish, you may reply in natural Hinglish.
5. Keep the answer conversational and concise.
6. Do NOT use Markdown.
7. Do NOT use **, ##, ###, bullet symbols, or special formatting.
8. Do not write headings unless they are necessary.
9. Give a natural answer suitable for speaking aloud.
"""

    for attempt in range(3):
        try:
            print(f"Gemini attempt {attempt + 1}/3...")

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=jarvis_prompt
            )

            if response and response.text:
                return response.text.strip()

            return ""

        except Exception as e:
            error = str(e)
            print("Gemini Error:", error)

            if "503" in error or "UNAVAILABLE" in error:
                if attempt < 2:
                    wait_time = 2 ** attempt
                    print(
                        f"Gemini is busy. Retrying in {wait_time} seconds..."
                    )
                    time.sleep(wait_time)
                else:
                    print("Gemini unavailable after 3 attempts.")
            else:
                break

    return "माफ कीजिए सर, मेरा AI ब्रेन अभी उपलब्ध नहीं है।"