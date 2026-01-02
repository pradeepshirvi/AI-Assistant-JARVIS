import google.generativeai as genai #pip install google-generativeai
import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install SpeechRecognition
import tkinter as tk #pip install tk
from tkinter import scrolledtext
import threading
import os # Added for file operations
import webbrowser # Added for opening websites
import datetime # Added for getting time
import random # Added for random filenames
import re # Added for sanitizing filenames


GENAI_API_KEY = "AIzaSyDAKrhTYGzatmdxvgT3EGAUEin91QboKLk"

if not GENAI_API_KEY:
    print("Error: Gemini API Key not found. Please set the environment variable.")
    # Optionally exit or disable AI features
    # exit()

try:
    genai.configure(api_key=GENAI_API_KEY)
except Exception as e:
    print(f"Error configuring Generative AI: {e}")
    # Optionally exit or disable AI features
    # exit()


# Text-to-Speech engine
try:
    engine = pyttsx3.init('sapi5')
    # Set properties if needed (optional)
    engine.setProperty('voice', engine.getProperty('voices')[0].id)
    # engine.setProperty('rate', 150) # Example rate adjustment
except Exception as e:
    print(f"Error initializing TTS engine: {e}")
    # Fallback or exit if TTS is crucial
    engine = None

def speak(text):
    """Safely speak text if TTS engine is available."""
    if engine:
        try:
            conversation_area.insert(tk.END, f"Jarvis: {text}\n")
            conversation_area.see(tk.END) # Scroll to the end
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"Error during speech: {e}")
    else:
        print(f"Jarvis (TTS disabled): {text}")
        conversation_area.insert(tk.END, f"Jarvis (TTS disabled): {text}\n")
        conversation_area.see(tk.END)


