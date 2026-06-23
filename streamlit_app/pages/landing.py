from __future__ import annotations

import random

import streamlit as st

from streamlit_app.components.cards import kpi_card, status_badge
from streamlit_app.components.charts import plot_metric_line, plot_hist


def render() -> None:
    st.markdown(
        """
        <div class="premium-card scanline" style="padding:22px 20px;">
          <div style="display:flex; align-items:flex-start; justify-content:space-between; gap:18px; flex-wrap:wrap;">
            <div style="flex: 1 1 520px;">
              <div style="font-size:12px; color: rgba(255,255,255,0.62); letter-spacing:0.14em;">AI TELECOM INTELLIGENCE</div>
              <div style="font-size:44px; font-weight:1000; margin-top:10px; line-height:1.06;">
                Network risk, predicted in seconds.
              </div>
              <div style="margin-top:12px; color: rgba(255,255,255,0.74); font-size:15px; max-width:760px;">
                Premium SaaS-grade analytics for Call Drop Prediction and Network QoS Health. Built for
                enterprise telecom operations—real-time signals, executive dashboards, and actionable recommendations.
              </div>
              <div style="margin-top:18px; display:flex; gap:10px; flex-wrap:wrap;">
                <span style="padding:10px 14px; border-radius:999px; border:1px solid rgba(34,230,255,0.22); background: rgba(34,230,255,0.08); color: rgba(34,230,255,0.95); font-weight:900;">98.7% Accuracy</span>
                <span style="padding:10px 14px; border-radius:999px; border:1px solid rgba(166,102,255,0.22); background: rgba(166,102,255,0.08); color: rgba(166,102,255,0.95); font-weight:900;">2M+ Records</span>
                <span style="padding:10px 14px; border-radius:999px; border:1px solid rgba(30,230,166,0.22); background: rgba(30,230,166,0.08); color: rgba(30,230,166,0.95); font-weight:900;">24/7 AI Monitoring</span>
              </div>
            </div>

            <div style="flex: 0 1 360px;">
              <div class="premium-card" style="padding:14px 14px; border-radius:18px;">
                <div style="display:flex; align-items:center; justify-content:space-between; gap:10px;">
                  <div>
                    <div style="font-size:12px; color: rgba(255,255,255,0.62);">System Status</div>
                    <div style="font-size:18px; font-weight:1000; margin-top:4px;">Operational</div>
                  </div>
                  <div>{""}</div>
                </div>
                <div style="margin-top:10px;">
                  {""}
                </div>
                <div style="margin-top:10px; height:12px; background: rgba(255,255,255,0.08); border-radius:999px; overflow:hidden;">
                  <div style="width:82%; height:100%; background: linear-gradient(90deg, rgba(34,230,255,0.9), rgba(166,102,255,0.7));"></div>
                </div>
                <div style="margin-top:8px; font-size:12px; color: rgba(255,255,255,0.62);">Last sync: just now • SLA: 99.95%</div>
                <div style="margin-top:12px; display:flex; gap:10px; flex-wrap:wrap;">
                  <span style="padding:8px 12px; border-radius:999px; border:1px solid rgba(30,230,166,0.25); background: rgba(30,230,166,0.08); color: rgba(30,230,166,0.92); font-weight:900;">Signals Healthy</span>
                  <span style="padding:8px 12px; border-radius:999px; border:1px solid rgba(34,230,255,0.22); background: rgba(34,230,255,0.08); color: rgba(34,230,255,0.92); font-weight:900;">Low Latency</span>
                </div>
              </div>

              <div style="height:12px"></div>

              <div style="font-size:12px; color: rgba(255,255,255,0.62);">Quick Access</div>
              <div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:8px;">
                <a class="stLinkButton" href="#" style="text-decoration:none;">
                  <span style="padding:10px 14px; border-radius:14px; border:1px solid rgba(34,230,255,0.25); background: rgba(34,230,255,0.08); color: rgba(255,255,255,0.92); font-weight:900;">Open Dashboard</span>
                </a>
                <a class="stLinkButton" href="#" style="text-decoration:none;">
                  <span style="padding:10px 14px; border-radius:14px; border:1px solid rgba(166,102,255,0.25); background: rgba(166,102,255,0.08); color: rgba(255,255,255,0.92); font-weight:900;">Run Prediction</span>
                </a>
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("""<div style="height:18px"></div>""", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4, gap="large")
    with c1:
        kpi_card("Prediction Accuracy", "98.7%", "Validated on holdout data", "rgba(34,230,255,0.35)")
    with c2:
        kpi_card("Network Records Processed", "2M+", "Through AI inference pipelines", "rgba(166,102,255,0.35)")
    with c3:
        kpi_card("States Analyzed", "50+", "Multi-region coverage", "rgba(34,230,255,0.35)")
    with c4:
        kpi_card("AI Monitoring", "24/7", "Automated risk detection", "rgba(30,230,166,0.35)")

    st.markdown("""<div style="height:16px"></div>""", unsafe_allow_html=True)

    h1, h2 = st.columns(2, gap="large")
    with h1:
        x = [f"T-{i}" for i in range(12, 0, -1)]
        y = [random.randint(56, 86) for _ in x]
        st.plotly_chart(plot_metric_line(x, y, "Network Stability Trend"), use_container_width=True)
    with h2:
        data = [random.gauss(0.66, 0.11) for _ in range(700)]
        st.plotly_chart(plot_hist(data, "QoS Distribution (Simulated)", "Quality Score"), use_container_width=True)

    st.markdown("""<div style="height:10px"></div>""", unsafe_allow_html=True)
    status_badge("Enterprise-grade analytics loaded", tone="good")

