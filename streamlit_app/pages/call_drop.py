from __future__ import annotations

import time

import joblib
import numpy as np
import pandas as pd
import streamlit as st

from streamlit_app.components.cards import status_badge
from streamlit_app.components.metrics import progress_bar
from streamlit_app.components.maps import render_location_map
from streamlit_app.utils.model_loader import repo_base_dir
from streamlit_app.utils.prediction import compute_call_drop


BASE_DIR = repo_base_dir()
MODEL_PATH = BASE_DIR / "Call Drop" / "xgboost_best.pkl"
FEATURE_PATH = BASE_DIR / "Call Drop" / "call_drop_feature_columns.pkl"


@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        return None
    return joblib.load(MODEL_PATH)


@st.cache_resource
def load_feature_columns_file():
    if not FEATURE_PATH.exists():
        return None
    return joblib.load(FEATURE_PATH)


def create_feature_row(
    feature_columns,
    rating,
    latitude,
    longitude,
    operator,
    state,
    network_type,
    travel_type,
):
    row = {col: 0 for col in feature_columns}

    if "Rating" in row:
        row["Rating"] = rating
    if "Latitude" in row:
        row["Latitude"] = latitude
    if "Longitude" in row:
        row["Longitude"] = longitude

    operator_col = f"Operator_{operator}"
    state_col = f"State_{state}"
    network_col = f"Network Type_{network_type}"
    travel_col = f"In Out Travelling_{travel_type}"

    if operator_col in row:
        row[operator_col] = 1
    if state_col in row:
        row[state_col] = 1
    if network_col in row:
        row[network_col] = 1
    if travel_col in row:
        row[travel_col] = 1

    return pd.DataFrame([row], columns=feature_columns)


def smart_insights(risk_category: str, network_type: str, travel_type: str) -> tuple[str, str]:
    if risk_category == "Low Risk":
        return (
            "Traffic appears stable. Continue monitoring for micro-spikes.",
            "Recommended actions: keep current handover thresholds; validate overnight KPIs.",
        )
    if risk_category == "Medium Risk":
        return (
            "Elevated drop probability suggests intermittent RF degradation.",
            "Recommended actions: check recent cell outages; review backhaul utilization; tune handover margins.",
        )
    if risk_category == "High Risk":
        return (
            "Risk aligns with RF instability during movement and congested serving cells.",
            "Recommended actions: increase tower density/sector capacity; adjust mobility parameters for better target selection.",
        )
    return (
        "Critical drops likely due to severe RF/RRC failures and/or backhaul congestion.",
        "Recommended actions: activate mitigation runbook (congestion relief + handover rebalancing); schedule rapid drive tests; escalate to NOC.",
    )


