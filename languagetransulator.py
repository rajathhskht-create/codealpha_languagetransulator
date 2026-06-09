import tkinter as tk
from tkinter import ttk, messagebox
import threading
import urllib.request
import urllib.parse
import json
import time

# 100+ supported languages
LANGUAGES = [
    ("Auto-detect",           "auto"),
    ("Afrikaans",             "af"),
    ("Albanian",              "sq"),
    ("Amharic",               "am"),
    ("Arabic",                "ar"),
    ("Armenian",              "hy"),
    ("Azerbaijani",           "az"),
    ("Basque",                "eu"),
    ("Bengali",               "bn"),
    ("Bosnian",               "bs"),
    ("Bulgarian",             "bg"),
    ("Catalan",               "ca"),
    ("Chinese (Simplified)",  "zh"),
    ("Chinese (Traditional)", "zh-TW"),
    ("Croatian",              "hr"),
    ("Czech",                 "cs"),
    ("Danish",                "da"),
    ("Dutch",                 "nl"),
    ("English",               "en"),
    ("Estonian",              "et"),
    ("Finnish",               "fi"),
    ("French",                "fr"),
    ("Galician",              "gl"),
    ("Georgian",              "ka"),
    ("German",                "de"),
    ("Greek",                 "el"),
    ("Gujarati",              "gu"),
    ("Haitian Creole",        "ht"),
    ("Hebrew",                "he"),
    ("Hindi",                 "hi"),
    ("Hungarian",             "hu"),
    ("Icelandic",             "is"),
    ("Indonesian",            "id"),
    ("Irish",                 "ga"),
    ("Italian",               "it"),
    ("Japanese",              "ja"),
    ("Kannada",               "kn"),
    ("Kazakh",                "kk"),
    ("Korean",                "ko"),
    ("Latin",                 "la"),
    ("Latvian",               "lv"),
    ("Lithuanian",            "lt"),
    ("Macedonian",            "mk"),
    ("Malay",                 "ms"),
    ("Malayalam",             "ml"),
    ("Maltese",               "mt"),
    ("Maori",                 "mi"),
    ("Marathi",               "mr"),
    ("Mongolian",             "mn"),
    ("Nepali",                "ne"),
    ("Norwegian",             "no"),
    ("Pashto",                "ps"),
    ("Persian",               "fa"),
    ("Polish",                "pl"),
    ("Portuguese",            "pt"),
    ("Punjabi",               "pa"),
    ("Romanian",              "ro"),
    ("Russian",               "ru"),
    ("Serbian",               "sr"),
    ("Sinhala",               "si"),
    ("Slovak",                "sk"),
    ("Slovenian",             "sl"),
    ("Somali",                "so"),
    ("Spanish",               "es"),
    ("Swahili",               "sw"),
    ("Swedish",               "sv"),
    ("Tagalog (Filipino)",    "tl"),
    ("Tamil",                 "ta"),
    ("Telugu",                "te"),
    ("Thai",                  "th"),
    ("Turkish",               "tr"),
    ("Ukrainian",             "uk"),
    ("Urdu",                  "ur"),
    ("Uzbek",                 "uz"),
    ("Vietnamese",            "vi"),
    ("Welsh",                 "cy"),
    ("Yoruba",                "yo"),
    ("Zulu",                  "zu"),
]

LANG_NAMES = [l[0] for l in LANGUAGES]
LANG_CODES = {l[0]: l[1] for l in LANGUAGES}
CODE_NAMES = {l[1]: l[0] for l in LANGUAGES}

#Vibrant Color Palette
BG           = "#0f0c29"
BG2          = "#302b63"
PANEL_BG     = "#1a1a2e"
CARD_BG      = "#16213e"
ACCENT1      = "#e040fb"   # vivid purple-pink
ACCENT2      = "#00bcd4"   # cyan
ACCENT3      = "#ff6f00"   # orange
GREEN        = "#00e676"
RED_ERR      = "#ff5252"
TEXT         = "#f0f0ff"
TEXT_DIM     = "#9090bb"
TEXT_FAINT   = "#555588"
BORDER       = "#3d3d6b"
YELLOW       = "#ffd740"
WHITE        = "#ffffff"

