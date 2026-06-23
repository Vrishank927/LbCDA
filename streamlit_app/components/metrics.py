from __future__ import annotations

import streamlit as st


def progress_bar(label: str, pct: float, tone: str = "cyan") -> None:
    color = {
        "cyan": "rgba(34,230,255,0.85)",
        "purple": "rgba(166,102,255,0.85)",
        "good": "rgba(30,230,166,0.9)",
        "warn": "rgba(255,200,87,0.92)",
        "bad": "rgba(255,77,109,0.92)",
        "crit": "rgba(255,45,122,0.95)",
    }.get(tone, "rgba(34,230,255,0.85)")

    st.markdown(
        f"""
        <div style="margin-top:12px;">
          <div style="display:flex; align-items:center; justify-content:space-between; gap:12px;">
            <div style="font-size:12px; color: rgba(255,255,255,0.65); font-weight:800; letter-spacing:0.02em;">{label}</div>
            <div style="font-size:12px; color: rgba(255,255,255,0.78); font-weight:900;">{pct:.1f}%</div>
          </div>
          <div style="margin-top:8px; height:12px; border-radius:999px; background: rgba(255,255,255,0.06); overflow:hidden; border:1px solid rgba(34,230,255,0.10);">
            <div style="width:{pct:.1f}%; height:100%; background: linear-gradient(90deg, {color}, rgba(166,102,255,0.55));"></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