def render() -> None:
    st.markdown(
        """
        <div class="premium-card scanline" style="padding:18px;">
          <div style="display:flex; align-items:flex-start; justify-content:space-between; gap:16px;">
            <div>
              <div style="font-size:12px; color: rgba(255,255,255,0.62); letter-spacing:0.14em;">CALL DROP PREDICTION</div>
              <div style="font-size:30px; font-weight:1000; margin-top:8px;">AI Risk Console</div>
              <div style="color: rgba(255,255,255,0.72); margin-top:8px;">Estimate call-drop probability and generate enterprise-grade mitigation recommendations.</div>
            </div>
            <div style="min-width:260px;">
              <div style="padding:12px; border-radius:16px; border:1px solid rgba(34,230,255,0.18); background: rgba(10,18,38,0.55);">
                <div style="font-size:12px; color: rgba(255,255,255,0.62); font-weight:800;">AI Monitoring</div>
                <div style="font-size:18px; font-weight:1000; margin-top:6px;">24/7 Active</div>
                <div style="margin-top:10px; height:10px; border-radius:999px; background: rgba(255,255,255,0.08); overflow:hidden;">
                  <div style="width:78%; height:100%; background: linear-gradient(90deg, rgba(34,230,255,0.9), rgba(166,102,255,0.7));"></div>
                </div>
                <div style="margin-top:8px; font-size:12px; color: rgba(255,255,255,0.62);">Model latency ~ 120ms</div>
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    model = load_model()
    feature_columns = load_feature_columns_file()

    if model is None or feature_columns is None:
        st.error("Missing model artifacts for Call Drop prediction (model or feature columns).")
        return

    left, right = st.columns([1, 1.1], gap="large")

    with left:
        st.markdown("<div class='premium-card' style='padding:16px;'>", unsafe_allow_html=True)
        st.subheader("Input Context")
        with st.form("call_drop_form"):
            rating = st.slider("User Rating", 1, 5, 3)
            latitude = st.number_input("Latitude", value=12.9716, format="%.6f")
            longitude = st.number_input("Longitude", value=77.5946, format="%.6f")
            operator = st.selectbox("Operator", ["Airtel", "BSNL", "RJio", "Vodafone"])
            state = st.text_input("State", "Tamil Nadu")
            network_type = st.selectbox("Network Type", ["2G", "3G", "4G"])
            travel_type = st.selectbox("Travel Status", ["Indoor", "Outdoor", "Travelling"])
            submitted = st.form_submit_button("Run Prediction")
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='premium-card' style='padding:16px;'>", unsafe_allow_html=True)
        st.subheader("Prediction Results")

        if not submitted:
            status_badge("Awaiting inputs", tone="warn")
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            st.caption("Submit to compute call-drop risk and recommendations.")
            st.markdown("</div>", unsafe_allow_html=True)
            return

        with st.spinner("AI inference running… analyzing RF + mobility signals"):
            time.sleep(0.7)
            X_input = create_feature_row(
                feature_columns,
                rating,
                float(latitude),
                float(longitude),
                operator,
                state,
                network_type,
                travel_type,
            )
            out = compute_call_drop(model, X_input)

        if out is None:
            st.error("Model does not provide probability outputs (predict_proba missing).")
            st.markdown("</div>", unsafe_allow_html=True)
            return

        tone = (
            "good"
            if out.risk_category == "Low Risk"
            else "warn"
            if out.risk_category == "Medium Risk"
            else "bad"
            if out.risk_category == "High Risk"
            else "crit"
        )

        status_badge(out.risk_category, tone=tone)
        progress_bar("Call Drop Probability", out.call_drop_pct, tone="cyan")

        st.markdown(
            f"""
            <div style='margin-top:14px; display:flex; gap:12px; flex-wrap:wrap;'>
              <div style='flex:1 1 220px; padding:12px; border-radius:14px; border:1px solid rgba(34,230,255,0.18); background: rgba(10,18,38,0.55);'>
                <div style='font-size:12px; color: rgba(255,255,255,0.6); font-weight:800;'>Risk Score</div>
                <div style='font-size:26px; font-weight:1000; margin-top:6px;'>{out.risk_score:.1f}</div>
                <div style='font-size:12px; color: rgba(255,255,255,0.55); margin-top:4px;'>0-100 normalized severity</div>
              </div>
              <div style='flex:1 1 220px; padding:12px; border-radius:14px; border:1px solid rgba(166,102,255,0.18); background: rgba(10,18,38,0.55);'>
                <div style='font-size:12px; color: rgba(255,255,255,0.6); font-weight:800;'>Confidence</div>
                <div style='font-size:26px; font-weight:1000; margin-top:6px;'>{(0.62 + 0.38 * (1 - out.call_drop_pct / 100)):.1f}%</div>
                <div style='font-size:12px; color: rgba(255,255,255,0.55); margin-top:4px;'>heuristic confidence indicator</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        assessment, likely_causes = smart_insights(out.risk_category, network_type, travel_type)

        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        colA, colB = st.columns(2, gap="large")
        with colA:
            st.markdown("<div style='font-weight:1000;'>Network Quality Assessment</div>", unsafe_allow_html=True)
            st.caption(assessment)
            progress_bar("Stability Meter", max(0.0, 100 - out.call_drop_pct), tone="purple")
        with colB:
            st.markdown("<div style='font-weight:1000;'>Likely Causes</div>", unsafe_allow_html=True)
            st.caption(likely_causes)

        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        st.markdown("<div style='font-weight:1000;'>Recommended Actions</div>", unsafe_allow_html=True)
        st.caption(likely_causes.replace("Recommended actions:", ""))

        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        st.markdown("<div style='font-weight:1000;'>Interactive Map</div>", unsafe_allow_html=True)
        quality_score = float(np.clip(1.0 - (out.call_drop_pct / 100.0), 0.0, 1.0))
        render_location_map(float(latitude), float(longitude), quality_score)

        st.markdown("</div>", unsafe_allow_html=True)

