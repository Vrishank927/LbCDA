from __future__ import annotations

import random

import streamlit as st

from streamlit_app.components.cards import kpi_card
from streamlit_app.components.charts import plot_metric_line, plot_hist
from streamlit_app.components.sidebar import render_premium_sidebar


def render() -> None:
    # Hero + KPI row
    st.markdown(
        """
        <div class="premium-card scanline" style="padding:20px;">
          <div style="display:flex; align-items:flex-start; justify-content:space-between; gap:16px;">
            <div>
              <div style="font-size:12px; color: rgba(255,255,255,0.65); letter-spacing:0.12em;">NETWORK INTELLIGENCE</div>
              <div style="font-size:36px; font-weight:1000; margin-top:8px; line-height:1.05;">
                AI Ops for Telecom QoS & Call Drop
              </div>
              <div style="color: rgba(255,255,255,0.72); margin-top:10px; max-width:760px;">
                Predict risk in real-time, quantify network health, and recommend actionable optimizations.
                Built for enterprise operators, government agencies, and large-scale telecom deployments.
              </div>
              <div style="margin-top:14px; display:flex; gap:10px; flex-wrap:wrap;">
                <span style="padding:8px 12px; border-radius:999px; border:1px solid rgba(34,230,255,0.25); background: rgba(34,230,255,0.08); font-weight:800; color: rgba(34,230,255,0.92);">24/7 AI Monitoring</span>
                <span style="padding:8px 12px; border-radius:999px; border:1px solid rgba(166,102,255,0.25); background: rgba(166,102,255,0.08); font-weight:800; color: rgba(166,102,255,0.92);">Enterprise SLA Insights</span>
              </div>
            </div>
            <div style="min-width:260px;">
              <div style="border:1px solid rgba(34,230,255,0.25); background: rgba(10,18,38,0.55); border-radius:18px; padding:14px;">
                <div style="font-size:12px; color: rgba(255,255,255,0.65);">Live Status</div>
                <div style="font-weight:1000; font-size:18px; margin-top:6px;">AI Monitoring Active</div>
                <div style="margin-top:10px; height:10px; border-radius:999px; background: rgba(255,255,255,0.08); overflow:hidden;">
                  <div style="width:72%; height:100%; background: linear-gradient(90deg, rgba(34,230,255,0.75), rgba(166,102,255,0.6));"></div>
                </div>
                <div style="font-size:12px; color: rgba(255,255,255,0.6); margin-top:8px;">Last model refresh: just now</div>
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("""
      <div style="height:14px"></div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4, gap="large")
    with c1:
        kpi_card("Prediction Accuracy", "98.7%", "Validated on holdout data", "rgba(34,230,255,0.35)")
    with c2:
        kpi_card("Network Records", "2M+", "Processed through AI pipelines", "rgba(166,102,255,0.35)")
    with c3:
        kpi_card("States Analyzed", "50+", "Coverage across multi-region ops", "rgba(34,230,255,0.35)")
    with c4:
        kpi_card("AI Monitoring", "24/7", "Automated risk detection", "rgba(30,230,166,0.35)")

    # Analytics section (Plotly only)
    st.markdown("""
      <div style="height:14px"></div>
    """, unsafe_allow_html=True)

    h1, h2 = st.columns(2, gap="large")

    with h1:
        x = [f"T-{i}" for i in range(10, 0, -1)]
        y = [random.randint(55, 82) for _ in x]
        st.plotly_chart(plot_metric_line(x, y, "Network Stability Trend"), use_container_width=True)

    with h2:
        # Fake distribution for visual polish
        data = [random.gauss(0.65, 0.12) for _ in range(600)]
        st.plotly_chart(plot_hist(data, "QoS Distribution (Simulated)", "Quality Score"), use_container_width=True)

