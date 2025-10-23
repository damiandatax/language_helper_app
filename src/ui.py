# from __future__ import annotations
# import json
# import random, re
# import streamlit as st
# from src.storage import increment, load_progress, reset_progress, add_translation, load_translations, clear_translations, load_words, add_word, delete_word, update_daily_progress
# import requests
# from gtts import gTTS
# from io import BytesIO
# import pandas as pd
# import altair as alt
# from datetime import datetime, timezone, timedelta
# from pathlib import Path
# from PIL import Image
# from base64 import b64encode
# from src.i18n import t, get_flag
# from pathlib import Path
# from base64 import b64encode
# import streamlit as st
# from src.i18n import LANGS, set_locale, get_flag, t
# from src.translator import translate_text, TranslationError
# import hashlib, io
# from typing import Literal, Callable, Any, cast
# import unicodedata

# def _normalize(text: str) -> str:
#     """
#     Normalizuje tekst do porównywania:
#     - usuwa polskie znaki i akcenty,
#     - zamienia na małe litery,
#     - obcina spacje.
#     """
#     if not isinstance(text, str):
#         return ""
#     text = text.strip().lower()
#     text = unicodedata.normalize("NFKD", text)
#     text = "".join([c for c in text if not unicodedata.combining(c)])
#     return text

# def sidebar():
#     logo_path = Path(__file__).resolve().parent.parent / "assets" / "logo_sidebar.png"

#     # --- mapowanie flag ---
#     FLAGS = {"pl": "🇵🇱", "en": "🇬🇧", "de": "🇩🇪", "es": "🇪🇸", "it": "🇮🇹"}

#     base = st.session_state.get("base_code", "pl").lower()
#     targ = st.session_state.get("target_code", "en").lower()
#     lang_pill = f'{FLAGS.get(base, "")} {base.upper()} → {FLAGS.get(targ, "")} {targ.upper()}'

#     # --- STYL ---
#     st.markdown("""
#     <style>
#       /* usuń wszystkie górne pady w sidebarze */
#       [data-testid="stSidebar"] { padding-top: 0 !important; }
#       [data-testid="stSidebar"] .block-container { padding-top: 0 !important; }

#       /* BRANDING — logo maksymalnie wysoko */
#       .lh-brand {
#         position: sticky;
#         top: 0;
#         z-index: 3;
#         background: transparent;
#         display: flex;
#         flex-direction: column;
#         align-items: center;
#         padding: 0 6px;
#         margin: -38px 0 -2px 0;   /* przesuwa cały blok wyżej */
#         transform: translateY(-12px); /* jeszcze wyżej */
#       }

#       .lh-brand img {
#         width: 240px;
#         height: auto;
#         margin: 0;  /* brak odstępu pod logiem */
#         filter: drop-shadow(0 0 6px rgba(80,140,255,.35));
#         transition: transform .25s ease, filter .25s ease;
#       }
#       .lh-brand img:hover {
#         transform: scale(1.04);
#         filter: drop-shadow(0 0 10px rgba(100,170,255,.6));
#       }

#       /* tytuł */
#       .lh-title {
#         font-weight: 800;
#         font-size: 1.45rem;
#         line-height: 1.1;
#         margin: 2px 0 0 0;
#         text-align: center;
#         letter-spacing: .3px;
#       }

#       /* podtytuł */
#       .lh-sub {
#         color: #9ca3af;
#         font-size: .9rem;
#         margin: 2px 0 6px 0;
#         text-align: center;
#       }

#       /* pigułka językowa */
#       .lh-pill {
#         display: inline-flex;
#         align-items: center;
#         justify-content: center;
#         gap: 6px;
#         padding: 6px 12px;
#         border-radius: 999px;
#         background: rgba(99,102,241,.14);
#         border: 1px solid rgba(99,102,241,.25);
#         font-size: .86rem;
#         font-weight: 600;
#         color: #dbe4ff;
#         backdrop-filter: blur(2px);
#         margin-top: 4px;
#       }

#       /* separator i radio */
#       [data-testid="stSidebar"] hr { margin: 10px 0 !important; opacity: .25; }
#       [data-testid="stSidebar"] .stRadio > div { gap: 8px; }
#     </style>
#     """, unsafe_allow_html=True)

#     # --- BRANDING ---
#     if logo_path.exists():
#         b64 = b64encode(logo_path.read_bytes()).decode()
#         st.markdown(
#             f"""
#             <div class="lh-brand">
#               <img src="data:image/png;base64,{b64}" alt="Language Helper logo"/>
#               <div class="lh-title">Language Helper</div>
#               <div class="lh-sub">Twoja pomoc w nauce języków</div>
#               <div class="lh-pill">{lang_pill}</div>
#             </div>
#             """,
#             unsafe_allow_html=True
#         )

#     st.divider()

#     # --- NAVIGACJA ---
#     nav_items = [
#         ("🏠", "Panel"),
#         ("🧠", "Fiszka dnia"),
#         ("🌍", "Tłumacz"),
#         ("🧱", "Słownictwo"),
#         ("📝", "Ćwiczenia"),
#         ("⚙️", "Ustawienia"),
#     ]
#     labels = [f"{e} {t}" for e, t in nav_items]
#     page = st.radio("Nawigacja", labels, label_visibility="collapsed", key="nav_page")

#     st.divider()

#     # --- CEL TYGODNIA ---
#     weekly_goal = 100
#     weekly_progress = min(
#         int(st.session_state.get("known_count", 0)) + int(st.session_state.get("unknown_count", 0)),
#         weekly_goal
#     )
#     pct = (weekly_progress / weekly_goal) if weekly_goal else 0

#     st.markdown('<div class="lh-section-title">Cel tygodnia</div>', unsafe_allow_html=True)
#     st.progress(pct, text=f"{weekly_progress}/{weekly_goal}")

#     return page

# def page_dashboard():
#     st.header("🏠 Panel")
#     st.caption("Statystyki nauki • Wykres aktywności • Ostatnie odpowiedzi")
#     st.divider()

#     # dane
#     progress = load_progress()
#     known = int(progress["totals"]["known"])
#     unknown = int(progress["totals"]["unknown"])
#     total = known + unknown
#     progress_ratio = (known / total) if total else 0.0

#     tab_sum, tab_chart, tab_hist = st.tabs(["📊 Podsumowanie", "📈 Wykres", "📜 Historia"])

#     with tab_sum:
#         c1, c2, c3 = st.columns([1, 1, 1])
#         c1.metric("✅ Znane słowa", known)
#         c2.metric("❌ Nieznane słowa", unknown)
#         c3.metric("🔥 Streak (dni z aktywnością)", _streak_days(progress))

#         st.progress(progress_ratio, text=f"Postęp: {progress_ratio*100:.0f}%")
#         st.write("")  # spacing

#         col_btn = st.columns([1, 3])[0]
#         if col_btn.button("♻️ Resetuj postęp"):
#             p = reset_progress()
#             st.session_state.known_count = int(p["totals"]["known"])
#             st.session_state.unknown_count = int(p["totals"]["unknown"])
#             st.success("Zresetowano postęp.")

#         if total == 0:
#             st.info("Zagraj w **Fiszka dnia**, żeby rozpocząć naukę 💡")

#     with tab_chart:
#         st.subheader("📈 Aktywność w czasie")

#     # Wybór zakresu (7, 14, 30 dni)
#     col_range = st.columns([2, 6])[0]
#     range_days = col_range.radio(
#         "Zakres dni",
#         options=[7, 14, 30],
#         index=0,
#         horizontal=True,
#         key="chart_range_days"
#     )

#     df = _history_to_df(progress, days=range_days)

#     if df.empty:
#         st.caption("Brak danych – zacznij od Fiszki dnia.")
#     else:
#         chart = alt.Chart(df).mark_bar().encode(
#             x=alt.X("date:T", title="Data"),
#             y=alt.Y("count:Q", title="Liczba odpowiedzi"),
#             color=alt.Color(
#                 "result:N",
#                 title="Typ",
#                 scale=alt.Scale(scheme="tableau10"),
#                 legend=alt.Legend(labelExpr="datum.value == 'known' ? 'Znam' : 'Nie znam'")
#             ),
#             tooltip=[
#                 alt.Tooltip("date:T", title="Data"),
#                 alt.Tooltip("count:Q", title="Liczba"),
#                 alt.Tooltip("result:N", title="Typ"),
#             ],
#         ).properties(height=260)
#         st.altair_chart(chart, use_container_width=True)
#         st.markdown("—")
#     st.subheader("🎯 Dzienne przerobione słówka")

#     # przełącznik zakresu dziennego (możesz użyć tego samego co wyżej, jeśli chcesz)
#     col_days = st.columns([2, 6])[0]
#     daily_range = col_days.radio(
#         "Zakres dni", options=[7, 14, 30], index=0, horizontal=True, key="daily_range_days"
#     )

#     df_daily = _daily_progress_df(progress, days=daily_range)
#     goal = int(st.session_state.get("daily_goal", 20))

#     if df_daily.empty:
#         st.caption("Brak danych dziennych.")
#     else:
#         # słupki: ile przerobione danego dnia
#         bars = alt.Chart(df_daily).mark_bar().encode(
#             x=alt.X("date:T", title="Data"),
#             y=alt.Y("done:Q", title="Przerobione słówka"),
#             tooltip=[
#                 alt.Tooltip("date:T", title="Data"),
#                 alt.Tooltip("done:Q", title="Przerobione"),
#             ],
#         )

#         # linia celu dziennego (pozioma)
#         rule_df = pd.DataFrame({"y": [goal]})
#         rule = alt.Chart(rule_df).mark_rule(strokeDash=[6,4]).encode(y="y:Q")

