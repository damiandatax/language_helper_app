# src/translator.py
from __future__ import annotations
import requests

LANG_MAP = {"pl":"pl", "en":"en", "de":"de", "es":"es", "it":"it"}

class TranslationError(Exception):
    pass

def _best_from_matches(data: dict) -> str | None:
    best = None
    best_q = -1.0
    for m in data.get("matches", []):
        seg = (m.get("translation") or "").strip()
        try:
            q = float(m.get("quality") or 0)
        except Exception:
            q = 0.0
        if seg and q > best_q:
            best_q = q
            best = seg
    return best

def _call_mymemory(text: str, s: str, t: str, timeout: float = 8.0) -> dict:
    url = "https://api.mymemory.translated.net/get"
    # parametr 'de' (email) poprawia limity/zachowanie
    params = {"q": text, "langpair": f"{s}|{t}", "de": "demo@example.com"}
    r = requests.get(url, params=params, timeout=timeout)
    r.raise_for_status()
    return r.json()

def _call_libretranslate(text: str, s: str, t: str, timeout: float = 8.0) -> str | None:
    """
    Fallback na LibreTranslate (publiczne instancje bywają przeciążone).
    Podmienisz endpoint przez sekrety/env jeśli chcesz.
    """
    # możesz zmienić na swoją instancję, np. https://libretranslate.com/translate
    url = "https://libretranslate.de/translate"
    payload = {"q": text, "source": s, "target": t, "format": "text"}
    headers = {"accept": "application/json"}
    r = requests.post(url, json=payload, headers=headers, timeout=timeout)
    r.raise_for_status()
    data = r.json()
    out = (data.get("translatedText") or "").strip()
    return out or None

def translate_text(text: str, src: str, dst: str, timeout: float = 8.0) -> str:
    """
    Najpierw MyMemory, potem fallback LibreTranslate.
    Rzuca TranslationError z czytelnym komunikatem, jeśli się nie uda.
    """
    text = (text or "").strip()
    if not text:
        raise TranslationError("Brak tekstu do przetłumaczenia.")

    s = LANG_MAP.get(src, src)
    t = LANG_MAP.get(dst, dst)
    if s == t:
        return text

    # 1) MyMemory: próba główna + matches + powtórka
    try:
        data = _call_mymemory(text, s, t, timeout)
        main = (data.get("responseData") or {}).get("translatedText", "").strip()
        if main and main.lower() != text.lower():
            return main

        best = _best_from_matches(data)
        if best and best.lower() != text.lower():
            return best

        # druga próba
        data2 = _call_mymemory(text, s, t, timeout)
        main2 = (data2.get("responseData") or {}).get("translatedText", "").strip()
        if main2 and main2.lower() != text.lower():
            return main2
        best2 = _best_from_matches(data2)
        if best2 and best2.lower() != text.lower():
            return best2
    except requests.RequestException as e:
        # pomijamy – spróbujemy fallback
        pass
    except Exception:
        pass

    # 2) Fallback: LibreTranslate
    try:
        lt = _call_libretranslate(text, s, t, timeout)
        if lt and lt.lower() != text.lower():
            return lt
    except requests.RequestException:
        pass
    except Exception:
        pass

    # 3) Nic nie wyszło – zwróć czytelny błąd
    raise TranslationError(
        "API zwróciło oryginał lub wystąpił limit. Spróbuj innego zdania, "
        "zmień kierunek albo spróbuj ponownie za chwilę."
    )
