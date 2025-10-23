# 🌍 Language Helper

A modern, Streamlit-based app that helps you learn languages through daily flashcards, a built-in translator with TTS, customizable vocabulary, and practice modes.

**Live:** https://language-assistant-damiandatax.streamlit.app  
**Repo:** https://github.com/damiandatax/language-helper

---

## ✨ Features

- **🧠 Flashcard of the Day** — reveal translation on click, mark _known/unknown_, session progress bar, TTS for target language.
- **🌍 Translator** — PL↔EN/DE/ES/IT, automatic direction based on settings, history of translations, TTS of the result.
- **🧱 Vocabulary** — add your own words (auto-translate if translation empty), filter, single & bulk delete, per-language word lists.
- **📝 Exercises** — two modes:
  - **Choice (ABCD)** — randomized correct + distractors,
  - **Write** — open input with normalized answer checking.
- **📊 Dashboard** — totals, streak, progress bars, activity charts (Altair), daily goal overlay line.
- **⚙️ Settings** — select base language (UI) and learning language, set daily goal.
- **🎨 Polished UI** — custom sidebar branding with logo, language pill, rounded components.
- **👑 No Streamlit crown** — clean browser tab title only.

---

## 🧰 Tech Stack

- **Python 3.10+**
- **Streamlit** — UI & routing
- **gTTS** — text-to-speech (mp3)
- **Altair** — charts
- **Pandas** — lightweight data handling
- **Pillow** — images (assets)
- **Requests** — (used in earlier iterations; optional now)
- Standard libs: `json`, `pathlib`, `datetime`, `random`, etc.

---

## 🗂 Project Structure

language-helper/
├─ app.py
├─ src/
│ ├─ ui.py
│ ├─ storage.py
│ ├─ translator.py
│ └─ i18n.py
├─ data/
│ ├─ words.json
│ ├─ progress.json
│ └─ translations.json
├─ assets/
│ └─ logo_sidebar.png
├─ requirements.txt
└─ README.md


---

## 🚀 Run Locally

```bash
# 1) Create & activate venv (Windows)
python -m venv .venv
.venv\Scripts\activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Start app
streamlit run app.py

Then open http://localhost:8501

☁️ Deploy on Streamlit Cloud

Push this repo to GitHub.

Go to: https://share.streamlit.io

Set:

Repository: damiandatax/language-helper

Branch: main

Main file: app.py

Subdomain: language-assistant-damiandatax

Click Deploy 🚀

Your app will be live at:
👉 https://language-assistant-damiandatax.streamlit.app

📦 Data Files

data/words.json — vocabulary lists per language.

data/progress.json — progress tracking (known/unknown, streaks).

data/translations.json — saved translation history.

Example words.json:
{
  "en": [
    {"word": "apple", "translation": "jabłko"},
    {"word": "house", "translation": "dom"}
  ],
  "de": [],
  "es": [],
  "it": []
}

🗺 Roadmap

🔁 Smart spaced repetition (SRS)

📤 Export / import vocabulary

🎨 Light / dark themes

🎧 Dual-language TTS

☁️ Cloud sync for user data

🛡 License

MIT License
© 2025 Damian

🙌 Acknowledgements

Streamlit
 for the web framework

gTTS
 for text-to-speech

Altair
 for visualization