<p align="center">
  <img src="assets/logo_sidebar.png" alt="Language Helper Logo" width="320"/>
</p>

# 🌍 Language Helper

[🇬🇧 Read in English](README.md)

Nowoczesna aplikacja do nauki języków stworzona w **Python + Streamlit**, która łączy fiszki, tłumacz z wymową, naukę słówek i ćwiczenia w jednym miejscu.

**Wersja online:** [https://language-assistant-damiandatax.streamlit.app](https://language-assistant-damiandatax.streamlit.app)  
**Repozytorium GitHub:** [https://github.com/damiandatax/language_helper_app](https://github.com/damiandatax/language_helper_app)

---

## ✨ Funkcje

- 🧠 **Fiszka dnia** — odkryj tłumaczenie po kliknięciu, oznaczaj słowa jako _znam_ / _nie znam_, licz postęp sesji i odsłuchuj wymowę.
- 🌍 **Tłumacz** — obsługuje języki PL ↔ EN/DE/ES/IT z automatycznym rozpoznawaniem kierunku i dźwiękiem (TTS).
- 🧱 **Słownictwo** — zarządzaj swoimi słówkami: dodawaj, filtruj, usuwaj i automatycznie tłumacz nowe wpisy.
- 📝 **Ćwiczenia** — utrwalaj słówka w dwóch trybach:
  - **Wybór (ABCD)** — test wielokrotnego wyboru,
  - **Pisanie** — samodzielne wpisywanie tłumaczenia.
- 📊 **Panel** — statystyki nauki, wykresy postępu i seria dni z aktywnością.
- ⚙️ **Ustawienia** — wybierz język bazowy i język nauki, ustaw cel dzienny.
- 🎨 **Nowoczesny wygląd** — własne logo, dopracowany sidebar i przejrzysty układ.
- 👑 **Brak korony Streamlit** — czysty tytuł w karcie przeglądarki.

---

## 🧰 Technologie

| Technologia | Zastosowanie |
|--------------|---------------|
| **Python 3.10+** | główny język |
| **Streamlit** | interfejs aplikacji |
| **gTTS** | generowanie wymowy (text-to-speech) |
| **Altair** | wykresy i wizualizacje |
| **Pandas** | operacje na danych |
| **Pillow** | obsługa grafik |
| **Requests** | tłumaczenia (API) |

---

## 🗂 Struktura projektu

```text
language-helper/
├─ app.py
├─ src/
│  ├─ ui.py
│  ├─ storage.py
│  ├─ translator.py
│  └─ i18n.py
├─ data/
│  ├─ words.json
│  ├─ progress.json
│  └─ translations.json
├─ assets/
│  └─ logo_sidebar.png
├─ requirements.txt
└─ README_PL.md

---

## 🚀 Uruchomienie lokalne

```bash
# 1) Utwórz i aktywuj środowisko wirtualne
python -m venv .venv
.venv\Scripts\activate

# 2) Zainstaluj wymagane pakiety
pip install -r requirements.txt

# 3) Uruchom aplikację
streamlit run app.py

Następnie otwórz w przeglądarce: http://localhost:8501

☁️ Publikacja w Streamlit Cloud

Wypchnij repozytorium do GitHuba.

Wejdź na https://share.streamlit.io

Ustaw:

Repository: damiandatax/language-helper

Branch: main

Main file: app.py

Subdomain: language-assistant-damiandatax

Kliknij Deploy 🚀

Aplikacja będzie dostępna pod adresem:
👉 https://language-assistant-damiandatax.streamlit.app

📦 Pliki danych

data/words.json — lista słówek dla każdego języka

data/progress.json — zapis postępu nauki

data/translations.json — historia tłumaczeń

Przykład words.json:
{
  "en": [
    {"word": "apple", "translation": "jabłko"},
    {"word": "house", "translation": "dom"}
  ]
}

🗺 Plan rozwoju

🔁 System powtórek (SRS)

📤 Import / eksport słownictwa

🎧 Wymowa w obu językach

☁️ Synchronizacja danych w chmurze

🌙 Tryb ciemny

🛡 Licencja

MIT License
© 2025 Damian

🙌 Podziękowania

Streamlit
 — framework do aplikacji webowych

gTTS
 — synteza mowy

Altair
 — wizualizacja danych