#         # etykieta celu (opcjonalnie)
#         text = alt.Chart(rule_df).mark_text(align="left", dx=5, dy=-5).encode(
#             y="y:Q",
#             text=alt.value(f"Cel: {goal}")
#         )

#         st.altair_chart((bars + rule + text).properties(height=240), use_container_width=True)


#     with tab_hist:
#         st.subheader("Ostatnie odpowiedzi (do 20)")
#         items = progress.get("history", [])
#         if not items:
#             st.caption("Brak odpowiedzi w historii.")
#         else:
#             for it in items[::-1][:20]:
#                 badge = "✅ znam" if it.get("result") == "known" else "❌ nie znam"
#                 ts = it.get("timestamp", "")
#                 word = it.get("word", "")
#                 st.markdown(f"- {ts} • **{word}** — {badge}")



# def page_vocab():
#     import streamlit as st
#     import json
#     from pathlib import Path
#     from src.translator import translate_text, TranslationError  # do auto-tłumaczenia

#     st.header("🧱 Słownictwo")

#     # Język nauki i bazowy (dla auto-tłumaczenia)
#     lang = st.session_state.get("target_code", "en").lower()
#     base = st.session_state.get("base_code", "pl").lower()
#     data_path = Path("data") / "words.json"

#     if not data_path.exists():
#         st.error("Brak pliku data/words.json")
#         return

#     # --- wczytaj bazę ---
#     try:
#         with open(data_path, "r", encoding="utf-8") as f:
#             all_words = json.load(f)
#         words = list(all_words.get(lang, []))
#     except Exception as e:
#         st.error(f"Nie można wczytać słówek: {e}")
#         return

#     st.caption(f"Aktualny język: **{lang.upper()}** (bazowy: {base.upper()})")

#     # ============== DODAWANIE NOWEGO SŁÓWKA ==============
#     with st.expander("➕ Dodaj nowe słówko", expanded=False):
#         new_word_key = f"new_word_{lang}"
#         new_tr_key   = f"new_tr_{lang}"

#         # pola wejściowe (bez .strip() tutaj!)
#         c1, c2, c3 = st.columns([2, 2, 1])
#         with c1:
#             st.text_input(
#                 "Słówko w języku docelowym",
#                 key=new_word_key,
#                 placeholder="np. apple / Haus / sol / libro"
#             )
#         with c2:
#             st.text_input(
#                 f"Tłumaczenie ({base.upper()}) — opcjonalnie",
#                 key=new_tr_key,
#                 placeholder="np. jabłko / dom / słońce / książka"
#             )

#         # callback dodawania (tu czyścimy pola i robimy rerun)
#         def _add_word_cb():
#             # odczyt + sanity
#             word = (st.session_state.get(new_word_key) or "").strip()
#             tr   = (st.session_state.get(new_tr_key) or "").strip()

#             if not word:
#                 st.session_state["__vocab_msg__"] = ("warn", "Podaj słówko w języku docelowym.")
#                 return

#             # sprawdź duplikat (po słowie docelowym)
#             exists = any((w.get("word","").strip().lower() == word.lower()) for w in words)
#             if exists:
#                 st.session_state["__vocab_msg__"] = ("info", "Takie słówko już istnieje na liście.")
#                 return

#             # auto-tłumaczenie jeśli brak
#             if not tr:
#                 try:
#                     from src.translator import translate_text, TranslationError
#                     tr = translate_text(word, lang, base)
#                 except Exception:
#                     tr = "—"

#             # zapis do pliku
#             try:
#                 words.append({"word": word, "translation": tr})
#                 all_words[lang] = words
#                 with open(data_path, "w", encoding="utf-8") as f:
#                     json.dump(all_words, f, ensure_ascii=False, indent=2)

#                 # komunikat + wyczyszczenie pól (TERAZ dopiero modyfikujemy state)
#                 st.session_state["__vocab_msg__"] = ("ok", f"Dodano: **{word}** → {tr}")
#                 st.session_state[new_word_key] = ""
#                 st.session_state[new_tr_key] = ""
                
#             except Exception as e:
#                 st.session_state["__vocab_msg__"] = ("err", f"Nie udało się zapisać: {e}")

#         # przycisk z callbackiem
#         st.button("Dodaj", type="primary", key=f"add_{lang}", on_click=_add_word_cb)

#         # wyświetl ostatni komunikat (jeśli jest)
#         msg = st.session_state.get("__vocab_msg__")
#         if msg:
#             kind, text = msg
#             if kind == "ok":
#                 st.success(text)
#             elif kind == "warn":
#                 st.warning(text)
#             elif kind == "info":
#                 st.info(text)
#             else:
#                 st.error(text)

#     # ============== FILTR ==============
#     q = st.text_input(
#         "🔎 Filtruj słówka",
#         value="",
#         placeholder="Wpisz fragment słowa lub tłumaczenia…",
#         key=f"filter_{lang}",
#     ).strip().lower()

#     # widok par (indeks, element) — unikalne klucze
#     if q:
#         view_pairs = [(i, w) for i, w in enumerate(words)
#                       if q in w.get("word","").lower() or q in w.get("translation","").lower()]
#     else:
#         view_pairs = list(enumerate(words))

#     st.session_state.setdefault("vocab_selected_to_delete", set())

#     st.markdown("#### Lista słówek")
#     if not view_pairs:
#         st.info("Brak słówek (lub nic nie pasuje do filtra).")
#         return

#     # ============== LISTA + USUWANIE POJEDYNCZE ==============
#     for orig_idx, item in view_pairs:
#         cols = st.columns([0.7, 3, 3, 1.2])
#         with cols[0]:
#             key_cb = f"vsel_{lang}_{orig_idx}"
#             checked = orig_idx in st.session_state.vocab_selected_to_delete
#             new_checked = st.checkbox("", value=checked, key=key_cb)
#             if new_checked:
#                 st.session_state.vocab_selected_to_delete.add(orig_idx)
#             else:
#                 st.session_state.vocab_selected_to_delete.discard(orig_idx)
#         with cols[1]:
#             st.write(f"**{item.get('word','')}**")
#         with cols[2]:
#             st.write(item.get("translation", "—"))
#         with cols[3]:
#             if st.button("🗑️ Usuń", key=f"del_{lang}_{orig_idx}"):
#                 try:
#                     words.pop(orig_idx)
#                     all_words[lang] = words
#                     with open(data_path, "w", encoding="utf-8") as f:
#                         json.dump(all_words, f, ensure_ascii=False, indent=2)
#                     st.session_state.vocab_selected_to_delete.discard(orig_idx)
#                     st.success("Usunięto słowo.")
#                     st.rerun()
#                 except Exception as e:
#                     st.error(f"Nie udało się usunąć: {e}")

#     st.divider()

#     # ============== USUWANIE ZBIORCZE ==============
#     selected = sorted(st.session_state.vocab_selected_to_delete)
#     if selected:
#         st.warning(f"Zaznaczonych do usunięcia: **{len(selected)}**")
#         c1, c2 = st.columns([1, 2])
#         with c1:
#             confirm = st.checkbox("Potwierdzam usunięcie", key=f"confirm_bulk_{lang}")
#         with c2:
#             if st.button("🗑️ Usuń zaznaczone", key=f"del_bulk_{lang}"):
#                 if not confirm:
#                     st.info("Zaznacz najpierw potwierdzenie.")
#                 else:
#                     try:
#                         for i in sorted(selected, reverse=True):
#                             if 0 <= i < len(words):
#                                 words.pop(i)
#                         all_words[lang] = words
#                         with open(data_path, "w", encoding="utf-8") as f:
#                             json.dump(all_words, f, ensure_ascii=False, indent=2)
#                         st.session_state.vocab_selected_to_delete.clear()
#                         st.success("Usunięto zaznaczone słowa.")
#                         st.rerun()
#                     except Exception as e:
#                         st.error(f"Nie udało się usunąć zaznaczonych: {e}")
#     else:
#         st.caption("Zaznacz wiersze po lewej, aby usunąć wiele naraz.")



# # =========================
# # ĆWICZENIA — HELPERY
# # =========================

# def _load_words_for_lang(lang_code: str):
#     """Zwraca listę słówek (dict: {word, translation}) dla danego języka docelowego."""
#     import json
#     from pathlib import Path
#     path = Path("data") / "words.json"
#     try:
#         with open(path, "r", encoding="utf-8") as f:
#             data = json.load(f)
#     except Exception:
#         return []
#     if isinstance(data, dict):
#         return list(data.get(lang_code, []))
#     elif isinstance(data, list):
#         return data
#     return []


# def _register_answer(ok: bool, user_answer: str):
#     """Zapisz wynik odpowiedzi + czas reakcji + serię i historię."""
#     import time
#     import streamlit as st

#     # czas w ms
#     ms = 0
#     if st.session_state.get("ex_started_at") is not None:
#         ms = int((time.time() - st.session_state["ex_started_at"]) * 1000)

#     # statystyki
#     st.session_state["ex_total"] += 1
#     if ok:
#         st.session_state["ex_correct"] += 1
#         st.session_state["ex_streak"] += 1
#     else:
#         st.session_state["ex_streak"] = 0

#     # historia
#     st.session_state["ex_history"].append({
#         "q": st.session_state.get("ex_question"),
#         "a": st.session_state.get("ex_answer"),
#         "u": user_answer,
#         "ok": ok,
#         "ms": ms,
#     })


# def _new_exercise_question(words, direction: str, mode: str):
#     """
#     words: LISTA {"word": "...", "translation": "..."}
#     direction: "to_base" (pytanie = word, odp = translation) lub "to_target"
#     mode: "choice" (ABCD) lub "write"
#     """
#     import random, time
#     import streamlit as st

