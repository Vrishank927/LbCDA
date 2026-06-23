from __future__ import annotations

import streamlit as st


def kpi_card(label: str, value: str, sub: str, accent: str = "rgba(34,230,255,0.35)") -> None:
    st.markdown(
        f"""
        <div class="premium-card kpi" style="border-color:{accent};">
          <div class="label">{label}</div>
          <div class="value">{value}</div>
          <div class="sub">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def status_badge(text: str, tone: str = "good") -> None:
    tone_map = {
        "good": ("rgba(30,230,166,0.25)", "rgba(30,230,166,0.85)"),
        "warn": ("rgba(255,200,87,0.22)", "rgba(255,200,87,0.9)"),
        "bad": ("rgba(255,77,109,0.22)", "rgba(255,77,109,0.92)"),
        "crit": ("rgba(255,45,122,0.22)", "rgba(255,45,122,0.95)"),
    }
    bg, fg = tone_map.get(tone, tone_map["good"])
    st.markdown(
        f"""
        <div style="display:inline-flex; align-items:center; gap:10px; padding:10px 14px; border-radius:999px; border:1px solid {fg}; background:{bg};">
          <span style="width:10px; height:10px; border-radius:50%; background:{fg}; box-shadow:0 0 16px {fg};"></span>
          <span style="font-weight:900; color:{fg};">{text}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

