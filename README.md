# JARVIS AI Assistant

This is a Python-based AI assistant that uses Google's Gemini Pro model for intelligence, along with speech recognition and text-to-speech capabilities to interact with the user.

## Features

- **Voice Interaction**: Listens to your commands and responds with voice.
- **AI-Powered**: Uses Google Gemini Pro for answering questions and generating content.
- **System Control**: Can open applications, websites, and take screenshots.
- **Utilities**:
    - Tell jokes
    - Play music
    - Send emails
    - Get weather updates
    - Set alarms
    - Search Wikipedia
    - Calculate math expressions

## Prerequisites

- [Python](https://www.python.org/downloads/) installed on your system.
- A Google Cloud API Key for Gemini.

## Installation

1.  **Clone or Download** this repository.
2.  **Navigate** to the project directory:
    ```bash
    cd "d:\JarvisAi"
    ```
3.  **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: You might need to install `pyaudio` separately if you encounter errors. On Windows, `pip install pipwin && pipwin install pyaudio` often works if direct installation fails.*

## Configuration

1.  Open `JARVISAI/jarvis.py` (or `JARVISAI/main.py`).
2.  Locate the line:
    ```python
    GENAI_API_KEY = "AIzaSyDAKrhTYGzatmdxvgT3EGAUEin91QboKLk"
    ```
    *Note: It is recommended to use environment variables for security instead of hardcoding the key.*
3.  Update other configurations like `output_dir`, `music_dir`, `email_user`, and `email_password` as needed in the script.
4. For Weather functionality, you will need an OpenWeatherMap API key and update it in the `get_weather` function.

## Usage

Run the main script:

```bash
python JARVISAI/jarvis.py
```
Or for the alternate version:
```bash
python JARVISAI/main.py
```

Click "Start Listening" on the GUI to begin interacting with Jarvis.

## Commands Examples

- "What is the time?"
- "Open YouTube"
- "Tell me a joke"
- "Search Wikipedia for Artificial Intelligence"
- "Take a screenshot"
- "Play music"