#     # 1) losowanie elementu
#     item = random.choice(words)
#     src = item.get("word", "")
#     dst = item.get("translation", "")

#     if direction == "to_target":
#         question, answer = dst, src
#     else:  # "to_base"
#         question, answer = src, dst

#     # 2) zapis do stanu
#     st.session_state["ex_question"] = question
#     st.session_state["ex_answer"] = answer

#     # 3) opcje dla trybu choice
#     if mode == "choice":
#         pool = []
#         for w in words:
#             s, d = w.get("word", ""), w.get("translation", "")
#             pool.append(d if direction == "to_base" else s)

#         pool = [p for p in pool if p and p != answer]
#         if len(pool) < 3 and pool:
#             while len(pool) < 3:
#                 pool.append(random.choice(pool))

#         options = [answer]
#         if pool:
#             options += random.sample(pool, k=min(3, len(pool)))
#         while len(options) < 4:
#             options.append("—")
#         random.shuffle(options)
#         st.session_state["ex_choices"] = options
#     else:
#         st.session_state["ex_choices"] = None

#     # 4) start timera + nowy identyfikator pytania (do kluczy widgetów)
#     st.session_state["ex_started_at"] = time.time()
#     st.session_state["ex_qid"] = st.session_state.get("ex_qid", 0) + 1


# # =========================
# # GŁÓWNA STRONA ĆWICZEŃ
# # =========================

# def page_exercises():
#     import streamlit as st

#     st.header("📝 Ćwiczenia")

#     # --- stan ćwiczeń (inicjalizacja) ---
#     st.session_state.setdefault("ex_question", None)
#     st.session_state.setdefault("ex_answer", None)
#     st.session_state.setdefault("ex_choices", None)
#     st.session_state.setdefault("ex_total", 0)
#     st.session_state.setdefault("ex_correct", 0)
#     st.session_state.setdefault("ex_streak", 0)
#     st.session_state.setdefault("ex_history", [])
#     st.session_state.setdefault("ex_started_at", None)
#     st.session_state.setdefault("ex_qid", 0)
#     st.session_state.setdefault("ex_prev_lang", None)
#     st.session_state.setdefault("ex_prev_mode", None)
#     st.session_state.setdefault("ex_prev_dir", None)

#     # --- słówka dla aktywnego języka ---
#     lang = st.session_state.get("target_code", "en")
#     base = st.session_state.get("base_code", "pl")
#     words = _load_words_for_lang(lang)
#     if not words:
#         st.info("Brak słówek dla bieżącego języka. Dodaj je w zakładce **Słownictwo**.")
#         return

#     # --- tryb i kierunek ---
#     c1, c2, c3 = st.columns([1.2, 1.2, 1])
#     with c1:
#         mode_label = st.radio("Tryb", ["Wybór (ABCD)", "Pisanie"], horizontal=True, key="ex_mode_label")
#         mode = "choice" if mode_label == "Wybór (ABCD)" else "write"
#     with c2:
#         dir_label = st.radio("Kierunek", ["Docelowy → Bazowy", "Bazowy → Docelowy"], horizontal=True, key="ex_dir_label")
#         direction = "to_base" if dir_label == "Docelowy → Bazowy" else "to_target"
#     with c3:
#         st.caption(f"Słówka: **{len(words)}**")

#     if mode == "choice" and len(words) < 4:
#         st.warning("Za mało słówek dla trybu wyboru (min. 4). Przełączam na **Pisanie**.")
#         mode = "write"

#     # --- jeśli zmienił się język / tryb / kierunek -> natychmiast nowe pytanie ---
#     changed = (
#         st.session_state["ex_prev_lang"] != lang or
#         st.session_state["ex_prev_mode"] != mode or
#         st.session_state["ex_prev_dir"]  != direction
#     )

#     st.session_state["ex_prev_lang"] = lang
#     st.session_state["ex_prev_mode"] = mode
#     st.session_state["ex_prev_dir"]  = direction

#     if changed:
#         st.session_state["ex_question"] = None
#         st.session_state["ex_answer"] = None
#         st.session_state["ex_choices"] = None
#         _new_exercise_question(words, direction, mode)

#     # --- reset statystyk ---
#     if st.button("♻️ Resetuj statystyki"):
#         st.session_state["ex_total"] = 0
#         st.session_state["ex_correct"] = 0
#         st.session_state["ex_streak"] = 0
#         st.session_state["ex_history"] = []
#         st.session_state["ex_started_at"] = None
#         st.success("Wyzerowano statystyki ćwiczeń.")

#     # --- dashboard wyników ---
#     colA, colB, colC, colD = st.columns(4)
#     acc = (st.session_state["ex_correct"] / st.session_state["ex_total"] * 100) if st.session_state["ex_total"] else 0
#     colA.metric("Poprawne", st.session_state["ex_correct"])
#     colB.metric("Wszystkie", st.session_state["ex_total"])
#     colC.metric("Skuteczność", f"{acc:.0f}%")
#     if st.session_state["ex_history"]:
#         avg_ms = sum(h.get("ms", 0) for h in st.session_state["ex_history"]) / max(1, len(st.session_state["ex_history"]))
#     else:
#         avg_ms = 0
#     colD.metric("Śr. czas", f"{int(avg_ms)} ms")
#     st.caption(f"🔥 Seria: **{st.session_state['ex_streak']}**")
#     st.divider()

#     # --- pierwsze pytanie (jeśli brak) ---
#     if st.session_state["ex_question"] is None:
#         _new_exercise_question(words, direction, mode)

#     # --- pytanie ---
#     st.subheader("Pytanie")
#     st.write(st.session_state["ex_question"])
#     result_placeholder = st.empty()
#     next_col1, next_col2 = st.columns([1, 1])

#     def _next():
#         result_placeholder.empty()
#         _new_exercise_question(words, direction, mode)

#     # --- tryb choice ---
#     if mode == "choice":
#         options = st.session_state.get("ex_choices") or []
#         choice_key = f"ex_choice_val_{st.session_state['ex_qid']}"
#         user_choice = st.radio(
#             "Wybierz odpowiedź:",
#             options,
#             index=0 if options else None,
#             key=choice_key
#         ) or ""

#         with next_col1:
#             if st.button("Sprawdź", type="primary", key=f"ex_check_choice_{st.session_state['ex_qid']}"):
#                 correct = st.session_state.get("ex_answer", "")
#                 if _normalize(user_choice) == _normalize(correct):
#                     result_placeholder.success("✅ Dobrze!")
#                     _register_answer(True, user_choice)
#                 else:
#                     result_placeholder.error(f"❌ Źle. Poprawna odpowiedź: **{correct}**")
#                     _register_answer(False, user_choice)

#         with next_col2:
#             st.button("Następne pytanie", key=f"ex_next_choice_{st.session_state['ex_qid']}", on_click=_next)

#     # --- tryb write ---
#     else:
#         input_key = f"ex_user_input_{st.session_state['ex_qid']}"
#         st.text_input("Twoja odpowiedź:", key=input_key, placeholder="Wpisz tłumaczenie…")

#         with next_col1:
#             if st.button("Sprawdź", type="primary", key=f"ex_check_write_{st.session_state['ex_qid']}"):
#                 user = _normalize(st.session_state.get(input_key) or "")
#                 answ = _normalize(st.session_state.get("ex_answer") or "")
#                 ok = bool(user) and (user == answ)
#                 if ok:
#                     result_placeholder.success("✅ Dobrze!")
#                 else:
#                     result_placeholder.error(f"❌ Źle. Poprawna odpowiedź: **{st.session_state['ex_answer']}**")
#                 _register_answer(ok, user)

#         with next_col2:
#             st.button("Następne pytanie", key=f"ex_next_write_{st.session_state['ex_qid']}", on_click=_next)

#     # --- historia ---
#     hist = st.session_state.get("ex_history", [])
#     if hist:
#         st.markdown("### Ostatnie odpowiedzi")
#         for h in hist[-5:][::-1]:
#             tag = "✅" if h["ok"] else "❌"
#             st.caption(f"{tag} {h['q']} → **{h['a']}**  •  Ty: _{h['u'] or '—'}_  •  {h['ms']} ms")


# def _after_answer(was_correct: bool) -> None:
#     """Aktualizacja wyniku sesji i dziennego postępu po sprawdzeniu."""
#     st.session_state.ex_total += 1
#     if was_correct:
#         st.session_state.ex_correct += 1
#     # zaliczamy każde pytanie jako „przerobione” w sensie dziennego celu
#     update_daily_progress(1)

# def _check_typed_answer(user_answer: str, correct_answer: str) -> None:
#     ua = _normalize(user_answer)
#     ca = _normalize(correct_answer)
#     ok = ua != "" and (ua == ca)
#     st.session_state.ex_answered = True
#     st.session_state.ex_was_correct = ok
#     _after_answer(ok)

# def _check_choice_answer(choice: str, correct_answer: str) -> None:
#     ok = _normalize(choice) == _normalize(correct_answer)
#     st.session_state.ex_answered = True
#     st.session_state.ex_was_correct = ok
#     _after_answer(ok)


# def page_settings():
#     st.header("⚙️ Ustawienia")
#     st.subheader("🌍 Wybór języków")

#     # listy dla selectboxów
#     target_options = [("en","Angielski"), ("de","Niemiecki"), ("es","Hiszpański"), ("it","Włoski")]
#     base_options   = [("pl","Polski"), ("en","Angielski"), ("de","Niemiecki"), ("es","Hiszpański"), ("it","Włoski")]

#     # aktualne wartości (domyślne)
#     st.session_state.setdefault("base_code", "pl")
#     st.session_state.setdefault("target_code", "en")

