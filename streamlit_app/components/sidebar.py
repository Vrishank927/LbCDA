from __future__ import annotations

import streamlit as st


def render_premium_sidebar(active_page: str) -> None:
    """Render a premium sidebar shell using CSS + Streamlit sidebar elements."""

    with st.sidebar:
        st.markdown(
            """
            <div class="scanline" style="padding: 14px 8px 6px 10px;">
              <div style="font-weight:900; font-size:18px; letter-spacing:-0.02em; color: rgba(255,255,255,0.95);">
                LbCDA
              </div>
              <div style="font-size:12px; color: rgba(255,255,255,0.65); margin-top:2px;">
                AI Telecom Network Intelligence
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        pages = ["Dashboard", "Call Drop", "QoS"]
        idx = pages.index(active_page) if active_page in pages else 0

        # System status indicator
        st.markdown(
            """
            <div style="display:flex; align-items:center; gap:10px;">
              <span style="width:10px; height:10px; border-radius:50%; background:#1EE6A6; box-shadow:0 0 18px rgba(30,230,166,0.5);"></span>
              <div style="font-size:12px; color: rgba(255,255,255,0.7);">System Online • 24/7 Monitoring</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div style="margin-top:12px;">
              <div style="font-size:12px; color: rgba(255,255,255,0.6);">Signed in</div>
              <div style="font-weight:800; color: rgba(255,255,255,0.92);">Enterprise Operator</div>
              <div style="font-size:12px; color: rgba(255,255,255,0.55);">SLA: 99.95%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        # Navigation
        selection = st.radio(
            label="Navigation",
            options=pages,
            index=idx,
            format_func=lambda x: f"{x}",
            label_visibility="collapsed",
        )


    return selection

