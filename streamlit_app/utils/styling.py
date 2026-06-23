from __future__ import annotations

import streamlit as st


PREMIUM_CSS = r"""
<style>
  :root{
    --bg0:#070A12;
    --bg1:#0A0F22;
    --card: rgba(14, 23, 48, 0.62);
    --card2: rgba(10, 18, 38, 0.72);
    --stroke: rgba(74, 208, 255, 0.28);
    --stroke2: rgba(166, 102, 255, 0.24);
    --text: rgba(255,255,255,0.92);
    --muted: rgba(255,255,255,0.65);
    --muted2: rgba(255,255,255,0.45);
    --blue:#2D7FF9;
    --cyan:#22E6FF;
    --purple:#A666FF;
    --good:#1EE6A6;
    --warn:#FFC857;
    --bad:#FF4D6D;
    --crit:#FF2D7A;
    --shadow: 0 18px 60px rgba(0,0,0,0.45);
  }

  html, body, [class*="stApp"]{background: linear-gradient(180deg, var(--bg0), var(--bg1)) !important; color: var(--text);} 

  /* Sidebar */
  [data-testid="stSidebar"]{
    background: rgba(8, 13, 28, 0.72) !important;
    backdrop-filter: blur(12px);
    border-right: 1px solid rgba(34,230,255,0.18);
  }
  [data-testid="stSidebarNav"] a{
    padding: 10px 12px !important;
  }

  /* Buttons */
  .stButton > button{
    background: linear-gradient(135deg, rgba(34,230,255,0.18), rgba(166,102,255,0.12)) !important;
    border: 1px solid rgba(34,230,255,0.28) !important;
    color: rgba(255,255,255,0.92) !important;
    border-radius: 14px !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.25);
    transition: transform 160ms ease, border-color 160ms ease, background 160ms ease;
  }
  .stButton > button:hover{
    transform: translateY(-1px);
    border-color: rgba(34,230,255,0.55) !important;
  }

  /* Containers/cards */
  .premium-card{
    background: var(--card) !important;
    border: 1px solid rgba(34,230,255,0.18) !important;
    border-radius: 18px !important;
    box-shadow: var(--shadow);
    backdrop-filter: blur(14px);
  }

  /* Inputs */
  input[type="text"], input[type="number"], select, textarea{
    background: rgba(10, 18, 38, 0.65) !important;
    color: var(--text) !important;
    border: 1px solid rgba(34,230,255,0.18) !important;
    border-radius: 12px !important;
  }
  div[data-baseweb="select"] > div{background: rgba(10, 18, 38, 0.65) !important;}

  /* Headers */
  h1, h2, h3{letter-spacing: -0.02em;}

  /* Metric cards */
  .kpi{
    padding: 18px 16px;
  }
  .kpi .label{font-size:12px; color: var(--muted); margin-bottom:6px;}
  .kpi .value{font-size:26px; font-weight:900;}
  .kpi .sub{font-size:12px; color: var(--muted2); margin-top:6px;}

  /* Tabs */
  div[role="tablist"] button{ border-radius: 12px !important; }

  /* Animated scan line */
  .scanline{
    position: relative;
    overflow: hidden;
  }
  .scanline:after{
    content:"";
    position:absolute;
    left:-20%; top:-40%;
    width:140%; height:35px;
    background: linear-gradient(90deg, transparent, rgba(34,230,255,0.35), transparent);
    transform: rotate(12deg);
    animation: scan 2.6s ease-in-out infinite;
    pointer-events:none;
  }
  @keyframes scan{
    0%{transform: translateY(-80px) rotate(12deg); opacity:0}
    30%{opacity:1}
    70%{opacity:1}
    100%{transform: translateY(200px) rotate(12deg); opacity:0}
  }
</style>
"""


def inject_premium_css() -> None:
    """Aggressively override Streamlit styling for a premium SaaS look."""
    st.markdown(PREMIUM_CSS, unsafe_allow_html=True)

