# src/i18n.py
import streamlit as st

LANGS = {
    "pl": {"name": "Polski",   "flag": "🇵🇱"},
    "en": {"name": "English",  "flag": "🇬🇧"},
    "de": {"name": "Deutsch",  "flag": "🇩🇪"},
    "es": {"name": "Español",  "flag": "🇪🇸"},
    "it": {"name": "Italiano", "flag": "🇮🇹"},
}

UI = {
    "app_title":      {"pl":"Language Helper","en":"Language Helper","de":"Language Helper","es":"Language Helper","it":"Language Helper"},
    "tagline":        {"pl":"Twoja pomoc w nauce języków","en":"Your language learning assistant","de":"Dein Sprachlern-Assistent","es":"Tu asistente para aprender idiomas","it":"Il tuo assistente di lingua"},
    "nav_dashboard":  {"pl":"🏠 Panel","en":"🏠 Dashboard","de":"🏠 Übersicht","es":"🏠 Panel","it":"🏠 Dashboard"},
    "nav_flashcard":  {"pl":"🧠 Fiszka dnia","en":"🧠 Daily Flashcard","de":"🧠 Tageskarte","es":"🧠 Tarjeta del día","it":"🧠 Scheda del giorno"},
    "nav_vocab":      {"pl":"🧱 Słownictwo","en":"🧱 Vocabulary","de":"🧱 Vokabeln","es":"🧱 Vocabulario","it":"🧱 Vocabolario"},
    "nav_translator": {"pl":"🌍 Tłumacz","en":"🌍 Translator","de":"🌍 Übersetzer","es":"🌍 Traductor","it":"🌍 Traduttore"},
    "nav_exercises":  {"pl":"📝 Ćwiczenia","en":"📝 Exercises","de":"📝 Übungen","es":"📝 Ejercicios","it":"📝 Esercizi"},
    "nav_settings":   {"pl":"⚙️ Ustawienia","en":"⚙️ Settings","de":"⚙️ Einstellungen","es":"⚙️ Ajustes","it":"⚙️ Impostazioni"},
    "heading_translator": {"pl":"🌍 Tłumacz","en":"🌍 Translator","de":"🌍 Übersetzer","es":"🌍 Traductor","it":"🌍 Traduttore"},
    "heading_flashcard":  {"pl":"🧠 Fiszka dnia","en":"🧠 Daily Flashcard","de":"🧠 Tageskarte","es":"🧠 Tarjeta del día","it":"🧠 Scheda del giorno"},
}

def get_flag(code: str) -> str:
    return LANGS.get(code, {}).get("flag", "🌐")

def set_locale(code: str):
    st.session_state["locale"] = code

def t(key: str) -> str:
    code = st.session_state.get("locale", "pl")
    return UI.get(key, {}).get(code, UI.get(key, {}).get("pl", key))
