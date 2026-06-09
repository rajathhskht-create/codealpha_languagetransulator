🌐 Language & Voice Translator
A fully functional desktop translation app built with Python — translates text across 80+ languages in real time, with voice output, auto language detection, and a beautiful dark UI.

🎓 Built as part of my Python internship at CodeAlpha


✨ Features
Feature                                           Description                                                                       
🌍 80+ Languages                          Covers major world & Indian languages
🔍 Auto-detect                            Automatically identifies the source language
🔊 Text-to-Speech                         Speaks both source and translated text
⇄ Swap Languages                          Swap source & target with one click
📋 Copy to Clipboard                      Copy translation instantly
⚡ No API Key                             Uses MyMemory free API — works out of the box
🎨 Dark UI                                Gradient dark theme with animated loading
🧵 Multi-threaded                         UI never freezes during translation
🖥️ Cross-platform                         Works on Windows, Mac & Linux

🖼️ Screenshots

(Add screenshots here after running the app — drag images into the screenshots/ folder)


🛠️ Tech Stack

Python 3.8+
Tkinter — GUI framework (built into Python)
MyMemory API — Free translation API (no key needed)
gTTS — Google Text-to-Speech
playsound — Audio playback
threading — Background API calls so UI stays smooth


⚙️ Setup & Run
1. Clone the repository
bashgit clone https://github.com/your-username/language-translator.git
cd language-translator
2. Create a virtual environment (recommended)
bashpython -m venv venv
source venv/bin/activate       # macOS / Linux
venv\Scripts\activate          # Windows
3. Install dependencies
bashpip install -r requirements.txt
4. Run the app
bashpython src/language_translator.py
The translator window will open immediately — no setup, no API key required!

📁 Project Structure
language-translator/
│
├── src/
│   └── language_translator.py   # Main application
│
├── screenshots/                 # App screenshots (add yours here)
│
├── requirements.txt             # Python dependencies
├── .gitignore
└── README.md

🌏 Supported Languages (80+)
Includes all major world languages and Indian regional languages:
English Hindi Telugu Tamil Kannada Malayalam Marathi
Bengali Punjabi Gujarati Urdu Spanish French German
Japanese Chinese Arabic Russian Portuguese Korean
and 60+ more!

🔊 Text-to-Speech Support

Primary: gTTS (Google TTS) — supports all 80+ languages including Telugu, Hindi, Tamil
Fallback (Windows): PowerShell SAPI — works offline for English
Fallback (Mac): say command — built-in macOS TTS

🙏 Acknowledgements

MyMemory Translation API — free translation API
gTTS — Google Text-to-Speech library
CodeAlpha — for the internship opportunity