#     # render selectboxów z flagami
#     def _fmt(opt): code, name = opt; return f"{get_flag(code)}  {name}"

#     base_idx   = [i for i,(c,_) in enumerate(base_options)   if c==st.session_state.base_code][0]
#     target_idx = [i for i,(c,_) in enumerate(target_options) if c==st.session_state.target_code][0]

#     base_sel = st.selectbox("Język bazowy (interfejs):", base_options, index=base_idx, format_func=_fmt)
#     targ_sel = st.selectbox("Język, którego się uczysz:", target_options, index=target_idx, format_func=_fmt)

#     st.session_state.base_code   = base_sel[0]
#     st.session_state.target_code = targ_sel[0]

#     # ustaw język interfejsu = bazowy
#     set_locale(st.session_state.base_code)

#     st.markdown("---")
#     st.subheader("🎯 Cel nauki")
#     st.number_input("Dzienny cel (minuty):", 5, 180, value=20, step=5, key="daily_goal")

#     st.success(
#         f"Interfejs: {get_flag(st.session_state.base_code)} "
#         f"{LANGS[st.session_state.base_code]['name']} • "
#         f"Nauka: {get_flag(st.session_state.target_code)} "
#         f"{LANGS[st.session_state.target_code]['name']}"
#     )

# @st.cache_data(show_spinner=False)
# def _tts_bytes(text: str, lang: str) -> bytes:
#     """
#     Zwraca MP3 (bytes) z wymową `text` w języku `lang` (kody gTTS: en/de/es/it/pl).
#     """
#     # prosty cache-klucz – gdybyś chciał dodatkowego poziomu
#     h = hashlib.md5(f"{lang}:{text}".encode("utf-8")).hexdigest()
#     buf = io.BytesIO()
#     gTTS(text=text, lang=lang).write_to_fp(buf)
#     buf.seek(0)
#     return buf.read()


# def page_flashcard():
#     import streamlit as st
#     import json, random
#     from pathlib import Path
#     from datetime import datetime

#     try:
#         from src.storage import increment  # zapis postępu
#     except Exception:
#         increment = None

#     st.header("🧠 Fiszka dnia")

#     # --- wczytaj słówka dla bieżącego języka ---
#     target = st.session_state.get("target_code", "en")
#     data_path = Path("data") / "words.json"
#     if not data_path.exists():
#         st.error("Brak pliku data/words.json")
#         return

#     try:
#         with open(data_path, "r", encoding="utf-8") as f:
#             all_words = json.load(f)
#         words = all_words.get(target, []) if isinstance(all_words, dict) else all_words
#     except Exception as e:
#         st.error(f"Nie można wczytać słówek: {e}")
#         return

#     if not words:
#         st.info("Brak słówek dla tego języka. Dodaj w zakładce **Słownictwo**.")
#         return

#     # --- stan fiszek ---
#     st.session_state.setdefault("fc_order", random.sample(range(len(words)), k=len(words)))
#     st.session_state.setdefault("fc_idx", 0)
#     st.session_state.setdefault("fc_show_translation", False)  # 🔹 domyślnie ukryte
#     st.session_state.setdefault("known_count", 0)
#     st.session_state.setdefault("unknown_count", 0)
#     st.session_state.setdefault("ex_qid", 0)  # rośnie przy każdym nowym pytaniu

#     # bieżąca karta
#     if st.session_state.fc_idx >= len(st.session_state.fc_order):
#         st.session_state.fc_idx = 0
#         random.shuffle(st.session_state.fc_order)

#     card = words[st.session_state.fc_order[st.session_state.fc_idx]]
#     w = card.get("word", "")
#     t = card.get("translation", "—")

#     # --- UI karty ---
#     # mapowanie na kody gTTS
#     gtts_map = {"en": "en", "de": "de", "es": "es", "it": "it", "pl": "pl"}
#     dst_gtts = gtts_map.get(target)  # target = st.session_state.get("target_code", "en")

#     # Słówko + przycisk głośnika obok
#     c_word, c_audio = st.columns([5, 1])
#     with c_word:
#         st.subheader(w)

#     with c_audio:
#     # tylko jeśli gTTS ma ten język
#         if dst_gtts:
#             if st.button("🔊", help="Odsłuch wymowy", key=f"fc_tts_{st.session_state.fc_idx}"):
#                 try:
#                     audio_bytes = _tts_bytes(w, dst_gtts)
#                     st.audio(audio_bytes, format="audio/mp3")
#                 except Exception as e:
#                     st.info(f"Nie udało się wygenerować wymowy: {e}")


#     # 🔹 przycisk pokazania tłumaczenia
#     if not st.session_state.fc_show_translation:
#         if st.button("👀 Pokaż tłumaczenie"):
#             st.session_state.fc_show_translation = True
#             st.rerun()
#     else:
#         st.success(t)

#         # przyciski akcji
#         c1, c2, c3 = st.columns([1, 1, 1])

#         def _mark(result: Literal["known", "unknown"]) -> None:
#             if result == "known":
#                 st.session_state.known_count += 1
#             else:
#                 st.session_state.unknown_count += 1

#             # zapis postępu, jeśli masz increment
#             if callable(increment):
#                 inc = cast(Callable[..., Any], increment)
#                 try:
#                     inc(result=result, word=w)     # zgodne z sygnaturą
#                 except TypeError:
#                     inc(result, w)                 # alternatywna sygnatura
#                 except Exception:
#                     pass

#             st.session_state.fc_idx += 1
#             st.session_state.fc_show_translation = False
#             st.rerun()

#         with c1:
#             if st.button("✅ Znam"):
#                 _mark("known")
#         with c2:
#             if st.button("❌ Nie znam"):
#                 _mark("unknown")
#         with c3:
#             if st.button("🔁 Następne"):
#                 st.session_state.fc_idx += 1
#                 st.session_state.fc_show_translation = False
#                 st.rerun()

#     st.divider()

#     # --- postęp ---
#     total_seen = st.session_state.known_count + st.session_state.unknown_count
#     if total_seen > 0:
#         ratio = st.session_state.known_count / total_seen
#         st.progress(ratio, text=f"Postęp tej sesji: {ratio*100:.0f}% (✅ {st.session_state.known_count} • ❌ {st.session_state.unknown_count})")
#     else:
#         st.info("Kliknij **Pokaż tłumaczenie**, aby rozpocząć sesję.")

   


# def page_translator():
#     import streamlit as st
#     from datetime import datetime
#     from gtts import gTTS
#     import hashlib, io
#     from src.translator import translate_text, TranslationError

#     # --- inicjalizacja stanu ---
#     st.session_state.setdefault("translations", [])
#     st.session_state.setdefault("tr_src", "")

#     st.header("🌍 Tłumacz")

#     # Pobierz aktualne języki
#     base = st.session_state.get("base_code", "pl")
#     targ = st.session_state.get("target_code", "en")

#     FLAGS = {"pl": "🇵🇱", "en": "🇬🇧", "de": "🇩🇪", "es": "🇪🇸", "it": "🇮🇹"}

#     base = st.session_state.get("base_code", "pl")
#     targ = st.session_state.get("target_code", "en")

#     label0 = f"{FLAGS[base]} {base.upper()} → {FLAGS[targ]} {targ.upper()}"
#     label1 = f"{FLAGS[targ]} {targ.upper()} → {FLAGS[base]} {base.upper()}"

#     # Używamy opcji 0/1 i czytelnych etykiet — wybór nie opiera się na startswith/emoji
#     dir_idx = st.radio("Kierunek", options=[0, 1], index=0, format_func=lambda i: label0 if i == 0 else label1)

#     # Kierunek pewny co do bitu
#     if dir_idx == 0:
#         src_lang, dst_lang = base, targ
#     else:
#         src_lang, dst_lang = targ, base
#     # placeholder zależny od języka źródłowego
#     ph = "Wpisz zdanie..." if src_lang == "pl" else "Type a sentence..."

#     # pole tekstowe
#     src_text = st.text_area("Tekst źródłowy", key="tr_src", height=120, placeholder=ph)

#     # --- przyciski ---
#     col1, col2 = st.columns(2)

#     with col1:
#         if st.button("Przetłumacz", type="primary"):
#             txt = st.session_state["tr_src"].strip()
#             if not txt:
#                 st.warning("Podaj tekst do tłumaczenia.")
#             else:
#                 try:
#                     result = translate_text(txt, src_lang, dst_lang)
#                     st.success(result)

#                     # 🧠 zapisz tłumaczenie w historii
#                     st.session_state["translations"].append({
#                         "src": txt,
#                         "dst": result,
#                         "dir": f"{src_lang.upper()}→{dst_lang.upper()}",
#                         "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#                     })

#                     # 🔊 generowanie dźwięku (gTTS)
#                     def _tts_bytes(text: str, lang: str) -> bytes:
#                         h = hashlib.md5(f"{lang}:{text}".encode("utf-8")).hexdigest()
#                         if f"tts_{h}" in st.session_state:
#                             return st.session_state[f"tts_{h}"]
#                         mp3 = io.BytesIO()
#                         gTTS(text=text, lang=lang).write_to_fp(mp3)
#                         mp3.seek(0)
#                         data = mp3.read()
#                         st.session_state[f"tts_{h}"] = data
#                         return data

#                     gtts_map = {"en": "en", "pl": "pl", "de": "de", "es": "es", "it": "it"}
#                     dst_gtts = gtts_map.get(dst_lang)

#                     if dst_gtts:
#                         audio_bytes = _tts_bytes(result, dst_gtts)
#                         st.audio(audio_bytes, format="audio/mp3")

#                 except TranslationError as e:
#                     st.error(str(e))
#                 except Exception as e:
#                     st.error(f"Nieoczekiwany błąd tłumaczenia: {e}")

