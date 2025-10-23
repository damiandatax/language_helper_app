from __future__ import annotations
import streamlit as st
from streamlit.components.v1 import html  # <— pancerne wstrzykiwanie CSS/HEAD
from src.ui import (
    sidebar,
    page_dashboard,
    page_vocab,
    page_exercises,
    page_settings,
    page_flashcard,
    page_translator,
)
from src.storage import load_progress

# ─────────────────────────────────────────────────────────────
# Konfiguracja strony – BEZ faviconu / korony Streamlit
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Language Helper 🌍",
    page_icon="",   # pusty = brak korony i jakiejkolwiek favicony
    layout="wide",
)


# ─────────────────────────────────────────────────────────────
# Inicjalizacja domyślnego session_state
# ─────────────────────────────────────────────────────────────
def ensure_state():
    defaults = {
        "base_code": "pl",
        "target_code": "en",
        "locale": "pl",
        "translations": [],
        "known_count": 0,
        "unknown_count": 0,
    }
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)

ensure_state()

# ─────────────────────────────────────────────────────────────
# Globalny CSS – wstrzykiwany przez components.html (nie wydrukuje się)
# ─────────────────────────────────────────────────────────────
GLOBAL_CSS = """
<meta name="google" content="notranslate" />
<style>
  /* zaokrąglenia */
  .stMarkdown, .stMetric, .stButton>button, .stTextInput>div>div>input,
  .stTextArea textarea, .stSelectbox, .stRadio, .stDataFrame, .stFileUploader {
    border-radius: 12px !important;
  }

  .stButton>button {
    padding: 0.5rem 1rem; font-weight: 600;
  }

  /* węższy sidebar */
  [data-testid="stSidebar"] { width: 300px; }

  /* stopka */
  .app-footer {
    text-align: center;
    color: #9ca3af;
    margin-top: 32px;
    font-size: 0.95rem;
    letter-spacing: 0.3px;
    font-weight: 500;
    opacity: 0.9;
  }
</style>
"""

# render do DOM bez wyświetlania (wysokość 0)
html(GLOBAL_CSS, height=0)

# ─────────────────────────────────────────────────────────────
# Wczytaj postęp (pierwsze uruchomienie)
# ─────────────────────────────────────────────────────────────
if "known_count" not in st.session_state or "unknown_count" not in st.session_state:
    _p = load_progress()
    st.session_state["known_count"] = int(_p["totals"]["known"])
    st.session_state["unknown_count"] = int(_p["totals"]["unknown"])

# ─────────────────────────────────────────────────────────────
# Sidebar + routing
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    page = sidebar()

if page == "🏠 Panel":
    page_dashboard()
elif page == "🧠 Fiszka dnia":
    page_flashcard()
elif page == "🌍 Tłumacz":
    page_translator()
elif page == "🧱 Słownictwo":
    page_vocab()
elif page == "📝 Ćwiczenia":
    page_exercises()
else:
    page_settings()

# ─────────────────────────────────────────────────────────────
# Stopka
# ─────────────────────────────────────────────────────────────
st.markdown(
    '<div class="app-footer">© 2025 Language Helper • Damian • v1.0</div>',
    unsafe_allow_html=True,
)
