from __future__ import annotations

import os
import sys

# Ensure the repo root (parent of this package) is on PYTHONPATH.
# This prevents `ModuleNotFoundError: No module named 'streamlit_app'`
# when Streamlit is launched from a different working directory.
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st


from streamlit_app.components.sidebar import render_premium_sidebar
from streamlit_app.utils.styling import inject_premium_css

from streamlit_app.pages import call_drop as call_drop_page
from streamlit_app.pages import dashboard as dashboard_page
from streamlit_app.pages import landing as landing_page
from streamlit_app.pages import qos as qos_page


st.set_page_config(page_title="LbCDA | Telecom Network Intelligence", layout="wide")

inject_premium_css()

# Premium SaaS routing via sidebar
active = render_premium_sidebar(active_page="Dashboard")

if active == "Dashboard":
    dashboard_page.render()
elif active == "Call Drop":
    call_drop_page.render()
elif active == "QoS":
    qos_page.render()
else:
    landing_page.render()

