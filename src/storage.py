from __future__ import annotations
from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any, Literal
import streamlit as st
DATA_DIR = Path("data")
PROGRESS_PATH = DATA_DIR / "progress.json"

DEFAULT_PROGRESS: Dict[str, Any] = {
    "totals": {"known": 0, "unknown": 0},
    "history": [],
}

def _ensure_files() -> None:
    """Tworzy katalog i plik z domyślną treścią, jeśli nie istnieją.
    Uwaga: NIE woła save_progress(), żeby uniknąć rekurencji.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not PROGRESS_PATH.exists():
        PROGRESS_PATH.write_text(
            json.dumps(DEFAULT_PROGRESS, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

def load_progress() -> Dict[str, Any]:
    _ensure_files()
    try:
        return json.loads(PROGRESS_PATH.read_text(encoding="utf-8"))
    except Exception:
        # jeśli plik uszkodzony – nadpisz domyślnym i zwróć
        PROGRESS_PATH.write_text(
            json.dumps(DEFAULT_PROGRESS, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return DEFAULT_PROGRESS.copy()

def save_progress(progress: Dict[str, Any]) -> None:
    # upewnij się tylko, że katalog istnieje (bez wywoływania _ensure_files)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(
        json.dumps(progress, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

def increment(word: str, result: Literal["known", "unknown"]) -> Dict[str, Any]:
    progress = load_progress()
    progress["totals"][result] = int(progress["totals"].get(result, 0)) + 1
    progress["history"].append(
        {
            "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "word": word,
            "result": result,
        }
    )
    save_progress(progress)
    return progress

def reset_progress() -> Dict[str, Any]:
    save_progress(DEFAULT_PROGRESS.copy())
    return load_progress()
# --- TRWAŁA HISTORIA TŁUMACZEŃ ---

TRANSLATIONS_PATH = DATA_DIR / "translations.json"
DEFAULT_TRANSLATIONS: Dict[str, Any] = {"items": []}

def _ensure_translations_file() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not TRANSLATIONS_PATH.exists():
        TRANSLATIONS_PATH.write_text(
            json.dumps(DEFAULT_TRANSLATIONS, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

def load_translations() -> Dict[str, Any]:
    _ensure_translations_file()
    try:
        return json.loads(TRANSLATIONS_PATH.read_text(encoding="utf-8"))
    except Exception:
        TRANSLATIONS_PATH.write_text(
            json.dumps(DEFAULT_TRANSLATIONS, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return DEFAULT_TRANSLATIONS.copy()

def save_translations(obj: Dict[str, Any]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    TRANSLATIONS_PATH.write_text(
        json.dumps(obj, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

def add_translation(direction: str, text_in: str, text_out: str, source: str = "mymemory") -> Dict[str, Any]:
    """Dodaje wpis do historii tłumaczeń i zwraca zaktualizowany obiekt."""
    data = load_translations()
    items = data.get("items", [])
    items.append({
        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "dir": direction,   # "🇵🇱 PL → EN" lub "🇬🇧 EN → PL"
        "in": text_in,
        "out": text_out,
        "source": source,
    })
    data["items"] = items
    save_translations(data)
    return data

def clear_translations() -> Dict[str, Any]:
    save_translations(DEFAULT_TRANSLATIONS.copy())
    return load_translations()

# --- SŁÓWKA ---

WORDS_PATH = DATA_DIR / "words.json"
DEFAULT_WORDS = [{"word": "apple", "translation": "jabłko"},
                 {"word": "house", "translation": "dom"},
                 {"word": "sun", "translation": "słońce"}]

def _ensure_words_file() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not WORDS_PATH.exists():
        WORDS_PATH.write_text(json.dumps(DEFAULT_WORDS, ensure_ascii=False, indent=2), encoding="utf-8")

def load_words() -> list[dict]:
    _ensure_words_file()
    try:
        return json.loads(WORDS_PATH.read_text(encoding="utf-8"))
    except Exception:
        WORDS_PATH.write_text(json.dumps(DEFAULT_WORDS, ensure_ascii=False, indent=2), encoding="utf-8")
        return DEFAULT_WORDS.copy()

def save_words(words: list[dict]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    WORDS_PATH.write_text(json.dumps(words, ensure_ascii=False, indent=2), encoding="utf-8")

def add_word(word: str, translation: str) -> list[dict]:
    """Dodaje słówko jeśli nie ma duplikatu (case-insensitive). Zwraca zaktualizowaną listę."""
    words = load_words()
    w = word.strip()
    t = translation.strip()
    if not w or not t:
        return words
    # duplikaty – porównujemy po lower()
    if any(x.get("word","").strip().lower() == w.lower() for x in words):
        return words
    words.append({"word": w, "translation": t})
    # sort alfabetyczny
    words.sort(key=lambda x: x.get("word","").lower())
    save_words(words)
    return words

def delete_word(word: str) -> list[dict]:
    words = load_words()
    nw = [x for x in words if x.get("word","").strip().lower() != (word or "").strip().lower()]
    save_words(nw)
    return nw

# --- CELE DZIENNE I POSTĘP ---

def update_daily_progress(count: int) -> dict:
    """Zwiększa licznik dzienny o 'count' i zapisuje do pliku progress.json."""
    progress = load_progress()
    today = datetime.utcnow().date().isoformat()
    if "daily" not in progress:
        progress["daily"] = {}
    progress["daily"].setdefault(today, 0)
    progress["daily"][today] += count
    save_progress(progress)
    return progress

def get_today_progress() -> tuple[int, int]:
    """Zwraca (dzisiejszy postęp, cel)"""
    progress = load_progress()
    today = datetime.utcnow().date().isoformat()
    done = int(progress.get("daily", {}).get(today, 0))
    # cel przechowujemy w session_state (ustawienia)
    goal = int(st.session_state.get("daily_goal", 20))
    return done, goal