#     # --- przycisk czyszczenia pola ---
#     def _clear_src():
#         st.session_state["tr_src"] = ""

#     with col2:
#         st.button("Wyczyść", on_click=_clear_src)

#     # --- HISTORIA TŁUMACZEŃ ---
#     history = st.session_state.get("translations", [])
#     st.markdown("### Historia tłumaczeń (ostatnie 5)")

#     if not history:
#         st.caption("Brak pozycji w historii.")
#     else:
#         for item in history[-5:][::-1]:
#             head = item["src"][:60] + ("…" if len(item["src"]) > 60 else "")
#             st.caption(f'{item.get("ts","")} • {item.get("dir","")}')
#             with st.expander(head):
#                 col_a, col_b = st.columns(2)
#                 with col_a:
#                     st.write("**Źródło**")
#                     st.write(item["src"])
#                 with col_b:
#                     st.write("**Wynik**")
#                     st.success(item["dst"])



   
    

# def _translate_and_show(text_in: str, direction: str):
#     text_in = (text_in or "").strip()
#     if not text_in:
#         st.warning("Wpisz tekst, który chcesz przetłumaczyć.")
#         return
#     try:
#         url = "https://api.mymemory.translated.net/get"
#         params = {"q": text_in, "langpair": "pl|en"} if direction == "🇵🇱 PL → EN" \
#                  else {"q": text_in, "langpair": "en|pl"}
#         r = requests.get(url, params=params, timeout=15)
#         r.raise_for_status()
#         data = r.json()
#         translation = data["responseData"]["translatedText"]

#         # 1) natychmiast pokaż w UI
#         st.success(translation)
#         st.session_state["translations"].append(
#             {"dir": direction, "in": text_in, "out": translation}
#         )
#         # 2) zapisz TRWALE do pliku
#         add_translation(direction, text_in, translation, source="mymemory")

#     except Exception as e:
#         st.error(f"Błąd podczas tłumaczenia: {e}")

# @st.cache_data(show_spinner=False)
# def _tts_en_bytes(text: str) -> bytes:
#     tts = gTTS(text=text, lang="en")
#     buf = BytesIO()
#     tts.write_to_fp(buf)
#     return buf.getvalue()

# def _last_english_result() -> str | None:
#     for item in reversed(st.session_state.get("translations", [])):
#         if item.get("dir") == "🇵🇱 PL → EN":
#             return item.get("out")
#     return None

# def _normalize_translations_in_state() -> None:
#     raw = st.session_state.get("translations", [])
#     normalized = []
#     for it in raw if isinstance(raw, list) else []:
#         if isinstance(it, dict):
#             if {"dir", "in", "out"} <= set(it.keys()):
#                 normalized.append(it)
#             elif "pl" in it and "en" in it:  # stary format
#                 normalized.append({
#                     "dir": "🇵🇱 PL → EN",
#                     "in": it.get("pl", ""),
#                     "out": it.get("en", "")
#                 })
#     st.session_state["translations"] = normalized

# def _history_to_df(progress: dict, days: int = 7) -> pd.DataFrame:
#     items = progress.get("history", [])
#     if not items:
#         return pd.DataFrame(columns=["date", "result", "count"])

#     rows = []
#     for it in items:
#         try:
#             ts = it.get("timestamp", "")
#             dt = datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(timezone.utc).date()
#             rows.append({"date": pd.Timestamp(dt), "result": it.get("result", "unknown")})
#         except Exception:
#             continue

#     if not rows:
#         return pd.DataFrame(columns=["date", "result", "count"])

#     df = pd.DataFrame(rows)
#     df = df.groupby(["date", "result"], as_index=False).size().rename(columns={"size": "count"})

#     # Zakres czasu — np. ostatnie 7, 14 lub 30 dni
#     last_days = pd.date_range(
#         end=pd.Timestamp(datetime.now(timezone.utc).date()),
#         periods=days,
#         freq="D"
#     )

#     out = []
#     for d in last_days:
#         for r in ["known", "unknown"]:
#             c = int(df.loc[(df["date"] == d) & (df["result"] == r), "count"].sum()) if not df.empty else 0
#             out.append({"date": d, "result": r, "count": c})
#     return pd.DataFrame(out)


# def _streak_days(progress: dict) -> int:
#     """Ile kolejnych dni (do dziś włącznie) był jakikolwiek wpis."""
#     dates = set()
#     for it in progress.get("history", []):
#         try:
#             d = datetime.fromisoformat(it.get("timestamp","").replace("Z", "+00:00")).date()
#             dates.add(d)
#         except Exception:
#             pass
#     if not dates:
#         return 0
#     streak = 0
#     today = datetime.now(timezone.utc).date()
#     cur = today
#     while cur in dates:
#         streak += 1
#         cur = cur - timedelta(days=1)
#     return streak

# def _daily_progress_df(progress: dict, days: int = 7) -> pd.DataFrame:
#     """Zwraca DataFrame z kolumnami: date, done (ile słówek danego dnia)."""
#     daily = progress.get("daily", {})
#     last_days = pd.date_range(
#         end=pd.Timestamp(datetime.now(timezone.utc).date()),
#         periods=days, freq="D"
#     )
#     rows = []
#     for d in last_days:
#         k = d.date().isoformat()
#         rows.append({"date": d, "done": int(daily.get(k, 0))})
#     return pd.DataFrame(rows)

from __future__ import annotations

import json
import random
import re
import io
import hashlib
import unicodedata
from typing import Literal, Callable, Any, cast
from datetime import datetime, timezone, timedelta
from pathlib import Path
from base64 import b64encode

import streamlit as st
import pandas as pd
import altair as alt
from gtts import gTTS

from src.storage import (
    increment,
    load_progress,
    reset_progress,
    load_words,
    add_word,
    delete_word,
    update_daily_progress,
)
from src.i18n import LANGS, set_locale, get_flag, t
from src.translator import translate_text, TranslationError


# ─────────────────────────────────────────────────────────────
# Utils
# ─────────────────────────────────────────────────────────────

def _normalize(text: str) -> str:
    """Normalizuje tekst do porównywania (bez akcentów, małe litery, trim)."""
    if not isinstance(text, str):
        return ""
    text = text.strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join([c for c in text if not unicodedata.combining(c)])
    return text


# ─────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────