FONT_TITLE   = ("Segoe UI", 17, "bold")
FONT_SUB     = ("Segoe UI", 9)
FONT_LABEL   = ("Segoe UI", 9, "bold")
FONT_TEXT    = ("Segoe UI", 11)
FONT_BTN     = ("Segoe UI", 10, "bold")
FONT_SMALL   = ("Segoe UI", 8)

#Gradient canvas helper 
def draw_gradient(canvas, w, h, c1, c2):
    """Draw a vertical gradient from c1 to c2 on a Canvas."""
    r1, g1, b1 = canvas.winfo_rgb(c1)
    r2, g2, b2 = canvas.winfo_rgb(c2)
    r1, g1, b1 = r1 // 256, g1 // 256, b1 // 256
    r2, g2, b2 = r2 // 256, g2 // 256, b2 // 256
    steps = max(h, 1)
    for i in range(steps):
        t   = i / steps
        r   = int(r1 + (r2 - r1) * t)
        g   = int(g1 + (g2 - g1) * t)
        b   = int(b1 + (b2 - b1) * t)
        col = f"#{r:02x}{g:02x}{b:02x}"
        canvas.create_line(0, i, w, i, fill=col)

class TranslatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🌐 Language Translator — Free & Fast")
        self.geometry("960x660")
        self.minsize(750, 520)
        self.configure(bg=BG)
        self.resizable(True, True)

        self._translated      = ""
        self._detected_code   = None
        self._anim_id         = None
        self._dot_count       = 0

        self._build_ui()
        self._apply_styles()

    # UI 
    def _build_ui(self):
        #  Header gradient banner
        self._header_canvas = tk.Canvas(self, height=80, highlightthickness=0)
        self._header_canvas.pack(fill="x")
        self._header_canvas.bind("<Configure>", self._redraw_header)
        # Will be drawn on first <Configure> event

        # Title label overlaid on canvas
        self._title_lbl = tk.Label(self._header_canvas,
                                   text="🌐  Language Translator",
                                   font=FONT_TITLE, bg="#24134a", fg=WHITE)
        self._title_lbl.place(x=24, y=14)

        self._sub_lbl = tk.Label(self._header_canvas,
                                 text="✦ No API key needed  ·  Free  ·  80+ languages",
                                 font=FONT_SUB, bg="#24134a", fg=ACCENT2)
        self._sub_lbl.place(x=26, y=50)

        # Language selector bar 
        lang_bar = tk.Frame(self, bg=CARD_BG, pady=12, padx=18)
        lang_bar.pack(fill="x", padx=22, pady=(10, 0))

        # FROM label + combo
        tk.Label(lang_bar, text="FROM", font=FONT_LABEL,
                 bg=CARD_BG, fg=ACCENT2).grid(row=0, column=0, sticky="w")
        self.src_var   = tk.StringVar(value="Auto-detect")
        self.src_combo = ttk.Combobox(lang_bar, textvariable=self.src_var,
                                      values=LANG_NAMES, state="readonly", width=28)
        self.src_combo.grid(row=1, column=0, padx=(0, 10))

        # Swap button (colored)
        self.swap_btn = tk.Button(lang_bar, text="⇄", font=("Segoe UI", 14, "bold"),
                                  bg=ACCENT1, fg=WHITE, relief="flat",
                                  activebackground="#c900e0", activeforeground=WHITE,
                                  cursor="hand2", width=3, bd=0,
                                  command=self._swap_languages)
        self.swap_btn.grid(row=1, column=1, padx=8)
        self.swap_btn.bind("<Enter>", lambda e: self.swap_btn.config(bg="#c900e0"))
        self.swap_btn.bind("<Leave>", lambda e: self.swap_btn.config(bg=ACCENT1))

        # TO label + combo
        tgt_names = [l[0] for l in LANGUAGES if l[1] != "auto"]
        tk.Label(lang_bar, text="TO", font=FONT_LABEL,
                 bg=CARD_BG, fg=ACCENT1).grid(row=0, column=2, sticky="w")
        self.tgt_var   = tk.StringVar(value="Spanish")
        self.tgt_combo = ttk.Combobox(lang_bar, textvariable=self.tgt_var,
                                      values=tgt_names, state="readonly", width=28)
        self.tgt_combo.grid(row=1, column=2, padx=(10, 0))

        # Detected language badge
        self.detected_lbl = tk.Label(lang_bar, text="", font=FONT_SUB,
                                     bg=CARD_BG, fg=GREEN)
        self.detected_lbl.grid(row=1, column=3, padx=(20, 0))

        # Text panels
        panels = tk.Frame(self, bg=BG)
        panels.pack(fill="both", expand=True, padx=22, pady=10)
        panels.columnconfigure(0, weight=1)
        panels.columnconfigure(1, weight=1)
        panels.rowconfigure(1, weight=1)

        # Source header
        src_top = tk.Frame(panels, bg=BG)
        src_top.grid(row=0, column=0, sticky="ew", pady=(0, 4))
        tk.Label(src_top, text="📝  Source Text", font=FONT_LABEL,
                 bg=BG, fg=ACCENT2).pack(side="left")
        self.char_lbl = tk.Label(src_top, text="0 / 500", font=FONT_SMALL,
                                  bg=BG, fg=TEXT_FAINT)
        self.char_lbl.pack(side="right")

        # Translation header
        tgt_top = tk.Frame(panels, bg=BG)
        tgt_top.grid(row=0, column=1, sticky="ew", pady=(0, 4), padx=(14, 0))
        tk.Label(tgt_top, text="✨  Translation", font=FONT_LABEL,
                 bg=BG, fg=ACCENT1).pack(side="left")
        self.out_char_lbl = tk.Label(tgt_top, text="", font=FONT_SMALL,
                                      bg=BG, fg=TEXT_FAINT)
        self.out_char_lbl.pack(side="right")

        # Source textarea
        src_frame = tk.Frame(panels, bg=ACCENT2,
                             highlightbackground=ACCENT2, highlightthickness=2)
        src_frame.grid(row=1, column=0, sticky="nsew")
        self.src_text = tk.Text(src_frame, font=FONT_TEXT, bg=CARD_BG, fg=TEXT,
                                insertbackground=ACCENT2, relief="flat",
                                wrap="word", padx=14, pady=12,
                                selectbackground=ACCENT2, selectforeground=BG)
        self.src_text.pack(fill="both", expand=True)
        self.src_text.bind("<KeyRelease>", self._on_src_key)
        self.src_text.bind("<Control-Return>", lambda e: self._translate())

        # Placeholder hint
        self._hint_visible = True
        self._hint_text = "Type or paste text here… (Ctrl+Enter to translate)"
        self.src_text.insert("1.0", self._hint_text)
        self.src_text.config(fg=TEXT_FAINT)
        self.src_text.bind("<FocusIn>",  self._clear_hint)
        self.src_text.bind("<FocusOut>", self._restore_hint)

        # Output textarea
        tgt_frame = tk.Frame(panels, bg=ACCENT1,
                             highlightbackground=ACCENT1, highlightthickness=2)
        tgt_frame.grid(row=1, column=1, sticky="nsew", padx=(14, 0))
        self.out_text = tk.Text(tgt_frame, font=FONT_TEXT, bg=CARD_BG, fg=TEXT,
                                relief="flat", wrap="word", padx=14, pady=12,
                                state="disabled", cursor="arrow",
                                selectbackground=ACCENT1, selectforeground=BG)
        self.out_text.pack(fill="both", expand=True)

        # Status bar
        self.status_lbl = tk.Label(self, text="✔  Ready — type text and press Translate",
                                   font=FONT_SMALL, bg=BG, fg=TEXT_DIM, anchor="w")
        self.status_lbl.pack(fill="x", padx=28, pady=(0, 4))

        # Bottom button row
        btn_row = tk.Frame(self, bg=BG, pady=10)
        btn_row.pack(fill="x", padx=22)

        # Clear
        self.clear_btn = self._mk_btn(btn_row, "✕  Clear", PANEL_BG, TEXT_DIM,
                                      "#c900e0", self._clear, side="left", padx=(0, 8))

        # Listen source
        self.speak_src_btn = self._mk_btn(btn_row, "🔊 Listen (source)", PANEL_BG,
                                          ACCENT2, ACCENT2, self._speak_source,
                                          side="left", padx=(0, 8))

        # Translate  (big vivid button)
        self.translate_btn = tk.Button(btn_row, text="  Translate  ➜",
                                       font=FONT_BTN,
                                       bg=ACCENT1, fg=WHITE, relief="flat",
                                       activebackground="#c900e0", activeforeground=WHITE,
                                       padx=26, pady=9, cursor="hand2",
                                       state="disabled", bd=0,
                                       command=self._translate)
        self.translate_btn.pack(side="left", padx=(0, 8))
        self.translate_btn.bind("<Enter>",
                                lambda e: self.translate_btn.config(bg="#c900e0"))
        self.translate_btn.bind("<Leave>",
                                lambda e: self.translate_btn.config(bg=ACCENT1))

        tk.Label(btn_row, text="Ctrl+Enter", font=FONT_SMALL,
                 bg=BG, fg=TEXT_FAINT).pack(side="left")

        # Copy
        self.copy_btn = self._mk_btn(btn_row, "📋 Copy", PANEL_BG, YELLOW,
                                     YELLOW, self._copy,
                                     side="right", padx=(8, 0), state="disabled")

        # Listen output
        self.speak_out_btn = self._mk_btn(btn_row, "🔊 Listen (output)", PANEL_BG,
                                          ACCENT2, ACCENT2, self._speak_output,
                                          side="right", padx=(8, 0), state="disabled")

    # Button factory 
    def _mk_btn(self, parent, text, bg, fg, hover_fg, cmd,
                side="left", padx=0, state="normal"):
        b = tk.Button(parent, text=text, font=FONT_BTN,
                      bg=bg, fg=fg, relief="flat",
                      activebackground=PANEL_BG, activeforeground=hover_fg,
                      padx=14, pady=8, cursor="hand2", state=state, bd=0,
                      command=cmd)
        b.pack(side=side, padx=padx)
        b.bind("<Enter>", lambda e, b=b, c=hover_fg: b.config(fg=c))
        b.bind("<Leave>", lambda e, b=b, c=fg: b.config(fg=c))
        return b

    # Header gradient redraw
    def _redraw_header(self, event=None):
        c  = self._header_canvas
        w  = c.winfo_width()
        h  = c.winfo_height()
        c.delete("all")
        draw_gradient(c, w, h, "#24134a", "#0d0d2b")
        # Glowing accent strip at bottom
        c.create_rectangle(0, h - 3, w, h, fill=ACCENT1, outline="")
        # Re-place labels after redraw
        self._title_lbl.place(x=24, y=12)
        self._sub_lbl.place(x=26, y=48)

    # Style 
    def _apply_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TCombobox",
                        fieldbackground=CARD_BG, background=CARD_BG,
                        foreground=TEXT, selectbackground=ACCENT1,
                        selectforeground=WHITE, arrowcolor=ACCENT2,
                        bordercolor=BORDER, lightcolor=CARD_BG,
                        darkcolor=CARD_BG, relief="flat",
                        padding=6)
        style.map("TCombobox",
                  fieldbackground=[("readonly", CARD_BG)],
                  foreground=[("readonly", TEXT)],
                  selectbackground=[("readonly", ACCENT1)])

    # Placeholder helpers
    def _clear_hint(self, _=None):
        if self._hint_visible:
            self.src_text.delete("1.0", "end")
            self.src_text.config(fg=TEXT)
            self._hint_visible = False

    def _restore_hint(self, _=None):
        if not self.src_text.get("1.0", "end-1c").strip():
            self.src_text.insert("1.0", self._hint_text)
            self.src_text.config(fg=TEXT_FAINT)
            self._hint_visible = True

    # Callbacks
    def _on_src_key(self, _=None):
        if self._hint_visible:
            return
        n = len(self.src_text.get("1.0", "end-1c"))
        self.char_lbl.config(text=f"{n} / 500")
        state = "normal" if n else "disabled"
        self.translate_btn.config(state=state)

    def _clear(self):
        self._clear_hint()
        self.src_text.delete("1.0", "end")
        self._restore_hint()
        self._set_output("")
        self.char_lbl.config(text="0 / 500")
        self.out_char_lbl.config(text="")
        self.translate_btn.config(state="disabled")
        self.copy_btn.config(state="disabled")
        self.speak_out_btn.config(state="disabled")
        self.detected_lbl.config(text="")
        self.status_lbl.config(text="✔  Ready — type text and press Translate",
                               fg=TEXT_DIM)
        self._translated     = ""
        self._detected_code  = None
        self._stop_anim()

    def _swap_languages(self):
        src = self.src_var.get()
        tgt = self.tgt_var.get()
        if src == "Auto-detect" and self._detected_code:
            self.src_var.set(CODE_NAMES.get(self._detected_code, tgt))
        elif src != "Auto-detect":
            self.src_var.set(tgt)
        else:
            self.src_var.set("English")

        if src == "Auto-detect":
            self.tgt_var.set("English")
        elif src in [l[0] for l in LANGUAGES if l[1] != "auto"]:
            self.tgt_var.set(src)

        if self._translated:
            self._clear_hint()
            self.src_text.delete("1.0", "end")
            self.src_text.insert("end", self._translated)
            self.src_text.config(fg=TEXT)
            self._hint_visible = False
            self._set_output("")
            self.copy_btn.config(state="disabled")
            self.speak_out_btn.config(state="disabled")
            self.translate_btn.config(state="normal")
            self._on_src_key()
        self.detected_lbl.config(text="")
        self._translated = ""

    #Translation (MyMemory free API — no key needed)
    def _translate(self, _=None):
        if self._hint_visible:
            return
        text = self.src_text.get("1.0", "end-1c").strip()
        if not text:
            return

        src  = self.src_var.get()
        tgt  = self.tgt_var.get()

        self.translate_btn.config(state="disabled", text="Translating…")
        self.copy_btn.config(state="disabled")
        self.speak_out_btn.config(state="disabled")
        self._set_output("", dim=True)
        self.status_lbl.config(text="⏳  Translating…", fg=ACCENT2)
        self._start_anim()
        self.update_idletasks()

        threading.Thread(target=self._do_translate,
                         args=(text, src, tgt), daemon=True).start()

    def _do_translate(self, text, src, tgt):
        try:
            src_code = LANG_CODES.get(src, "auto")
            tgt_code = LANG_CODES.get(tgt, "en")

            # MyMemory free translation — no key required
            # Language pair format: "en|fr"
            if src_code == "auto":
                lang_pair = f"autodetect|{tgt_code}"
            else:
                lang_pair = f"{src_code}|{tgt_code}"

            params = urllib.parse.urlencode({
                "q":       text[:500],   # MyMemory free limit ~500 chars/req
                "langpair": lang_pair,
            })
            url = f"https://api.mymemory.translated.net/get?{params}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            response_status = data.get("responseStatus", 0)
            if response_status != 200:
                err = data.get("responseDetails", "Unknown error")
                self.after(0, self._show_error, f"API error {response_status}: {err}")
                return

            translation = data["responseData"]["translatedText"]

            # Detect source language from response (best-effort)
            detected = None
            matches  = data.get("matches", [])
            if matches:
                detected_raw = matches[0].get("source-language-code", "")
                if detected_raw:
                    base = detected_raw.split("-")[0].lower()
                    detected = CODE_NAMES.get(base) or CODE_NAMES.get(detected_raw)

            self.after(0, self._show_result, translation, detected)

        except Exception as exc:
            self.after(0, self._show_error, str(exc))

    def _show_result(self, translation, detected):
        self._stop_anim()
        self._translated = translation
        self._set_output(translation)
        self.out_char_lbl.config(text=f"{len(translation)} chars")
        self.translate_btn.config(state="normal", text="  Translate  ➜")
        self.copy_btn.config(state="normal")
        self.speak_out_btn.config(state="normal")
        self.status_lbl.config(text="✅  Translation complete!", fg=GREEN)

        if detected:
            self._detected_code = LANG_CODES.get(detected)
            self.detected_lbl.config(
                text=f"✦ Detected: {detected}", fg=GREEN)
        else:
            self.detected_lbl.config(text="")

    def _show_error(self, msg):
        self._stop_anim()
        self._set_output(f"⚠  {msg}", error=True)
        self.translate_btn.config(state="normal", text="  Translate  ➜")
        self.status_lbl.config(text="❌  Translation failed", fg=RED_ERR)

    # Dot animation
    def _start_anim(self):
        self._dot_count = 0
        self._anim_step()

    def _anim_step(self):
        self._dot_count = (self._dot_count + 1) % 4
        dots = "●" * self._dot_count + "○" * (3 - self._dot_count)
        self._set_output(f"  {dots}  translating…", dim=True)
        self._anim_id = self.after(400, self._anim_step)

    def _stop_anim(self):
        if self._anim_id:
            self.after_cancel(self._anim_id)
            self._anim_id = None

    # Output helper 
    def _set_output(self, text, dim=False, error=False):
        self.out_text.config(state="normal")
        self.out_text.delete("1.0", "end")
        colour = TEXT_FAINT if dim else (RED_ERR if error else TEXT)
        self.out_text.config(fg=colour)
        self.out_text.insert("end", text)
        self.out_text.config(state="disabled")

    # Copy 
    def _copy(self):
        if not self._translated:
            return
        self.clipboard_clear()
        self.clipboard_append(self._translated)
        orig = self.copy_btn.cget("text")
        self.copy_btn.config(text="✓ Copied!", fg=GREEN)
        self.after(2000, lambda: self.copy_btn.config(text=orig, fg=YELLOW))

    # TTS
    def _speak_source(self):
        if self._hint_visible:
            return
        text = self.src_text.get("1.0", "end-1c").strip()
        if not text:
            return
        # Resolve language code for source
        src = self.src_var.get()
        if src == "Auto-detect":
            lang_code = self._detected_code or "en"
        else:
            lang_code = LANG_CODES.get(src, "en")
        threading.Thread(target=self._tts,
                         args=(text, lang_code), daemon=True).start()

    def _speak_output(self):
        if not self._translated:
            return
        tgt = self.tgt_var.get()
        lang_code = LANG_CODES.get(tgt, "en")
        threading.Thread(target=self._tts,
                         args=(self._translated, lang_code), daemon=True).start()

    def _tts(self, text, lang_code="en"):
        """Speak text using gTTS + playsound (supports Telugu & all languages).
        Falls back to Windows SAPI for English when offline."""
        import sys, tempfile, os, subprocess
        plat = sys.platform

        # Try gTTS + playsound (works for Telugu, Hindi, all Indian languages)
        try:
            from gtts import gTTS
            from playsound import playsound

            # gTTS doesn't support 'auto'; default to English
            safe_lang = lang_code if lang_code != "auto" else "en"

            tts = gTTS(text=text, lang=safe_lang, slow=False)
            tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
            tmp_path = tmp.name
            tmp.close()
            tts.save(tmp_path)

            # playsound 1.2.2 plays MP3 via Windows Media COM — no extra deps
            playsound(tmp_path, block=True)

            try:
                os.remove(tmp_path)
            except Exception:
                pass
            return  # success — done

        except ImportError as ie:
            self.after(0, lambda: self.status_lbl.config(
                text=f"💡 Run: pip install gtts playsound==1.2.2",
                fg=YELLOW))
            self.after(5000, lambda: self.status_lbl.config(
                text="✅  Translation complete!", fg=GREEN))

        except Exception as e:
            self.after(0, lambda err=e: self.status_lbl.config(
                text=f"⚠ TTS error: {err}", fg=RED_ERR))
            return

        #Fallback: Windows SAPI (English only)
        if plat == "win32":
            try:
                safe_text = text.replace('"', '').replace("'", "")
                subprocess.run(
                    ["powershell", "-Command",
                     f'Add-Type -AssemblyName System.Speech; '
                     f'(New-Object System.Speech.Synthesis.SpeechSynthesizer)'
                     f'.Speak("{safe_text}")'],
                    check=True, timeout=30)
            except Exception:
                pass
        elif plat == "darwin":
            try:
                subprocess.run(["say", text], check=True, timeout=30)
            except Exception:
                pass

# Entry point
if __name__ == "__main__":
    app = TranslatorApp()
    app.mainloop()
