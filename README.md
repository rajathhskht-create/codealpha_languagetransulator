# codealpha_languagetransulator
A Python Tkinter desktop app using Google Cloud Translate API to translate text across 80+ languages. Features include auto language detection, source/target language selection with swap, API key input, copy to clipboard, text-to-speech output, real-time character count, and threaded background API calls for a smooth, responsive UI.

Importing Libraries:
pythonimport tkinter as tk
from tkinter import ttk, messagebox
import threading, os, urllib.request, urllib.parse, json

tkinter → builds the desktop GUI window

threading → runs API call in background so the window doesn't freeze

urllib → sends HTTP request to Google Translate API

json → reads the API response

os → reads environment variables (API key) 

 Colors & Fonts
pythonBG = "#1e1e2e"   ACCENT = "#7c6fe0"   TEXT = "#e8e6f0"

Defines the dark theme colors and Segoe UI fonts used throughout the UI — set once, reused everywhere
