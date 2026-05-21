import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os

try:
    from google.cloud import translate_v2 as translate
except ImportError:
    raise SystemExit("Please run:  pip install google-cloud-translate")

# ── 100+ supported languages ──────────────────────────────────────────────────
LANGUAGES = [
    ("Auto-detect",          "auto"),
    ("Afrikaans",            "af"),
    ("Albanian",             "sq"),
    ("Amharic",              "am"),
    ("Arabic",               "ar"),
    ("Armenian",             "hy"),
    ("Azerbaijani",          "az"),
    ("Basque",               "eu"),
    ("Bengali",              "bn"),
    ("Bosnian",              "bs"),
    ("Bulgarian",            "bg"),
    ("Catalan",              "ca"),
    ("Chinese (Simplified)", "zh-CN"),
    ("Chinese (Traditional)","zh-TW"),
    ("Croatian",             "hr"),
    ("Czech",                "cs"),
    ("Danish",               "da"),
    ("Dutch",                "nl"),
    ("English",              "en"),
    ("Estonian",             "et"),
    ("Finnish",              "fi"),
    ("French",               "fr"),
    ("Galician",             "gl"),
    ("Georgian",             "ka"),
    ("German",               "de"),
    ("Greek",                "el"),
    ("Gujarati",             "gu"),
    ("Haitian Creole",       "ht"),
    ("Hebrew",               "he"),
    ("Hindi",                "hi"),
    ("Hungarian",            "hu"),
    ("Icelandic",            "is"),
    ("Indonesian",           "id"),
    ("Irish",                "ga"),
    ("Italian",              "it"),
    ("Japanese",             "ja"),
    ("Javanese",             "jv"),
    ("Kannada",              "kn"),
    ("Kazakh",               "kk"),
    ("Khmer",                "km"),
    ("Korean",               "ko"),
    ("Lao",                  "lo"),
    ("Latin",                "la"),
    ("Latvian",              "lv"),
    ("Lithuanian",           "lt"),
    ("Macedonian",           "mk"),
    ("Malay",                "ms"),
    ("Malayalam",            "ml"),
    ("Maltese",              "mt"),
    ("Maori",                "mi"),
    ("Marathi",              "mr"),
    ("Mongolian",            "mn"),
    ("Nepali",               "ne"),
    ("Norwegian",            "no"),
    ("Pashto",               "ps"),
    ("Persian",              "fa"),
    ("Polish",               "pl"),
    ("Portuguese",           "pt"),
    ("Punjabi",              "pa"),
    ("Romanian",             "ro"),
    ("Russian",              "ru"),
    ("Serbian",              "sr"),
    ("Sinhala",              "si"),
    ("Slovak",               "sk"),
    ("Slovenian",            "sl"),
    ("Somali",               "so"),
    ("Spanish",              "es"),
    ("Swahili",              "sw"),
    ("Swedish",              "sv"),
    ("Tagalog (Filipino)",   "tl"),
    ("Tajik",                "tg"),
    ("Tamil",                "ta"),
    ("Telugu",               "te"),
    ("Thai",                 "th"),
    ("Turkish",              "tr"),
    ("Ukrainian",            "uk"),
    ("Urdu",                 "ur"),
    ("Uzbek",                "uz"),
    ("Vietnamese",           "vi"),
    ("Welsh",                "cy"),
    ("Yoruba",               "yo"),
    ("Zulu",                 "zu"),
]

LANG_NAMES  = [l[0] for l in LANGUAGES]          # display names
LANG_CODES  = {l[0]: l[1] for l in LANGUAGES}    # name → code
CODE_NAMES  = {l[1]: l[0] for l in LANGUAGES}    # code → name

# ── Colours & fonts ───────────────────────────────────────────────────────────
BG          = "#1e1e2e"
PANEL_BG    = "#2a2a3d"
ACCENT      = "#7c6fe0"
ACCENT_DARK = "#5c4fcf"
ACCENT_LITE = "#3d3060"
TEXT        = "#e8e6f0"
TEXT_DIM    = "#8888aa"
TEXT_FAINT  = "#555570"
BORDER      = "#3a3a55"
SUCCESS     = "#4caf88"
ERROR_COL   = "#e06060"
WHITE       = "#ffffff"

