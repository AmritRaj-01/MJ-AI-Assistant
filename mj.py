import speech_recognition as sr
import pyttsx3
import webbrowser
import subprocess
import time
from google import genai

#  YOUR API KEY 
API_KEY = "Your API_KEY"


# Initialize Gemini
try:
    client = genai.Client(api_key=API_KEY)
    GEMINI_AVAILABLE = True
    print("✅ AI features enabled! (Gemini is ready)")
except Exception as e:
    GEMINI_AVAILABLE = False
    print(f"❌ AI features disabled: {e}")

engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text):
    print("MJ:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎤 Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
        except:
            return ""
    
    try:
        text = r.recognize_google(audio).lower()
        print(f"📝 You said: {text}")
        return text
    except:
        return ""

def ask_gemini(prompt):
    if not GEMINI_AVAILABLE:
        return "AI features disabled. Please check your API key."
    try:
        time.sleep(2)  # Delay to avoid rate limiting
        response = client.models.generate_content(
            model="gemini-1.5-flash",  # Changed model
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Sorry, I'm busy right now. Please try again in a moment."

def open_website(url, name):
    speak(f"Opening {name}")
    webbrowser.open(url)

# Websites database
websites = {
    "youtube": "https://youtube.com",
    "whatsapp": "https://web.whatsapp.com",
    "github": "https://github.com",
    "leetcode": "https://leetcode.com",
    "chatgpt": "https://chat.openai.com",
    "chat gpt": "https://chat.openai.com",
    "instagram": "https://instagram.com",
    "facebook": "https://facebook.com",
    "gmail": "https://gmail.com",
    "google": "https://google.com",
}

speak("MJ is online with AI features. Say MJ then your command.")

while True:
    command = listen()
    
    if not command:
        continue
    
    if "mj" in command or "em jay" in command:
        speak("Yes?")
        task = listen()
        
        if not task:
            speak("Say again?")
            continue
        
        print(f"Task: {task}")
        
        # ===== WEBSITES =====
        opened = False
        for name, url in websites.items():
            if name in task:
                open_website(url, name.title())
                opened = True
                break
        
        if opened:
            pass
        
        # ===== GOOGLE SEARCH =====
        elif "search" in task:
            query = task.replace("search", "").strip()
            if query:
                speak(f"Searching Google for {query}")
                webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
            else:
                speak("What should I search?")
                query = listen()
                if query:
                    webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
        
        # ===== APPLICATIONS =====
        elif "notepad" in task:
            speak("Opening Notepad")
            subprocess.run(["notepad.exe"])
        
        elif "calculator" in task:
            speak("Opening Calculator")
            subprocess.run(["calc.exe"])
        
        # ===== TIME & DATE =====
        elif "time" in task:
            from datetime import datetime
            now = datetime.now().strftime("%I:%M %p")
            speak(f"The time is {now}")
        
        elif "date" in task:
            from datetime import datetime
            today = datetime.now().strftime("%B %d, %Y")
            speak(f"Today is {today}")
        
        # ===== EXIT =====
        elif "exit" in task or "quit" in task or "bye" in task:
            speak("Goodbye!")
            break
        
        # ===== 🤖 AI CHAT =====
        else:
            if GEMINI_AVAILABLE:
                speak("Let me think... 🤔")
                reply = ask_gemini(task)
                speak(reply)
            else:
                speak("I don't know that command.")