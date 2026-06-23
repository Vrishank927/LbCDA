from __future__ import annotations

import streamlit as st


def toast_success(msg: str) -> None:
    # Streamlit built-in toast API varies by version; safe fallback.
    try:
        st.toast(msg, icon="✅")
    except Exception:
        st.success(msg)


def toast_warning(msg: str) -> None:
    try:
        st.toast(msg, icon="⚠️")
    except Exception:
        st.warning(msg)


def toast_error(msg: str) -> None:
    try:
        st.toast(msg, icon="⛔")
    except Exception:
        st.error(msg)

