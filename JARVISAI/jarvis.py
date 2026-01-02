# -------- Jarvis AI Assistant (Upgraded + Your Request Integrated) -------- 
import google.generativeai as genai
import pyttsx3
import speech_recognition as sr
import tkinter as tk
from tkinter import scrolledtext
import threading
import os
import webbrowser
import datetime
import random
import re
import wikipedia
import smtplib
import pyautogui
import time
import pyjokes
import requests
import subprocess

GENAI_API_KEY = "API KEY HERE"  
genai.configure(api_key=GENAI_API_KEY)

output_dir = "D:\\JarvisAI\\JARVISAI"
music_dir = "C:\\Users\\shivs\\Music" 

email_user = "pradeepshirvi72@gmail.com" 
email_password = "Pradeep#@786" 

sites = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "github": "https://github.com",
    "stackoverflow": "https://stackoverflow.com",
}

# ----------------- TTS Engine -----------------
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 170)

def speak(text):
    conversation_area.insert(tk.END, f"Jarvis: {text}\n")
    conversation_area.see(tk.END)
    engine.say(text)
    engine.runAndWait()

# ----------------- Listen Function -----------------
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        conversation_area.insert(tk.END, "Listening...\n")
        conversation_area.see(tk.END)
        recognizer.pause_threshold = 1
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            query = recognizer.recognize_google(audio, language='en-in').lower()
            conversation_area.insert(tk.END, f"You: {query}\n\n")
            conversation_area.see(tk.END)
            return query
        except:
            speak("Sorry, I couldn't hear you properly.")
            return "none"

# ----------------- Gemini Response -----------------
def generate_response(prompt):
    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                max_output_tokens=300,
                temperature=0.6,
            )
        )
        return response.text.strip()
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "Sorry, I encountered an error contacting the AI."
# ----------------- Helper Functions -----------------
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def wish_me():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning Sir!")
    elif 12 <= hour < 18:
        speak("Good Afternoon Sir!")
    else:
        speak("Good Evening Sir!")
    speak("I am Jarvis. Your personal assistant. How can I help you today?")

def search_wikipedia(query):
    try:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "").strip()
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(results)
    except wikipedia.exceptions.PageError:
        speak(f"Sorry, I couldn't find a page for '{query}' on Wikipedia.")
    except wikipedia.exceptions.DisambiguationError as e:
        speak(f"There are multiple pages for '{query}'. Could you be more specific? {e.options[:5]}")
    except Exception:
        speak("Sorry, I encountered an error while searching Wikipedia.")

def open_app(name):
    apps = {
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
    }
    normalized_name = name.lower()
    if normalized_name in apps:
        subprocess.Popen(apps[normalized_name])
        speak(f"Opening {name}")
    else:
        speak("Application not found.")

def send_email(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_password)
        server.sendmail(email_user, to, content)
        server.quit()
        speak("Email has been sent successfully!")
    except Exception as e:
        speak(f"Sorry, I am unable to send the email. Error: {e}")

def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)

def play_music():
    try:
        songs = os.listdir(music_dir)
        if songs:
            chosen_song = random.choice(songs)
            os.startfile(os.path.join(music_dir, chosen_song))
            speak(f"Playing {chosen_song} for you.")
        else:
            speak("No music found in the specified directory.")
    except FileNotFoundError:
        speak("The music directory was not found.")
    except Exception as e:
        speak(f"An error occurred while trying to play music: {e}")

def take_screenshot():
    try:
        image = pyautogui.screenshot()
        filename = f"screenshot_{random.randint(1000,9999)}.png"
        filepath = os.path.join(output_dir, filename)
        image.save(filepath)
        speak(f"Screenshot saved successfully to {filepath}")
    except Exception as e:
        speak(f"An error occurred while taking a screenshot: {e}")

def get_weather(city):
    try:
        api_key = "YOUR_OPENWEATHERMAP_API_KEY"  # <<< Get from OpenWeatherMap
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        weather = requests.get(base_url).json()
        if weather["cod"] != "404":
            temp = weather["main"]["temp"]
            description = weather["weather"][0]["description"]
            speak(f"The temperature in {city} is {temp} degrees Celsius with {description}")
        else:
            speak("City not found.")
    except requests.exceptions.RequestException as e:
        speak(f"Error connecting to the weather service: {e}")
    except Exception as e:
        speak(f"An error occurred while fetching weather information: {e}")

