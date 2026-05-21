# codealpha_languagetransulator
A Python Tkinter desktop app using Google Cloud Translate API to translate text across 80+ languages. Features include auto language detection, source/target language selection with swap, API key input, copy to clipboard, text-to-speech output, real-time character count, and threaded background API calls for a smooth, responsive UI.

Importing Libraries:

pythonimport tkinter as tk

from tkinter import ttk, messagebox

import threading

import os

import urllib.request

import urllib.parse

import json

tkinter → builds the desktop GUI window

threading → runs API call in background so the window doesn't freeze

urllib → sends HTTP request to Google Translate API

json → reads the API response

os → reads environment variables (API key) 

Translation Logic:

pythonthreading.Thread(target=self._do_api_call, ...).start()

Validates that text and API key are present

Sets UI to loading state ("Translating…")

Launches background thread to call the API — UI stays responsive

Key Events:

_on_src_key — triggered every keypress:

pythonself.char_lbl.config(text=f"{n} / 5000")

Updates character count and enables/disables Translate button.

_clear — resets everything to blank state.

_swap_languages — swaps FROM/TO dropdowns and moves translated text back to source box.

process for language transulator:

User types text

      ↓
      
Clicks Translate

      ↓
      
Background thread calls Google API

      ↓
      
Response parsed (translation + detected language)

      ↓
      
UI updated → output shown → Copy/Listen enabled