def sidebar():
    logo_path = Path(__file__).resolve().parent.parent / "assets" / "logo_sidebar.png"

    FLAGS = {"pl": "🇵🇱", "en": "🇬🇧", "de": "🇩🇪", "es": "🇪🇸", "it": "🇮🇹"}
    base = st.session_state.get("base_code", "pl").lower()
    targ = st.session_state.get("target_code", "en").lower()
    lang_pill = f'{FLAGS.get(base, "")} {base.upper()} → {FLAGS.get(targ, "")} {targ.upper()}'

    # CSS
    st.markdown("""
    <style>
      /* usuń górne pady w sidebarze */
      [data-testid="stSidebar"] { padding-top: 0 !important; }
      [data-testid="stSidebar"] .block-container { padding-top: 0 !important; }

      /* BRANDING — logo wysoko, mały odstęp z tytułem */
      .lh-brand {
        position: sticky;
        top: 0;
        z-index: 3;
        background: transparent;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 0 6px;
        margin: -38px 0 -2px 0;
        transform: translateY(-12px);
      }
      .lh-brand img {
        width: 240px;
        height: auto;
        margin: 0;
        filter: drop-shadow(0 0 6px rgba(80,140,255,.35));
        transition: transform .25s ease, filter .25s ease;
      }
      .lh-brand img:hover {
        transform: scale(1.04);
        filter: drop-shadow(0 0 10px rgba(100,170,255,.6));
      }
      .lh-title {
        font-weight: 800;
        font-size: 1.45rem;
        line-height: 1.1;
        margin: 2px 0 0 0;
        text-align: center;
        letter-spacing: .3px;
      }
      .lh-sub {
        color: #9ca3af;
        font-size: .9rem;
        margin: 2px 0 6px 0;
        text-align: center;
      }
      .lh-pill {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        padding: 6px 12px;
        border-radius: 999px;
        background: rgba(99,102,241,.14);
        border: 1px solid rgba(99,102,241,.25);
        font-size: .86rem;
        font-weight: 600;
        color: #dbe4ff;
        backdrop-filter: blur(2px);
        margin-top: 4px;
      }
      [data-testid="stSidebar"] hr { margin: 10px 0 !important; opacity: .25; }
      [data-testid="stSidebar"] .stRadio > div { gap: 8px; }
    </style>
    """, unsafe_allow_html=True)

    # Branding
    if logo_path.exists():
        b64 = b64encode(logo_path.read_bytes()).decode()
        st.markdown(
            f"""
            <div class="lh-brand">
              <img src="data:image/png;base64,{b64}" alt="Language Helper logo"/>
              <div class="lh-title">Language Helper</div>
              <div class="lh-sub">Twoja pomoc w nauce języków</div>
              <div class="lh-pill">{lang_pill}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    # Nawigacja
    nav_items = [
        ("🏠", "Panel"),
        ("🧠", "Fiszka dnia"),
        ("🌍", "Tłumacz"),
        ("🧱", "Słownictwo"),
        ("📝", "Ćwiczenia"),
        ("⚙️", "Ustawienia"),
    ]
    labels = [f"{e} {t}" for e, t in nav_items]
    page = st.radio("Nawigacja", labels, label_visibility="collapsed", key="nav_page")

    st.divider()

    # Cel tygodnia (demo)
    weekly_goal = 100
    weekly_progress = min(
        int(st.session_state.get("known_count", 0)) + int(st.session_state.get("unknown_count", 0)),
        weekly_goal
    )
    pct = (weekly_progress / weekly_goal) if weekly_goal else 0
    st.markdown('<div class="lh-section-title">Cel tygodnia</div>', unsafe_allow_html=True)
    st.progress(pct, text=f"{weekly_progress}/{weekly_goal}")

    return page


# ─────────────────────────────────────────────────────────────
# Dashboard
# ─────────────────────────────────────────────────────────────

def page_dashboard():
    st.header("🏠 Panel")
    st.caption("Statystyki nauki • Wykres aktywności • Ostatnie odpowiedzi")
    st.divider()

    progress = load_progress()
    known = int(progress["totals"]["known"])
    unknown = int(progress["totals"]["unknown"])
    total = known + unknown
    progress_ratio = (known / total) if total else 0.0

    tab_sum, tab_chart, tab_hist = st.tabs(["📊 Podsumowanie", "📈 Wykres", "📜 Historia"])

    with tab_sum:
        c1, c2, c3 = st.columns([1, 1, 1])
        c1.metric("✅ Znane słowa", known)
        c2.metric("❌ Nieznane słowa", unknown)
        c3.metric("🔥 Streak (dni z aktywnością)", _streak_days(progress))
        st.progress(progress_ratio, text=f"Postęp: {progress_ratio*100:.0f}%")
        st.write("")

        col_btn = st.columns([1, 3])[0]
        if col_btn.button("♻️ Resetuj postęp"):
            p = reset_progress()
            st.session_state.known_count = int(p["totals"]["known"])
            st.session_state.unknown_count = int(p["totals"]["unknown"])
            st.success("Zresetowano postęp.")

        if total == 0:
            st.info("Zagraj w **Fiszka dnia**, żeby rozpocząć naukę 💡")

    with tab_chart:
        st.subheader("📈 Aktywność w czasie")
        col_range = st.columns([2, 6])[0]
        range_days = col_range.radio(
            "Zakres dni", options=[7, 14, 30], index=0, horizontal=True, key="chart_range_days"
        )
        df = _history_to_df(progress, days=range_days)
        if df.empty:
            st.caption("Brak danych – zacznij od Fiszki dnia.")
        else:
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X("date:T", title="Data"),
                y=alt.Y("count:Q", title="Liczba odpowiedzi"),
                color=alt.Color(
                    "result:N",
                    title="Typ",
                    scale=alt.Scale(scheme="tableau10"),
                    legend=alt.Legend(labelExpr="datum.value == 'known' ? 'Znam' : 'Nie znam'")
                ),
                tooltip=[
                    alt.Tooltip("date:T", title="Data"),
                    alt.Tooltip("count:Q", title="Liczba"),
                    alt.Tooltip("result:N", title="Typ"),
                ],
            ).properties(height=260)
            st.altair_chart(chart, use_container_width=True)
            st.markdown("—")

        st.subheader("🎯 Dzienne przerobione słówka")
        col_days = st.columns([2, 6])[0]
        daily_range = col_days.radio("Zakres dni", options=[7, 14, 30], index=0, horizontal=True, key="daily_range_days")
        df_daily = _daily_progress_df(progress, days=daily_range)
        goal = int(st.session_state.get("daily_goal", 20))
        if df_daily.empty:
            st.caption("Brak danych dziennych.")
        else:
            bars = alt.Chart(df_daily).mark_bar().encode(
                x=alt.X("date:T", title="Data"),
                y=alt.Y("done:Q", title="Przerobione słówka"),
                tooltip=[alt.Tooltip("date:T", title="Data"), alt.Tooltip("done:Q", title="Przerobione")],
            )
            rule_df = pd.DataFrame({"y": [goal]})
            rule = alt.Chart(rule_df).mark_rule(strokeDash=[6,4]).encode(y="y:Q")
            text = alt.Chart(rule_df).mark_text(align="left", dx=5, dy=-5).encode(y="y:Q", text=alt.value(f"Cel: {goal}"))
            st.altair_chart((bars + rule + text).properties(height=240), use_container_width=True)

    with tab_hist:
        st.subheader("Ostatnie odpowiedzi (do 20)")
        items = progress.get("history", [])
        if not items:
            st.caption("Brak odpowiedzi w historii.")
        else:
            for it in items[::-1][:20]:
                badge = "✅ znam" if it.get("result") == "known" else "❌ nie znam"
                ts = it.get("timestamp", "")
                word = it.get("word", "")
                st.markdown(f"- {ts} • **{word}** — {badge}")


# ─────────────────────────────────────────────────────────────
# Słownictwo
# ─────────────────────────────────────────────────────────────

def page_vocab():
    st.header("🧱 Słownictwo")

    lang = st.session_state.get("target_code", "en").lower()
    base = st.session_state.get("base_code", "pl").lower()
    data_path = Path("data") / "words.json"

    if not data_path.exists():
        st.error("Brak pliku data/words.json")
        return

    try:
        with open(data_path, "r", encoding="utf-8") as f:
            all_words = json.load(f)
        words = list(all_words.get(lang, []))
    except Exception as e:
        st.error(f"Nie można wczytać słówek: {e}")
        return

    st.caption(f"Aktualny język: **{lang.upper()}** (bazowy: {base.upper()})")

    # Dodawanie nowego słówka
    with st.expander("➕ Dodaj nowe słówko", expanded=False):
        new_word_key = f"new_word_{lang}"
        new_tr_key   = f"new_tr_{lang}"

        c1, c2, _ = st.columns([2, 2, 1])
        with c1:
            st.text_input("Słówko w języku docelowym", key=new_word_key,
                          placeholder="np. apple / Haus / sol / libro")
        with c2:
            st.text_input(f"Tłumaczenie ({base.upper()}) — opcjonalnie", key=new_tr_key,
                          placeholder="np. jabłko / dom / słońce / książka")

        def _add_word_cb():
            word = (st.session_state.get(new_word_key) or "").strip()
            tr   = (st.session_state.get(new_tr_key) or "").strip()

            if not word:
                st.session_state["__vocab_msg__"] = ("warn", "Podaj słówko w języku docelowym.")
                return

            exists = any((w.get("word","").strip().lower() == word.lower()) for w in words)
            if exists:
                st.session_state["__vocab_msg__"] = ("info", "Takie słówko już istnieje na liście.")
                return

            if not tr:
                try:
                    tr = translate_text(word, lang, base)
                except Exception:
                    tr = "—"

            try:
                words.append({"word": word, "translation": tr})
                all_words[lang] = words
                with open(data_path, "w", encoding="utf-8") as f:
                    json.dump(all_words, f, ensure_ascii=False, indent=2)

                st.session_state["__vocab_msg__"] = ("ok", f"Dodano: **{word}** → {tr}")
                st.session_state[new_word_key] = ""
                st.session_state[new_tr_key] = ""
            except Exception as e:
                st.session_state["__vocab_msg__"] = ("err", f"Nie udało się zapisać: {e}")

        st.button("Dodaj", type="primary", key=f"add_{lang}", on_click=_add_word_cb)

        msg = st.session_state.get("__vocab_msg__")
        if msg:
            kind, text = msg
            {"ok": st.success, "warn": st.warning, "info": st.info}.get(kind, st.error)(text)

    # Filtr
    q = st.text_input("🔎 Filtruj słówka", value="", placeholder="Wpisz fragment…",
                      key=f"filter_{lang}").strip().lower()

    if q:
        view_pairs = [(i, w) for i, w in enumerate(words)
                      if q in w.get("word","").lower() or q in w.get("translation","").lower()]
    else:
        view_pairs = list(enumerate(words))

    st.session_state.setdefault("vocab_selected_to_delete", set())

    st.markdown("#### Lista słówek")
    if not view_pairs:
        st.info("Brak słówek (lub nic nie pasuje do filtra).")
        return

    # Lista + usuwanie pojedyncze
    for orig_idx, item in view_pairs:
        cols = st.columns([0.7, 3, 3, 1.2])
        with cols[0]:
            key_cb = f"vsel_{lang}_{orig_idx}"
            checked = orig_idx in st.session_state.vocab_selected_to_delete
            new_checked = st.checkbox("", value=checked, key=key_cb)
            if new_checked:
                st.session_state.vocab_selected_to_delete.add(orig_idx)
            else:
                st.session_state.vocab_selected_to_delete.discard(orig_idx)
        with cols[1]:
            st.write(f"**{item.get('word','')}**")
        with cols[2]:
            st.write(item.get("translation", "—"))
        with cols[3]:
            if st.button("🗑️ Usuń", key=f"del_{lang}_{orig_idx}"):
                try:
                    words.pop(orig_idx)
                    all_words[lang] = words
                    with open(data_path, "w", encoding="utf-8") as f:
                        json.dump(all_words, f, ensure_ascii=False, indent=2)
                    st.session_state.vocab_selected_to_delete.discard(orig_idx)
                    st.success("Usunięto słowo.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Nie udało się usunąć: {e}")

    st.divider()

    # Usuwanie zbiorcze
    selected = sorted(st.session_state.vocab_selected_to_delete)
    if selected:
        st.warning(f"Zaznaczonych do usunięcia: **{len(selected)}**")
        c1, c2 = st.columns([1, 2])
        with c1:
            confirm = st.checkbox("Potwierdzam usunięcie", key=f"confirm_bulk_{lang}")
        with c2:
            if st.button("🗑️ Usuń zaznaczone", key=f"del_bulk_{lang}"):
                if not confirm:
                    st.info("Zaznacz najpierw potwierdzenie.")
                else:
                    try:
                        for i in sorted(selected, reverse=True):
                            if 0 <= i < len(words):
                                words.pop(i)
                        all_words[lang] = words
                        with open(data_path, "w", encoding="utf-8") as f:
                            json.dump(all_words, f, ensure_ascii=False, indent=2)
                        st.session_state.vocab_selected_to_delete.clear()
                        st.success("Usunięto zaznaczone słowa.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Nie udało się usunąć zaznaczonych: {e}")
    else:
        st.caption("Zaznacz wiersze po lewej, aby usunąć wiele naraz.")


# ─────────────────────────────────────────────────────────────
# Ćwiczenia
# ─────────────────────────────────────────────────────────────

def _load_words_for_lang(lang_code: str):
    """Zwraca listę słówek (dict: {word, translation}) dla danego języka docelowego."""
    path = Path("data") / "words.json"
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return []
    if isinstance(data, dict):
        return list(data.get(lang_code, []))
    elif isinstance(data, list):
        return data
    return []


def _register_answer(ok: bool, user_answer: str):
    """Zapisz wynik odpowiedzi + czas reakcji + serię i historię."""
    import time
    ms = 0
    if st.session_state.get("ex_started_at") is not None:
        ms = int((time.time() - st.session_state["ex_started_at"]) * 1000)

    st.session_state["ex_total"] += 1
    if ok:
        st.session_state["ex_correct"] += 1
        st.session_state["ex_streak"] += 1
    else:
        st.session_state["ex_streak"] = 0

    st.session_state["ex_history"].append({
        "q": st.session_state.get("ex_question"),
        "a": st.session_state.get("ex_answer"),
        "u": user_answer,
        "ok": ok,
        "ms": ms,
    })


def _new_exercise_question(words, direction: str, mode: str):
    """
    words: LISTA {"word": "...", "translation": "..."}
    direction: "to_base" (pytanie = word, odp = translation) lub "to_target"
    mode: "choice" (ABCD) lub "write"
    """
    import time

    item = random.choice(words)
    src = item.get("word", "")
    dst = item.get("translation", "")

    if direction == "to_target":
        question, answer = dst, src
    else:  # "to_base"
        question, answer = src, dst

    st.session_state["ex_question"] = question
    st.session_state["ex_answer"] = answer

    if mode == "choice":
        pool = []
        for w in words:
            s, d = w.get("word", ""), w.get("translation", "")
            pool.append(d if direction == "to_base" else s)

        pool = [p for p in pool if p and p != answer]
        if len(pool) < 3 and pool:
            while len(pool) < 3:
                pool.append(random.choice(pool))

        options = [answer]
        if pool:
            options += random.sample(pool, k=min(3, len(pool)))
        while len(options) < 4:
            options.append("—")
        random.shuffle(options)
        st.session_state["ex_choices"] = options
    else:
        st.session_state["ex_choices"] = None

    st.session_state["ex_started_at"] = time.time()
    st.session_state["ex_qid"] = st.session_state.get("ex_qid", 0) + 1


def page_exercises():
    st.header("📝 Ćwiczenia")

    # stan
    st.session_state.setdefault("ex_question", None)
    st.session_state.setdefault("ex_answer", None)
    st.session_state.setdefault("ex_choices", None)
    st.session_state.setdefault("ex_total", 0)
    st.session_state.setdefault("ex_correct", 0)
    st.session_state.setdefault("ex_streak", 0)
    st.session_state.setdefault("ex_history", [])
    st.session_state.setdefault("ex_started_at", None)
    st.session_state.setdefault("ex_qid", 0)
    st.session_state.setdefault("ex_prev_lang", None)
    st.session_state.setdefault("ex_prev_mode", None)
    st.session_state.setdefault("ex_prev_dir", None)

    lang = st.session_state.get("target_code", "en")
    base = st.session_state.get("base_code", "pl")
    words = _load_words_for_lang(lang)
    if not words:
        st.info("Brak słówek dla bieżącego języka. Dodaj je w zakładce **Słownictwo**.")
        return

    c1, c2, c3 = st.columns([1.2, 1.2, 1])
    with c1:
        mode_label = st.radio("Tryb", ["Wybór (ABCD)", "Pisanie"], horizontal=True, key="ex_mode_label")
        mode = "choice" if mode_label == "Wybór (ABCD)" else "write"
    with c2:
        dir_label = st.radio("Kierunek", ["Docelowy → Bazowy", "Bazowy → Docelowy"], horizontal=True, key="ex_dir_label")
        direction = "to_base" if dir_label == "Docelowy → Bazowy" else "to_target"
    with c3:
        st.caption(f"Słówka: **{len(words)}**")

    if mode == "choice" and len(words) < 4:
        st.warning("Za mało słówek dla trybu wyboru (min. 4). Przełączam na **Pisanie**.")
        mode = "write"

    changed = (
        st.session_state["ex_prev_lang"] != lang or
        st.session_state["ex_prev_mode"] != mode or
        st.session_state["ex_prev_dir"]  != direction
    )
    st.session_state["ex_prev_lang"] = lang
    st.session_state["ex_prev_mode"] = mode
    st.session_state["ex_prev_dir"]  = direction
    if changed:
        st.session_state["ex_question"] = None
        st.session_state["ex_answer"] = None
        st.session_state["ex_choices"] = None
        _new_exercise_question(words, direction, mode)

    if st.button("♻️ Resetuj statystyki"):
        st.session_state["ex_total"] = 0
        st.session_state["ex_correct"] = 0
        st.session_state["ex_streak"] = 0
        st.session_state["ex_history"] = []
        st.session_state["ex_started_at"] = None
        st.success("Wyzerowano statystyki ćwiczeń.")

    colA, colB, colC, colD = st.columns(4)
    acc = (st.session_state["ex_correct"] / st.session_state["ex_total"] * 100) if st.session_state["ex_total"] else 0
    colA.metric("Poprawne", st.session_state["ex_correct"])
    colB.metric("Wszystkie", st.session_state["ex_total"])
    colC.metric("Skuteczność", f"{acc:.0f}%")
    if st.session_state["ex_history"]:
        avg_ms = sum(h.get("ms", 0) for h in st.session_state["ex_history"]) / max(1, len(st.session_state["ex_history"]))
    else:
        avg_ms = 0
    colD.metric("Śr. czas", f"{int(avg_ms)} ms")
    st.caption(f"🔥 Seria: **{st.session_state['ex_streak']}**")
    st.divider()

    if st.session_state["ex_question"] is None:
        _new_exercise_question(words, direction, mode)

    st.subheader("Pytanie")
    st.write(st.session_state["ex_question"])
    result_placeholder = st.empty()
    next_col1, next_col2 = st.columns([1, 1])

    def _next():
        result_placeholder.empty()
        _new_exercise_question(words, direction, mode)

    if mode == "choice":
        options = st.session_state.get("ex_choices") or []
        choice_key = f"ex_choice_val_{st.session_state['ex_qid']}"
        user_choice = st.radio("Wybierz odpowiedź:", options, index=0 if options else None, key=choice_key) or ""
        with next_col1:
            if st.button("Sprawdź", type="primary", key=f"ex_check_choice_{st.session_state['ex_qid']}"):
                correct = st.session_state.get("ex_answer", "")
                if _normalize(user_choice) == _normalize(correct):
                    result_placeholder.success("✅ Dobrze!")
                    _register_answer(True, user_choice)
                else:
                    result_placeholder.error(f"❌ Źle. Poprawna odpowiedź: **{correct}**")
                    _register_answer(False, user_choice)
        with next_col2:
            st.button("Następne pytanie", key=f"ex_next_choice_{st.session_state['ex_qid']}", on_click=_next)
    else:
        input_key = f"ex_user_input_{st.session_state['ex_qid']}"
        st.text_input("Twoja odpowiedź:", key=input_key, placeholder="Wpisz tłumaczenie…")
        with next_col1:
            if st.button("Sprawdź", type="primary", key=f"ex_check_write_{st.session_state['ex_qid']}"):
                user = _normalize(st.session_state.get(input_key) or "")
                answ = _normalize(st.session_state.get("ex_answer") or "")
                ok = bool(user) and (user == answ)
                if ok:
                    result_placeholder.success("✅ Dobrze!")
                else:
                    result_placeholder.error(f"❌ Źle. Poprawna odpowiedź: **{st.session_state['ex_answer']}**")
                _register_answer(ok, user)
        with next_col2:
            st.button("Następne pytanie", key=f"ex_next_write_{st.session_state['ex_qid']}", on_click=_next)

    hist = st.session_state.get("ex_history", [])
    if hist:
        st.markdown("### Ostatnie odpowiedzi")
        for h in hist[-5:][::-1]:
            tag = "✅" if h["ok"] else "❌"
            st.caption(f"{tag} {h['q']} → **{h['a']}**  •  Ty: _{h['u'] or '—'}_  •  {h['ms']} ms")


# ─────────────────────────────────────────────────────────────
# Ustawienia
# ─────────────────────────────────────────────────────────────

def page_settings():
    st.header("⚙️ Ustawienia")
    st.subheader("🌍 Wybór języków")

    target_options = [("en","Angielski"), ("de","Niemiecki"), ("es","Hiszpański"), ("it","Włoski")]
    base_options   = [("pl","Polski"), ("en","Angielski"), ("de","Niemiecki"), ("es","Hiszpański"), ("it","Włoski")]

    st.session_state.setdefault("base_code", "pl")
    st.session_state.setdefault("target_code", "en")

    def _fmt(opt): code, name = opt; return f"{get_flag(code)}  {name}"

    base_idx   = [i for i,(c,_) in enumerate(base_options)   if c==st.session_state.base_code][0]
    target_idx = [i for i,(c,_) in enumerate(target_options) if c==st.session_state.target_code][0]

    base_sel = st.selectbox("Język bazowy (interfejs):", base_options, index=base_idx, format_func=_fmt)
    targ_sel = st.selectbox("Język, którego się uczysz:", target_options, index=target_idx, format_func=_fmt)

    st.session_state.base_code   = base_sel[0]
    st.session_state.target_code = targ_sel[0]

    set_locale(st.session_state.base_code)

    st.markdown("---")
    st.subheader("🎯 Cel nauki")
    st.number_input("Dzienny cel (minuty):", 5, 180, value=20, step=5, key="daily_goal")

    st.success(
        f"Interfejs: {get_flag(st.session_state.base_code)} "
        f"{LANGS[st.session_state.base_code]['name']} • "
        f"Nauka: {get_flag(st.session_state.target_code)} "
        f"{LANGS[st.session_state.target_code]['name']}"
    )


# ─────────────────────────────────────────────────────────────
# TTS cache używany w Fiszce
# ─────────────────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def _tts_bytes(text: str, lang: str) -> bytes:
    """Zwraca MP3 (bytes) z wymową `text` w języku `lang` (gTTS: en/de/es/it/pl)."""
    buf = io.BytesIO()
    gTTS(text=text, lang=lang).write_to_fp(buf)
    buf.seek(0)
    return buf.read()


# ─────────────────────────────────────────────────────────────
# Fiszka
# ─────────────────────────────────────────────────────────────

def page_flashcard():
    st.header("🧠 Fiszka dnia")

    target = st.session_state.get("target_code", "en")
    data_path = Path("data") / "words.json"
    if not data_path.exists():
        st.error("Brak pliku data/words.json")
        return

    try:
        with open(data_path, "r", encoding="utf-8") as f:
            all_words = json.load(f)
        words = all_words.get(target, []) if isinstance(all_words, dict) else all_words
    except Exception as e:
        st.error(f"Nie można wczytać słówek: {e}")
        return

    if not words:
        st.info("Brak słówek dla tego języka. Dodaj w zakładce **Słownictwo**.")
        return

    st.session_state.setdefault("fc_order", random.sample(range(len(words)), k=len(words)))
    st.session_state.setdefault("fc_idx", 0)
    st.session_state.setdefault("fc_show_translation", False)
    st.session_state.setdefault("known_count", 0)
    st.session_state.setdefault("unknown_count", 0)
    st.session_state.setdefault("ex_qid", 0)

    if st.session_state.fc_idx >= len(st.session_state.fc_order):
        st.session_state.fc_idx = 0
        random.shuffle(st.session_state.fc_order)

    card = words[st.session_state.fc_order[st.session_state.fc_idx]]
    w = card.get("word", "")
    t = card.get("translation", "—")

    gtts_map = {"en": "en", "de": "de", "es": "es", "it": "it", "pl": "pl"}
    dst_gtts = gtts_map.get(target)

    c_word, c_audio = st.columns([5, 1])
    with c_word:
        st.subheader(w)
    with c_audio:
        if dst_gtts:
            if st.button("🔊", help="Odsłuch wymowy", key=f"fc_tts_{st.session_state.fc_idx}"):
                try:
                    audio_bytes = _tts_bytes(w, dst_gtts)
                    st.audio(audio_bytes, format="audio/mp3")
                except Exception as e:
                    st.info(f"Nie udało się wygenerować wymowy: {e}")

    if not st.session_state.fc_show_translation:
        if st.button("👀 Pokaż tłumaczenie"):
            st.session_state.fc_show_translation = True
            st.rerun()
    else:
        st.success(t)

        c1, c2, c3 = st.columns([1, 1, 1])

        def _mark(result: Literal["known", "unknown"]) -> None:
            if result == "known":
                st.session_state.known_count += 1
            else:
                st.session_state.unknown_count += 1

            if callable(increment):
                inc = cast(Callable[..., Any], increment)
                try:
                    inc(result=result, word=w)
                except TypeError:
                    inc(result, w)
                except Exception:
                    pass

            st.session_state.fc_idx += 1
            st.session_state.fc_show_translation = False
            st.rerun()

        with c1:
            if st.button("✅ Znam"):
                _mark("known")
        with c2:
            if st.button("❌ Nie znam"):
                _mark("unknown")
        with c3:
            if st.button("🔁 Następne"):
                st.session_state.fc_idx += 1
                st.session_state.fc_show_translation = False
                st.rerun()

    st.divider()

    total_seen = st.session_state.known_count + st.session_state.unknown_count
    if total_seen > 0:
        ratio = st.session_state.known_count / total_seen
        st.progress(ratio, text=f"Postęp tej sesji: {ratio*100:.0f}% (✅ {st.session_state.known_count} • ❌ {st.session_state.unknown_count})")
    else:
        st.info("Kliknij **Pokaż tłumaczenie**, aby rozpocząć sesję.")


# ─────────────────────────────────────────────────────────────
# Translator
# ─────────────────────────────────────────────────────────────

def page_translator():
    st.header("🌍 Tłumacz")

    st.session_state.setdefault("translations", [])
    st.session_state.setdefault("tr_src", "")

    base = st.session_state.get("base_code", "pl")
    targ = st.session_state.get("target_code", "en")
    FLAGS = {"pl": "🇵🇱", "en": "🇬🇧", "de": "🇩🇪", "es": "🇪🇸", "it": "🇮🇹"}

    label0 = f"{FLAGS[base]} {base.upper()} → {FLAGS[targ]} {targ.upper()}"
    label1 = f"{FLAGS[targ]} {targ.upper()} → {FLAGS[base]} {base.upper()}"
    dir_idx = st.radio("Kierunek", options=[0, 1], index=0,
                       format_func=lambda i: label0 if i == 0 else label1)

    if dir_idx == 0:
        src_lang, dst_lang = base, targ
    else:
        src_lang, dst_lang = targ, base

    ph = "Wpisz zdanie..." if src_lang == "pl" else "Type a sentence..."
    st.text_area("Tekst źródłowy", key="tr_src", height=120, placeholder=ph)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Przetłumacz", type="primary"):
            txt = st.session_state["tr_src"].strip()
            if not txt:
                st.warning("Podaj tekst do tłumaczenia.")
            else:
                try:
                    result = translate_text(txt, src_lang, dst_lang)
                    st.success(result)
                    st.session_state["translations"].append({
                        "src": txt,
                        "dst": result,
                        "dir": f"{src_lang.upper()}→{dst_lang.upper()}",
                        "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    })
                    gtts_map = {"en": "en", "pl": "pl", "de": "de", "es": "es", "it": "it"}
                    dst_gtts = gtts_map.get(dst_lang)
                    if dst_gtts:
                        audio_bytes = _tts_bytes(result, dst_gtts)
                        st.audio(audio_bytes, format="audio/mp3")
                except TranslationError as e:
                    st.error(str(e))
                except Exception as e:
                    st.error(f"Nieoczekiwany błąd tłumaczenia: {e}")

    def _clear_src():
        st.session_state["tr_src"] = ""

    with col2:
        st.button("Wyczyść", on_click=_clear_src)

    history = st.session_state.get("translations", [])
    st.markdown("### Historia tłumaczeń (ostatnie 5)")
    if not history:
        st.caption("Brak pozycji w historii.")
    else:
        for item in history[-5:][::-1]:
            head = item["src"][:60] + ("…" if len(item["src"]) > 60 else "")
            st.caption(f'{item.get("ts","")} • {item.get("dir","")}')
            with st.expander(head):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write("**Źródło**")
                    st.write(item["src"])
                with col_b:
                    st.write("**Wynik**")
                    st.success(item["dst"])


# ─────────────────────────────────────────────────────────────
# Dashboard helpers
# ─────────────────────────────────────────────────────────────

def _history_to_df(progress: dict, days: int = 7) -> pd.DataFrame:
    items = progress.get("history", [])
    if not items:
        return pd.DataFrame(columns=["date", "result", "count"])

    rows = []
    for it in items:
        try:
            ts = it.get("timestamp", "")
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(timezone.utc).date()
            rows.append({"date": pd.Timestamp(dt), "result": it.get("result", "unknown")})
        except Exception:
            continue

    if not rows:
        return pd.DataFrame(columns=["date", "result", "count"])

    df = pd.DataFrame(rows)
    df = df.groupby(["date", "result"], as_index=False).size().rename(columns={"size": "count"})

    last_days = pd.date_range(
        end=pd.Timestamp(datetime.now(timezone.utc).date()),
        periods=days, freq="D"
    )

    out = []
    for d in last_days:
        for r in ["known", "unknown"]:
            c = int(df.loc[(df["date"] == d) & (df["result"] == r), "count"].sum()) if not df.empty else 0
            out.append({"date": d, "result": r, "count": c})
    return pd.DataFrame(out)


def _streak_days(progress: dict) -> int:
    """Ile kolejnych dni (do dziś włącznie) był jakikolwiek wpis."""
    dates = set()
    for it in progress.get("history", []):
        try:
            d = datetime.fromisoformat(it.get("timestamp","").replace("Z", "+00:00")).date()
            dates.add(d)
        except Exception:
            pass
    if not dates:
        return 0
    streak = 0
    today = datetime.now(timezone.utc).date()
    cur = today
    while cur in dates:
        streak += 1
        cur = cur - timedelta(days=1)
    return streak


def _daily_progress_df(progress: dict, days: int = 7) -> pd.DataFrame:
    """Zwraca DataFrame z kolumnami: date, done (ile słówek danego dnia)."""
    daily = progress.get("daily", {})
    last_days = pd.date_range(
        end=pd.Timestamp(datetime.now(timezone.utc).date()),
        periods=days, freq="D"
    )
    rows = []
    for d in last_days:
        k = d.date().isoformat()
        rows.append({"date": d, "done": int(daily.get(k, 0))})
    return pd.DataFrame(rows)