def set_alarm(seconds):
    try:
        seconds = int(seconds)
        if seconds > 0:
            speak(f"Setting alarm for {seconds} seconds.")
            threading.Thread(target=alarm_timer, args=(seconds,)).start()
        else:
            speak("Please provide a valid positive number of seconds for the alarm.")
    except ValueError:
        speak("Invalid input for alarm duration. Please specify the time in seconds.")

def alarm_timer(seconds):
    time.sleep(seconds)
    speak("Time's up!")

def calculate_expression(expression):
    try:
        # Remove any potentially dangerous functions from the expression
        safe_expression = expression.replace("os.", "").replace("subprocess.", "").replace("import", "")
        result = eval(safe_expression)
        speak(f"The result is {result}")
    except Exception as e:
        speak(f"Sorry, I couldn't calculate that. Error: {e}")

# ----------------- Main Jarvis Logic -----------------
def handle_conversation():
    global stop_conversation
    wish_me()

    while not stop_conversation:
        query = listen()
        if query == "none":
            continue

        command_handled = False

        # 1. Exit command
        if "bye" in query or "goodbye" in query or "jarvis quit" in query:
            speak("Goodbye! Have a great day!")
            stop_conversation = True
            break

        # 2. Time and date commands
        elif "the time" in query:
            now = datetime.datetime.now()
            time_str = now.strftime("%I:%M %p")
            speak(f"The current time is {time_str}")
            command_handled = True

        elif "the date" in query or "what's today's date" in query:
            today = datetime.date.today()
            date_str = today.strftime("%B %d, %Y")
            speak(f"Today's date is {date_str}")
            command_handled = True

        # 3. Website opening commands
        else:
            for site, url in sites.items():
                if f"open {site}" in query:
                    speak(f"Opening {site}...")
                    try:
                        webbrowser.open(url)
                        command_handled = True
                        break
                    except Exception as e:
                        speak(f"Sorry, I couldn't open {site}. Error: {e}")
                        command_handled = True
                        break

        # 4. Create file about topic using AI
        if not command_handled and ("create file about" in query or "save response for" in query):
            topic = query.replace("create file about", "").replace("save response for", "").strip()
            if topic:
                speak(f"Okay, generating content to create a file about {topic}...")
                ai_content = generate_response(f"Write a short text about: {topic}")
                if "Sorry, I encountered an error" not in ai_content:
                    try:
                        os.makedirs(output_dir, exist_ok=True)
                        filename = sanitize_filename(topic) + ".txt"
                        filepath = os.path.join(output_dir, filename)
                        with open(filepath, "w", encoding='utf-8') as f:
                            f.write(f"Query: {topic}\n\nResponse:\n{ai_content}")
                        speak(f"Content saved successfully to {filepath}")
                    except Exception as e:
                        speak(f"Sorry, I failed to save the file. Error: {e}")
                else:
                    speak(ai_content)
                command_handled = True
            else:
                speak("Please specify what you want me to create a file about.")
                command_handled = True

        # 5. Wikipedia Search
        elif not command_handled and "search wikipedia for" in query:
            search_term = query.replace("search wikipedia for", "").strip()
            search_wikipedia(search_term)
            command_handled = True

        elif not command_handled and "what is" in query:
            search_term = query.replace("what is", "").strip()
            search_wikipedia(search_term)
            command_handled = True

        elif not command_handled and "who is" in query:
            search_term = query.replace("who is", "").strip()
            search_wikipedia(search_term)
            command_handled = True

        # 6. Open Application
        elif not command_handled and "open" in query:
            app_name = query.replace("open", "").strip()
            open_app(app_name)
            command_handled = True

        # 7. Send Email
        elif not command_handled and "send email to" in query:
            try:
                parts = query.split("to")
                if len(parts) == 2:
                    recipient = parts[1].split("saying")[0].strip()
                    content_parts = query.split("saying")
                    if len(content_parts) > 1:
                        email_content = content_parts[1].strip()
                        speak(f"Sending email to {recipient} with content: {email_content}")
                        send_email(recipient, email_content)
                        command_handled = True
                    else:
                        speak("What should I say in the email?")
                        command_handled = True
                else:
                    speak("Please specify the recipient and the content of the email.")
                    command_handled = True
            except Exception as e:
                speak(f"Sorry, I encountered an error processing the email command: {e}")
                command_handled = True

        # 8. Tell a Joke
        elif not command_handled and "tell me a joke" in query:
            tell_joke()
            command_handled = True

        # 9. Play Music
        elif not command_handled and "play music" in query:
            play_music()
            command_handled = True

        # 10. Take a Screenshot
        elif not command_handled and "take a screenshot" in query:
            take_screenshot()
            command_handled = True

        # 11. Get Weather
        elif not command_handled and "what's the weather in" in query:
            city = query.replace("what's the weather in", "").strip()
            get_weather(city)
            command_handled = True

        elif not command_handled and "weather in" in query:
            city = query.replace("weather in", "").strip()
            get_weather(city)
            command_handled = True

        # 12. Set an Alarm
        elif not command_handled and "set an alarm for" in query:
            duration_str = query.replace("set an alarm for", "").strip()
            # Try to extract a number of seconds
            match = re.search(r'(\d+)\s*(seconds?|minutes?|hours?)', duration_str)
            if match:
                value = int(match.group(1))
                unit = match.group(2).lower()
                if "second" in unit:
                    set_alarm(value)
                    command_handled = True
                elif "minute" in unit:
                    set_alarm(value * 60)
                    command_handled = True
                elif "hour" in unit:
                    set_alarm(value * 3600)
                    command_handled = True
                else:
                    speak("Please specify the alarm duration in seconds, minutes, or hours.")
                    command_handled = True
            else:
                # Try to see if just a number of seconds was given
                match_seconds = re.search(r'(\d+)', duration_str)
                if match_seconds:
                    set_alarm(match_seconds.group(1))
                    command_handled = True
                else:
                    speak("Please specify the alarm duration.")
                    command_handled = True

        # 13. Calculate Expression
        elif not command_handled and "calculate" in query:
            expression = query.replace("calculate", "").strip()
            calculate_expression(expression)
            command_handled = True

        # 14. Default Gemini Chat
        if not command_handled:
            response = generate_response(query)
            speak(response)