FONT_MAIN   = ("Segoe UI", 10)
FONT_LABEL  = ("Segoe UI", 9)
FONT_TITLE  = ("Segoe UI", 13, "bold")
FONT_TEXT   = ("Segoe UI", 11)
FONT_BTN    = ("Segoe UI", 10, "bold")


# ─────────────────────────────────────────────────────────────────────────────
class TranslatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Language and Voice Translator")
        self.geometry("900x620")
        self.minsize(700, 500)
        self.configure(bg=BG)
        self.resizable(True, True)

        # Check API key early
        self._api_key = os.getenv("GOOGLE_API_KEY", "")
        self._client  = None
        self._translated = ""
        self._detected_code = None
        self._speaking = False

        self._build_ui()
        self._apply_styles()

    # ── UI construction ───────────────────────────────────────────────────────
    def _build_ui(self):
        # ─ Header ─
        hdr = tk.Frame(self, bg=BG, pady=14)
        hdr.pack(fill="x", padx=24)

        tk.Label(hdr, text="🌐  Language and Voice Translator", font=("Segoe UI", 18, "bold"),
                 bg=BG, fg=WHITE).pack(side="left")
        tk.Label(hdr, text="AI-powered translation · 80+ languages",
                 font=FONT_LABEL, bg=BG, fg=TEXT_DIM).pack(side="left", padx=14, pady=6)

        # API key field (top-right)
        key_frame = tk.Frame(hdr, bg=BG)
        key_frame.pack(side="right")
        tk.Label(key_frame, text="API Key:", font=FONT_LABEL,
                 bg=BG, fg=TEXT_DIM).pack(side="left", padx=(0,4))
        self.key_var = tk.StringVar(value=self._api_key)
        key_entry = tk.Entry(key_frame, textvariable=self.key_var, show="•",
                             width=28, bg=PANEL_BG, fg=TEXT, insertbackground=TEXT,
                             relief="flat", font=FONT_LABEL,
                             highlightthickness=1, highlightbackground=BORDER,
                             highlightcolor=ACCENT)
        key_entry.pack(side="left")

        # ─ Language bar ─
        lang_bar = tk.Frame(self, bg=PANEL_BG, pady=10, padx=16)
        lang_bar.pack(fill="x", padx=24, pady=(0, 8))

        # Source language
        tk.Label(lang_bar, text="FROM", font=("Segoe UI", 8, "bold"),
                 bg=PANEL_BG, fg=TEXT_DIM).grid(row=0, column=0, sticky="w")
        self.src_var = tk.StringVar(value="Auto-detect")
        src_names = LANG_NAMES  # includes Auto-detect
        self.src_combo = ttk.Combobox(lang_bar, textvariable=self.src_var,
                                      values=src_names, state="readonly", width=26)
        self.src_combo.grid(row=1, column=0, padx=(0, 8))

        # Swap button
        self.swap_btn = tk.Button(lang_bar, text="⇄", font=("Segoe UI", 13),
                                  bg=ACCENT_LITE, fg=WHITE, relief="flat",
                                  cursor="hand2", width=3,
                                  command=self._swap_languages)
        self.swap_btn.grid(row=1, column=1, padx=6)

        # Target language
        tk.Label(lang_bar, text="TO", font=("Segoe UI", 8, "bold"),
                 bg=PANEL_BG, fg=TEXT_DIM).grid(row=0, column=2, sticky="w")
        tgt_names = [l[0] for l in LANGUAGES if l[1] != "auto"]
        self.tgt_var = tk.StringVar(value="Spanish")
        self.tgt_combo = ttk.Combobox(lang_bar, textvariable=self.tgt_var,
                                      values=tgt_names, state="readonly", width=26)
        self.tgt_combo.grid(row=1, column=2, padx=(8, 0))

        # Detected label
        self.detected_lbl = tk.Label(lang_bar, text="", font=FONT_LABEL,
                                     bg=PANEL_BG, fg=SUCCESS)
        self.detected_lbl.grid(row=1, column=3, padx=(18, 0))

        # ─ Text panels ─
        panels = tk.Frame(self, bg=BG)
        panels.pack(fill="both", expand=True, padx=24, pady=(0, 8))
        panels.columnconfigure(0, weight=1)
        panels.columnconfigure(1, weight=1)
        panels.rowconfigure(1, weight=1)

        # Source label + char count
        src_top = tk.Frame(panels, bg=BG)
        src_top.grid(row=0, column=0, sticky="ew", pady=(0, 4))
        tk.Label(src_top, text="Source Text", font=FONT_LABEL,
                 bg=BG, fg=TEXT_DIM).pack(side="left")
        self.char_lbl = tk.Label(src_top, text="0 / 5000", font=FONT_LABEL,
                                 bg=BG, fg=TEXT_FAINT)
        self.char_lbl.pack(side="right")

        # Target label + char count
        tgt_top = tk.Frame(panels, bg=BG)
        tgt_top.grid(row=0, column=1, sticky="ew", pady=(0, 4), padx=(12, 0))
        tk.Label(tgt_top, text="Translation", font=FONT_LABEL,
                 bg=BG, fg=TEXT_DIM).pack(side="left")
        self.out_char_lbl = tk.Label(tgt_top, text="", font=FONT_LABEL,
                                     bg=BG, fg=TEXT_FAINT)
        self.out_char_lbl.pack(side="right")

        # Source textarea
        src_frame = tk.Frame(panels, bg=PANEL_BG,
                             highlightbackground=BORDER, highlightthickness=1)
        src_frame.grid(row=1, column=0, sticky="nsew")
        self.src_text = tk.Text(src_frame, font=FONT_TEXT, bg=PANEL_BG, fg=TEXT,
                                insertbackground=ACCENT, relief="flat", wrap="word",
                                padx=14, pady=12, maxundo=50)
        self.src_text.pack(fill="both", expand=True)
        self.src_text.bind("<KeyRelease>", self._on_src_key)
        self.src_text.bind("<Control-Return>", lambda e: self._translate())

        # Target text (read-only)
        tgt_frame = tk.Frame(panels, bg=PANEL_BG,
                             highlightbackground=BORDER, highlightthickness=1)
        tgt_frame.grid(row=1, column=1, sticky="nsew", padx=(12, 0))
        self.out_text = tk.Text(tgt_frame, font=FONT_TEXT, bg=PANEL_BG, fg=TEXT,
                                relief="flat", wrap="word", padx=14, pady=12,
                                state="disabled", cursor="arrow")
        self.out_text.pack(fill="both", expand=True)

        # ─ Status bar ─
        self.status_lbl = tk.Label(self, text="Ready", font=FONT_LABEL,
                                   bg=BG, fg=TEXT_DIM, anchor="w")
        self.status_lbl.pack(fill="x", padx=28, pady=(0, 4))

        # ─ Bottom buttons ─
        btn_row = tk.Frame(self, bg=BG, pady=10)
        btn_row.pack(fill="x", padx=24)

        self.clear_btn = tk.Button(btn_row, text="✕  Clear", font=FONT_BTN,
                                   bg=PANEL_BG, fg=TEXT_DIM, relief="flat",
                                   padx=14, pady=8, cursor="hand2",
                                   command=self._clear)
        self.clear_btn.pack(side="left", padx=(0, 8))

        self.speak_src_btn = tk.Button(btn_row, text="🔊 Listen (source)", font=FONT_BTN,
                                       bg=PANEL_BG, fg=TEXT_DIM, relief="flat",
                                       padx=14, pady=8, cursor="hand2",
                                       command=self._speak_source)
        self.speak_src_btn.pack(side="left", padx=(0, 8))

        # Translate (centre)
        self.translate_btn = tk.Button(btn_row, text="  Translate  ➜",
                                       font=FONT_BTN, bg=ACCENT, fg=WHITE,
                                       relief="flat", padx=22, pady=8,
                                       cursor="hand2", state="disabled",
                                       command=self._translate)
        self.translate_btn.pack(side="left", padx=(0, 8))

        tk.Label(btn_row, text="Ctrl+Enter", font=("Segoe UI", 8),
                 bg=BG, fg=TEXT_FAINT).pack(side="left")

        self.copy_btn = tk.Button(btn_row, text="📋 Copy", font=FONT_BTN,
                                  bg=PANEL_BG, fg=TEXT_DIM, relief="flat",
                                  padx=14, pady=8, cursor="hand2",
                                  state="disabled", command=self._copy)
        self.copy_btn.pack(side="right", padx=(8, 0))

        self.speak_out_btn = tk.Button(btn_row, text="🔊 Listen (output)", font=FONT_BTN,
                                       bg=PANEL_BG, fg=TEXT_DIM, relief="flat",
                                       padx=14, pady=8, cursor="hand2",
                                       state="disabled",
                                       command=self._speak_output)
        self.speak_out_btn.pack(side="right", padx=(8, 0))

    def _apply_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TCombobox",
                        fieldbackground=PANEL_BG, background=PANEL_BG,
                        foreground=TEXT, selectbackground=ACCENT,
                        selectforeground=WHITE, arrowcolor=TEXT_DIM,
                        bordercolor=BORDER, lightcolor=PANEL_BG,
                        darkcolor=PANEL_BG, relief="flat")
        style.map("TCombobox",
                  fieldbackground=[("readonly", PANEL_BG)],
                  foreground=[("readonly", TEXT)],
                  selectbackground=[("readonly", ACCENT)])

    # ── Callbacks ─────────────────────────────────────────────────────────────
    def _on_src_key(self, _=None):
        n = len(self.src_text.get("1.0", "end-1c"))
        self.char_lbl.config(text=f"{n} / 5000")
        self.translate_btn.config(state="normal" if n else "disabled")

    def _clear(self):
        self.src_text.delete("1.0", "end")
        self._set_output("")
        self.char_lbl.config(text="0 / 5000")
        self.out_char_lbl.config(text="")
        self.translate_btn.config(state="disabled")
        self.copy_btn.config(state="disabled")
        self.speak_out_btn.config(state="disabled")
        self.detected_lbl.config(text="")
        self.status_lbl.config(text="Ready", fg=TEXT_DIM)
        self._translated = ""
        self._detected_code = None

    def _swap_languages(self):
        src = self.src_var.get()
        tgt = self.tgt_var.get()
        tgt_code = LANG_CODES.get(tgt, "en")

        # Set source to current target (skip Auto-detect)
        if src == "Auto-detect" and self._detected_code:
            self.src_var.set(CODE_NAMES.get(self._detected_code, tgt))
        else:
            self.src_var.set(tgt)

        # Set target to current source
        if src == "Auto-detect":
            self.tgt_var.set("English")
        else:
            # make sure it's not in the no-auto list
            if src in [l[0] for l in LANGUAGES if l[1] != "auto"]:
                self.tgt_var.set(src)

        # Move translated text to source
        if self._translated:
            self.src_text.delete("1.0", "end")
            self.src_text.insert("end", self._translated)
            self._set_output("")
            self.copy_btn.config(state="disabled")
            self.speak_out_btn.config(state="disabled")
            self.translate_btn.config(state="normal")
            self._on_src_key()
        self.detected_lbl.config(text="")
        self._translated = ""

    # ── Translation ───────────────────────────────────────────────────────────
    def _translate(self, _=None):
        text = self.src_text.get("1.0", "end-1c").strip()
        if not text:
            return

        api_key = self.key_var.get().strip()
        if not api_key:
            messagebox.showerror("API Key Missing",
                                 "Please enter your Google API key in the top-right field.\n"
                                 "Get one at: https://console.cloud.google.com")
            return

        src = self.src_var.get()
        tgt = self.tgt_var.get()
        tgt_name = tgt
        src_name = src if src != "Auto-detect" else "the detected language"

        # UI → loading state
        self.translate_btn.config(state="disabled", text="Translating…")
        self.copy_btn.config(state="disabled")
        self.speak_out_btn.config(state="disabled")
        self._set_output("⏳  Translating…", dim=True)
        self.status_lbl.config(text="Calling API…", fg=ACCENT)
        self.update_idletasks()

        # Run in background thread so UI stays responsive
        threading.Thread(target=self._do_api_call,
                         args=(api_key, text, src, src_name, tgt_name),
                         daemon=True).start()

    def _do_api_call(self, api_key, text, src, src_name, tgt_name):
        try:
            from google.api_core.exceptions import GoogleAPICallError, PermissionDenied
            from google.oauth2 import service_account
            from google.api_core.client_options import ClientOptions

            client = translate.Client(client_options=ClientOptions(api_key=api_key))

            tgt_code = LANG_CODES.get(tgt_name, "en")

            if src == "Auto-detect":
                result = client.translate(text, target_language=tgt_code)
                translation = result["translatedText"]
                detected_code = result.get("detectedSourceLanguage", None)
                detected = CODE_NAMES.get(detected_code) if detected_code else None
            else:
                src_code = LANG_CODES.get(src, None)
                result = client.translate(text, source_language=src_code, target_language=tgt_code)
                translation = result["translatedText"]
                detected = None

            self.after(0, self._show_result, translation, detected)

        except PermissionDenied:
            self.after(0, self._show_error, "Invalid API key or permission denied. Check your key and try again.")
        except GoogleAPICallError as exc:
            self.after(0, self._show_error, f"Google API error: {exc.message}")
        except Exception as exc:
            self.after(0, self._show_error, str(exc))

    def _show_result(self, translation, detected):
        self._translated = translation
        self._set_output(translation)
        self.out_char_lbl.config(text=f"{len(translation)} chars")
        self.translate_btn.config(state="normal", text="  Translate  ➜")
        self.copy_btn.config(state="normal")
        self.speak_out_btn.config(state="normal")
        self.status_lbl.config(text="Translation complete  ✓", fg=SUCCESS)

        if detected:
            self._detected_code = LANG_CODES.get(detected)
            self.detected_lbl.config(text=f"✦ Detected: {detected}")
        else:
            self.detected_lbl.config(text="")

    def _show_error(self, msg):
        self._set_output(f"Error: {msg}", error=True)
        self.translate_btn.config(state="normal", text="  Translate  ➜")
        self.status_lbl.config(text="Translation failed", fg=ERROR_COL)

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _set_output(self, text, dim=False, error=False):
        self.out_text.config(state="normal")
        self.out_text.delete("1.0", "end")
        colour = TEXT_FAINT if dim else (ERROR_COL if error else TEXT)
        self.out_text.config(fg=colour)
        self.out_text.insert("end", text)
        self.out_text.config(state="disabled")

    def _copy(self):
        if not self._translated:
            return
        self.clipboard_clear()
        self.clipboard_append(self._translated)
        original = self.copy_btn.cget("text")
        self.copy_btn.config(text="✓ Copied!", fg=SUCCESS)
        self.after(2000, lambda: self.copy_btn.config(text=original, fg=TEXT_DIM))

    def _speak_source(self):
        text = self.src_text.get("1.0", "end-1c").strip()
        if text:
            threading.Thread(target=self._tts, args=(text,), daemon=True).start()

    def _speak_output(self):
        if self._translated:
            threading.Thread(target=self._tts, args=(self._translated,), daemon=True).start()

    def _tts(self, text):
        """Cross-platform text-to-speech (best-effort)."""
        import subprocess, sys, shutil
        platform = sys.platform
        try:
            if platform == "darwin":
                subprocess.run(["say", text], check=True)
            elif platform.startswith("linux"):
                if shutil.which("espeak"):
                    subprocess.run(["espeak", text], check=True)
                elif shutil.which("festival"):
                    subprocess.run(["festival", "--tts"], input=text.encode(), check=True)
                else:
                    self.after(0, lambda: messagebox.showinfo(
                        "TTS", "Install espeak for audio:\n  sudo apt install espeak"))
            elif platform == "win32":
                subprocess.run(
                    ["powershell", "-Command",
                     f'Add-Type -AssemblyName System.Speech; '
                     f'(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak("{text}")'],
                    check=True)
        except Exception:
            pass  # TTS is optional; silent fail


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = TranslatorApp()
    app.mainloop()