def listen_to_command():
    """Speech to Text with improved error display."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # Update GUI directly from the main thread if possible, or use queue
        # For simplicity here, we update directly, but queue is safer for complex GUIs
        conversation_area.insert(tk.END, "Listening...\n")
        conversation_area.see(tk.END)
        recognizer.pause_threshold = 1
        recognizer.adjust_for_ambient_noise(source, duration=0.5) # Adjust faster
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            query = recognizer.recognize_google(audio, language='en-in').lower()
            conversation_area.insert(tk.END, f"You: {query}\n\n")
            conversation_area.see(tk.END)
            return query
        except sr.WaitTimeoutError:
            conversation_area.insert(tk.END, "Jarvis: No speech detected within timeout.\n")
            conversation_area.see(tk.END)
            speak("Didn't hear anything.") # Avoid speaking errors constantly
            print("Timeout waiting for speech.")
            return "none"
        except sr.UnknownValueError:
            conversation_area.insert(tk.END, "Jarvis: Sorry, I didn't catch that.\n")
            conversation_area.see(tk.END)
            speak("Sorry, I didn't catch that.") # Avoid speaking errors constantly
            print("Could not understand audio.")
            return "none"
        except sr.RequestError as e:
            error_msg = f"Jarvis: Network error ({e}). Please check connection.\n"
            conversation_area.insert(tk.END, error_msg)
            conversation_area.see(tk.END)
            speak(f"Network error: {e}")
            return "none"
        except Exception as e:
            error_msg = f"Jarvis: Error during speech recognition: {e}\n"
            conversation_area.insert(tk.END, error_msg)
            conversation_area.see(tk.END)
            speak("Sorry, an error occurred during listening.")
            return "none"


def generate_response(query):
    """Generate a response for the given query using Gemini."""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        # Consider adding safety settings if needed
        response = model.generate_content(
            query,
            generation_config=genai.GenerationConfig(
                max_output_tokens=150, # Increased token limit slightly
                temperature=0.7, # Slightly more creative for chat
            )
        )
        # print(response.prompt_feedback) # Useful for debugging safety blocks
        return response.text.strip()
    except Exception as e:
        print(f"Error generating Gemini response: {e}")
        # Check for specific Google API errors if possible
        return f"Sorry, I encountered an error interacting with the AI: {e}"

def sanitize_filename(name):
    """Removes or replaces characters illegal in filenames."""
    name = re.sub(r'[<>:"/\\|?*]', '_', name) # Replace illegal chars with underscore
    name = name.strip()
    if not name: # Handle empty names after sanitization
        name = f"gemini_output_{random.randint(1000, 9999)}"
    return name[:100] # Limit filename length


# --- Command Handling Logic ---
def handle_conversation():
    """Continuously listen to user input and respond."""
    global stop_conversation

    # Define websites to open
    sites = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "facebook": "https://www.facebook.com",
    "twitter": "https://twitter.com",
    "instagram": "https://www.instagram.com",
    "baidu": "https://www.baidu.com",
    "wikipedia": "https://www.wikipedia.org",
    "yahoo": "https://www.yahoo.com",
    "whatsapp": "https://www.whatsapp.com",
    "reddit": "https://www.reddit.com",
    "amazon": "https://www.amazon.com",
    "tiktok": "https://www.tiktok.com",
    "vk": "https://vk.com",
    "linkedin": "https://www.linkedin.com",
    "microsoft": "https://www.microsoft.com",
    "netflix": "https://www.netflix.com",
    "yandex": "https://yandex.ru",
    "mail.ru": "https://mail.ru",
    "bing": "https://www.bing.com",
    "duckduckgo": "https://duckduckgo.com",
    "twitch": "https://www.twitch.tv",
    "roblox": "https://www.roblox.com",
    "msn": "https://www.msn.com",
    "ebay": "https://www.ebay.com",
    "paypal": "https://www.paypal.com",
    "wikimedia": "https://wikimedia.org",
    "stackoverflow": "https://stackoverflow.com",
    "craigslist": "https://www.craigslist.org",
    "imdb": "https://www.imdb.com",
    "apple": "https://www.apple.com",
    "office": "https://www.office.com",
    "canva": "https://www.canva.com",
    "discord": "https://discord.com",
    "cloudflare": "https://www.cloudflare.com",
    "openai": "https://openai.com",
    "zoom": "https://zoom.us",
    "nytimes": "https://www.nytimes.com",
    "cnn": "https://www.cnn.com",
    "bbc": "https://www.bbc.com",
    "quora": "https://www.quora.com",
    "espn": "https://www.espn.com",
    "weather": "https://weather.com",
    "live": "https://outlook.live.com",
    "googleusercontent": "https://www.googleusercontent.com",
    "blogspot": "https://www.blogspot.com",
    "wordpress": "https://wordpress.com",
    "amazonaws": "https://aws.amazon.com",
    "adobe": "https://www.adobe.com",
    "mozilla": "https://www.mozilla.org",
    "wikimediafoundation": "https://wikimediafoundation.org",
    "github": "https://github.com",
    "gitlab": "https://gitlab.com",
    "docker": "https://www.docker.com",
    "npm": "https://www.npmjs.com",
    "stackoverflowcareers": "https://stackoverflow.careers",
    "indeed": "https://www.indeed.com",
    "glassdoor": "https://www.glassdoor.com",
    "craigslistboston": "https://boston.craigslist.org",
    "zillow": "https://www.zillow.com",
    "realtor": "https://www.realtor.com",
    "booking": "https://www.booking.com",
    "airbnb": "https://www.airbnb.com",
    "tripadvisor": "https://www.tripadvisor.com",
    "expedia": "https://www.expedia.com",
    "walmart": "https://www.walmart.com",
    "target": "https://www.target.com",
    "homedepot": "https://www.homedepot.com",
    "lowes": "https://www.lowes.com",
    "bestbuy": "https://www.bestbuy.com",
    "costco": "https://www.costco.com",
    "samsung": "https://www.samsung.com",
    "huawei": "https://www.huawei.com",
    "mi": "https://www.mi.com",
    "oppo": "https://www.oppo.com",
    "vivo": "https://www.vivo.com",
    "shopify": "https://www.shopify.com",
    "etsy": "https://www.etsy.com",
    "aliexpress": "https://www.aliexpress.com",
    "alibaba": "https://www.alibaba.com",
    "substack": "https://substack.com",
    "medium": "https://medium.com",
    "wordpressorg": "https://wordpress.org",
    "drupal": "https://www.drupal.org",
    "joomla": "https://www.joomla.org",
    "python": "https://www.python.org",
    "java": "https://www.java.com",
    "javascript": "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
    "php": "https://www.php.net",
    "mysql": "https://www.mysql.com",
    "postgresql": "https://www.postgresql.org",
    "w3schools": "https://www.w3schools.com",
    "coursera": "https://www.coursera.org",
    "udemy": "https://www.udemy.com",
    "edx": "https://www.edx.org",
    "khanacademy": "https://www.khanacademy.org",
    "spotify": "https://www.spotify.com",
    "pandora": "https://www.pandora.com",
    "soundcloud": "https://soundcloud.com"
}
    output_dir = "D:\\JarvisAi\\JARVISAI" # Directory to save files

    while not stop_conversation:
        query = listen_to_command()
        if query == "none" or query == "":
            continue # Skip if listening failed

        command_handled = False # Flag to check if a specific command was run

        # 1. Check for Exit command
        if "bye" in query or "goodbye" in query or "jarvis quit" in query:
            speak("Goodbye! Have a great day!")
            stop_conversation = True 

        # 2. Check for Time command
        elif "the time" in query:
            now = datetime.datetime.now()
            time_str = now.strftime("%I:%M %p") 
            speak(f"The current time is {time_str}")
            command_handled = True

        elif "the date" in query or "what's today's date" in query:
            today = datetime.date.today()
            date_str = today.strftime("%B %d, %Y") # Format: April 03, 2025
            speak(f"Today's date is {date_str}")
            command_handled = True

        # 3. Check for Website Opening commands
        else:
            for site, url in sites.items():
                if f"open {site}" in query:
                    speak(f"Opening {site}...")
                    try:
                        webbrowser.open(url)
                        command_handled = True
                        break # Exit site loop once handled
                    except Exception as e:
                        speak(f"Sorry, I couldn't open {site}. Error: {e}")
                        command_handled = True # Still handle it to prevent AI call
                        break

        # 4. Check for Create File command
        if not command_handled and ("create file about" in query or "save response for" in query):
            # Extract the topic
            topic = query.replace("create file about", "").replace("save response for", "").strip()
            if topic:
                speak(f"Okay, generating content to create a file about {topic}...")
                ai_content = generate_response(f"Write a short text about: {topic}") # Get content from Gemini

                if "Sorry, I encountered an error" not in ai_content: # Check if AI call was successful
                    try:
                        # Create directory if it doesn't exist
                        os.makedirs(output_dir, exist_ok=True)

                        # Create filename
                        filename = sanitize_filename(topic) + ".txt"
                        filepath = os.path.join(output_dir, filename)

                        # Prepare text to save
                        file_content = f"Query: {topic}\n\nResponse:\n{ai_content}"

                        # Write to file
                        with open(filepath, "w", encoding='utf-8') as f:
                            f.write(file_content)

                        speak(f"Content saved successfully to {filepath}")
                    except Exception as e:
                        speak(f"Sorry, I failed to save the file. Error: {e}")
                else:
                    # Speak the error message returned by generate_response
                    speak(ai_content)

                command_handled = True
            else:
                speak("Please specify what you want me to create a file about.")
                command_handled = True

        # 5. Default to Gemini Chat if no specific command was handled
        if not command_handled:
            # Generate and respond using Gemini
            response = generate_response(query)
            speak(response) # speak() now also adds to conversation_area

# Initialize conversation_thread *before* start_conversation
conversation_thread = None
stop_conversation = False # Initialize stop_conversation globally

def start_conversation():
    """Start the conversation thread."""
    global conversation_thread, stop_conversation
    if conversation_thread is not None and conversation_thread.is_alive():
        conversation_area.insert(tk.END, "Jarvis: Conversation already running.\n")
        return

    stop_conversation = False # Ensure flag is reset when starting
    # Clear conversation area on start
    conversation_area.delete('1.0', tk.END)
    conversation_area.insert(tk.END, "Starting Jarvis...\n")

    # Start the background thread
    conversation_thread = threading.Thread(target=handle_conversation)
    conversation_thread.daemon = True # Ensures thread exits when main program does
    conversation_thread.start()

    # Initial greeting after thread starts
    conversation_area.insert(tk.END, "Jarvis: Hi, I am Jarvis. How can I help you?\n\n")
    conversation_area.see(tk.END)
    speak("Hi, I am Jarvis. How can I help you?")


def end_conversation():
    """Set the stop_conversation flag and close the application."""
    global stop_conversation
    if stop_conversation: # Prevent multiple end messages if already stopping
        return

    stop_conversation = True
    speak("Ending conversation. Goodbye!")
    # Add a small delay to allow the thread loop to check the flag maybe
    # root.after(500, root.quit) # Delay quit slightly (optional)
    root.quit() # Stop Tkinter mainloop
    # No need to explicitly join daemon thread


# --- Set up the GUI ---
# --- Set up the GUI (Better, Stylish) ---
root = tk.Tk()
root.title("J-A-R-V-I-S (Gemini Edition)")
root.geometry("700x500")  # Bigger and cleaner window
root.config(bg="#0F172A")  # Darker background color (Dark Blue)

# Custom font and colors
FONT = ("Segoe UI", 12)
HEADER_FONT = ("Segoe UI", 18, "bold")
TEXT_COLOR = "#E2E8F0"  # Light text
BUTTON_BG = "#1E293B"
BUTTON_HOVER_BG = "#3B82F6"
BUTTON_FG = "#F1F5F9"

# Header Label
header_label = tk.Label(
    root, text="🤖 Jarvis AI Assistant", font=HEADER_FONT,
    bg="#0F172A", fg="#3B82F6", pady=10
)
header_label.pack()

# Conversation area
conversation_area = scrolledtext.ScrolledText(
    root, wrap=tk.WORD, width=80, height=20,
    font=FONT, bg="#1E293B", fg=TEXT_COLOR, insertbackground=TEXT_COLOR,
    relief=tk.FLAT, bd=5
)
conversation_area.pack(padx=15, pady=10, expand=True, fill=tk.BOTH)

# Frame for buttons
button_frame = tk.Frame(root, bg="#0F172A")
button_frame.pack(pady=10)

# Helper function for button hover effect
def on_enter(e):
    e.widget['background'] = BUTTON_HOVER_BG

def on_leave(e):
    e.widget['background'] = BUTTON_BG

# Start button
start_button = tk.Button(
    button_frame, text="🎙️ Start Listening",
    font=FONT, bg=BUTTON_BG, fg=BUTTON_FG,
    activebackground=BUTTON_HOVER_BG, activeforeground=TEXT_COLOR,
    padx=15, pady=5, relief=tk.GROOVE,
    command=start_conversation
)
start_button.pack(side=tk.LEFT, padx=10)
start_button.bind("<Enter>", on_enter)
start_button.bind("<Leave>", on_leave)

# End button
end_button = tk.Button(
    button_frame, text="❌ Stop & Exit",
    font=FONT, bg=BUTTON_BG, fg=BUTTON_FG,
    activebackground=BUTTON_HOVER_BG, activeforeground=TEXT_COLOR,
    padx=15, pady=5, relief=tk.GROOVE,
    command=end_conversation
)
end_button.pack(side=tk.LEFT, padx=10)
end_button.bind("<Enter>", on_enter)
end_button.bind("<Leave>", on_leave)

# Ensure conversation stops if window closed via 'X'
def on_closing():
    global stop_conversation
    stop_conversation = True
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# --- Start the Tkinter event loop ---
root.mainloop()
