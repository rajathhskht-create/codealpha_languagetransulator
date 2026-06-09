🌐 Language & Voice Translator
A fully functional desktop translation app built with Python — translates text across 80+ languages in real time, with voice output, auto language detection, and a beautiful dark UI.

🎓 Built as part of my Python internship at CodeAlpha


✨ Features
FeatureDescription🌍 80+ LanguagesCovers major world & Indian languages🔍 Auto-detectAutomatically identifies the source language🔊 Text-to-SpeechSpeaks both source and translated text⇄ Swap LanguagesSwap source & target with one click📋 Copy to ClipboardCopy translation instantly⚡ No API KeyUses MyMemory free API — works out of the box🎨 Dark UIGradient dark theme with animated loading🧵 Multi-threadedUI never freezes during translation🖥️ Cross-platformWorks on Windows, Mac & Linux

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


🚀 Future Improvements

 History of past translations
 Favourite/bookmark translations
 Dark/light theme toggle
 Offline translation support
 Translation of uploaded text files (.txt, .pdf)
 Pronunciation guide