# ----------------- GUI -----------------
root = tk.Tk()
root.title("JARVIS (Upgraded)")
root.geometry("800x600")
root.config(bg="#0D1117")

FONT = ("Segoe UI", 12)
HEADER_FONT = ("Segoe UI", 20, "bold")
TEXT_COLOR = "#E6EDF3"
BUTTON_BG = "#21262D"
BUTTON_HOVER_BG = "#238636"
BUTTON_FG = "#F0F6FC"

header = tk.Label(root, text="🧠 JARVIS - AI Assistant", font=HEADER_FONT, bg="#0D1117", fg="#58A6FF")
header.pack(pady=10)

conversation_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=25,
    font=FONT, bg="#161B22", fg=TEXT_COLOR, insertbackground=TEXT_COLOR, relief=tk.FLAT)
conversation_area.pack(padx=20, pady=10, expand=True, fill=tk.BOTH)

button_frame = tk.Frame(root, bg="#0D1117")
button_frame.pack()

def on_enter(e):
    e.widget['background'] = BUTTON_HOVER_BG

def on_leave(e):
    e.widget['background'] = BUTTON_BG

def start_conversation():
    """Start the conversation thread."""
    global conversation_thread, stop_conversation
    if conversation_thread is not None and conversation_thread.is_alive():
        conversation_area.insert(tk.END, "Jarvis: Conversation already running.\n")
        return

    stop_conversation = False
    conversation_area.delete('1.0', tk.END)
    conversation_area.insert(tk.END, "Starting Jarvis...\n")
    conversation_thread = threading.Thread(target=handle_conversation)
    conversation_thread.daemon = True
    conversation_thread.start()

def end_conversation():
    global stop_conversation
    speak("Goodbye! Have a great day!")
    stop_conversation = True

    root.quit()

start_button = tk.Button(button_frame, text="🎙️ Start Listening", font=FONT, bg=BUTTON_BG, fg=BUTTON_FG,
    activebackground=BUTTON_HOVER_BG, activeforeground=TEXT_COLOR, command=start_conversation)
start_button.pack(side=tk.LEFT, padx=10)
start_button.bind("<Enter>", on_enter)
start_button.bind("<Leave>", on_leave)

stop_button = tk.Button(button_frame, text="❌ Stop & Exit", font=FONT, bg=BUTTON_BG, fg=BUTTON_FG,
    activebackground=BUTTON_HOVER_BG, activeforeground=TEXT_COLOR, command=end_conversation)
stop_button.pack(side=tk.LEFT, padx=10)
stop_button.bind("<Enter>", on_enter)
stop_button.bind("<Leave>", on_leave)

def on_closing():
    global stop_conversation
    speak("Goodbye! Have a great day!")
    stop_conversation = True
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
conversation_thread = None
stop_conversation = False

# ----------------- Main Loop -----------------
root.mainloop()