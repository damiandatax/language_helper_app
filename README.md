<p align="center">
  <img src="assets/logo_sidebar.png" alt="Language Helper Logo" width="320"/>
</p>

# 🌍 Language Helper

[🇵🇱 Czytaj po polsku](README_PL.md)

A modern, Streamlit-based app that helps you learn languages through daily flashcards, a built-in translator with TTS, customizable vocabulary, and practice modes.

**Live App:** [https://language-assistant-damiandatax.streamlit.app](https://language-assistant-damiandatax.streamlit.app)  
**GitHub Repo:** [https://github.com/damiandatax/language-helper](https://github.com/damiandatax/language-helper)

---

## ✨ Features

- 🧠 **Flashcard of the Day** — reveal translation, mark known/unknown, track progress, and listen to pronunciation.  
- 🌍 **Translator** — PL↔EN/DE/ES/IT with automatic direction and TTS.  
- 🧱 **Vocabulary Manager** — add, edit, delete, and auto-translate words.  
- 📝 **Exercises** — train vocabulary via:
  - Multiple choice (ABCD)
  - Writing mode  
- 📊 **Dashboard** — progress charts, streaks, daily goals.  
- ⚙️ **Settings** — choose base & target languages, set goals.  
- 🎨 **Modern UI** — custom logo, sidebar, consistent design.  
- 👑 **No Streamlit crown** — clean browser tab title only.  

---

## 🧰 Tech Stack

| Tool | Purpose |
|------|----------|
| **Python 3.10+** | Core language |
| **Streamlit** | Web app framework |
| **gTTS** | Text-to-speech |
| **Altair** | Charts |
| **Pandas** | Data processing |
| **Pillow** | Image handling |
| **Requests** | Translation API |

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

MIT License
© 2025 Damian

🙌 Acknowledgements

Streamlit
 for the web framework

gTTS
 for text-to-speech

Altair
 for visualization