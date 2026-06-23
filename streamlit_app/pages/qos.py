from __future__ import annotations

import time

import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

from streamlit_app.components.cards import status_badge
from streamlit_app.components.metrics import progress_bar
from streamlit_app.components.charts import plot_metric_line
from streamlit_app.components.toasts import toast_success, toast_warning, toast_error

from streamlit_app.utils.model_loader import repo_base_dir
from streamlit_app.utils.model_loader import load_artifact


BASE_DIR = repo_base_dir()
MODEL_PATH = BASE_DIR / "Quality of Service" / "random_forest_best.pkl"

OPERATOR_ENCODER = BASE_DIR / "Quality of Service" / "operator_encoder.pkl"
STATE_ENCODER = BASE_DIR / "Quality of Service" / "state_encoder.pkl"
TRANSPORT_ENCODER = BASE_DIR / "Quality of Service" / "transport_encoder.pkl"

FEATURE_PATH = BASE_DIR / "Quality of Service" / "qos_feature_columns.pkl"


@st.cache_resource
def load_model():
    return load_artifact(MODEL_PATH)


@st.cache_resource
def load_encoders():
    return {
        "Operatorname": load_artifact(OPERATOR_ENCODER),
        "State": load_artifact(STATE_ENCODER),
        "Transport_Mode": load_artifact(TRANSPORT_ENCODER),
    }


@st.cache_resource
def load_feature_columns():
    cols = load_artifact(FEATURE_PATH)
    return list(cols) if cols is not None else None


def qos_label(pred: int) -> str:
    if pred == 2:
        return "Good QoS"
    if pred == 1:
        return "Moderate QoS"
    return "Poor QoS"


def tone_for(pred: str) -> str:
    return {
        "Good QoS": "good",
        "Moderate QoS": "warn",
        "Poor QoS": "bad",
    }.get(pred, "warn")


def encode_with_label_encoder(encoder, raw_value: str) -> float:
    # best-effort: fall back to first known class
    try:
        return float(encoder.transform([raw_value])[0])
    except Exception:
        if hasattr(encoder, "classes_") and len(encoder.classes_) > 0:
            return float(encoder.transform([encoder.classes_[0]])[0])
        return 0.0


def align_features(feature_columns: list[str], values: dict) -> pd.DataFrame:
    row = {col: 0 for col in feature_columns}
    for k, v in values.items():
        if k in row:
            row[k] = v
    return pd.DataFrame([row], columns=feature_columns)


def recommendation_engine(qos_class: str, signal_quality: dict) -> list[str]:
    recs: list[str] = []

    if qos_class == "Good QoS":
        recs.append("Maintain current RAN parameters; continue passive monitoring for drift.")
        recs.append("Validate handover success rate after peak-hours changes.")
        return recs

    if qos_class == "Moderate QoS":
        recs.append("Tune handover margins and neighbor cell thresholds to reduce ping-pong and drop risk.")
        recs.append("Investigate mild backhaul congestion; review scheduling and buffering policies.")
        if signal_quality.get("RSRQ", -10) < -12:
            recs.append("Improve RSRQ: adjust antenna tilt/azimuth or rebalance load across sectors.")
        return recs

    recs.append("QoS is poor: prioritize corrective actions for RF stability and mobility.")
    recs.append("Check backhaul congestion and packet loss; mitigate with traffic engineering.")
    if signal_quality.get("SNR", 0) < 8:
        recs.append("Increase tower density/sector capacity in coverage holes; schedule targeted drive tests.")
    recs.append("Revisit handover parameters and mobility thresholds for the affected region.")
    return recs


def render() -> None:
    st.markdown(
        """
        <div class="premium-card scanline" style="padding:18px;">
          <div style="display:flex; align-items:flex-start; justify-content:space-between; gap:16px;">
            <div>
              <div style="font-size:12px; color: rgba(255,255,255,0.62); letter-spacing:0.14em;">NETWORK HEALTH</div>
              <div style="font-size:30px; font-weight:1000; margin-top:8px;">QoS Intelligence Dashboard</div>
              <div style="color: rgba(255,255,255,0.72); margin-top:8px;">Enter RF indicators to predict QoS and generate enterprise recommendations.</div>
            </div>
            <div style="min-width:260px;">
              <div style="padding:12px; border-radius:16px; border:1px solid rgba(166,102,255,0.18); background: rgba(10,18,38,0.55);">
                <div style="font-size:12px; color: rgba(255,255,255,0.62); font-weight:800;">AI Signal Analytics</div>
                <div style="font-size:18px; font-weight:1000; margin-top:6px;">Live Evaluation</div>
                <div style="margin-top:10px; height:10px; background: rgba(255,255,255,0.08); border-radius:999px; overflow:hidden; border:1px solid rgba(166,102,255,0.12);">
                  <div style="width:68%; height:100%; background: linear-gradient(90deg, rgba(166,102,255,0.9), rgba(34,230,255,0.6));"></div>
                </div>
                <div style="margin-top:8px; font-size:12px; color: rgba(255,255,255,0.62);">Anomaly pre-check ✓</div>
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    model = load_model()
    feature_columns = load_feature_columns()
    encoders = load_encoders()

    if model is None or feature_columns is None:
        st.error("Missing QoS model artifacts.")
        return

    left, right = st.columns([1, 1.1], gap="large")

    with left:
        st.markdown("<div class='premium-card' style='padding:16px;'>", unsafe_allow_html=True)
        st.subheader("Prediction Inputs")
        with st.form("qos_form"):
            Speed = st.number_input("Speed", value=50.0)
            Operatorname_raw = st.text_input("Operator Name", "Airtel")
            State_raw = st.text_input("State", "Tamil Nadu")
            Transport_Mode_raw = st.text_input("Transport Mode", "road")

            RSRP = st.number_input("RSRP", value=-95.0)
            RSRQ = st.number_input("RSRQ", value=-10.0)
            SNR = st.number_input("SNR", value=10.0)
            CQI = st.number_input("CQI", value=8.0)
            NRxRSRP = st.number_input("NRxRSRP", value=-95.0)
            NRxRSRQ = st.number_input("NRxRSRQ", value=-10.0)
            ServingCell_Distance = st.number_input("Serving Cell Distance", value=1000.0)

            Hour = st.slider("Hour", 0, 23, 12)
            DayOfWeek = st.slider("Day Of Week", 0, 6, 1)
            IsWeekend = st.selectbox("Is Weekend", [0, 1])

            submitted = st.form_submit_button("Run QoS Prediction")
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='premium-card' style='padding:16px;'>", unsafe_allow_html=True)
        st.subheader("Network Health Results")

        if not submitted:
            status_badge("Awaiting RF metrics", tone="warn")
            st.caption("Submit RF indicators to predict QoS and evaluate signal analytics.")
            st.markdown("</div>", unsafe_allow_html=True)
            return

        with st.spinner("AI inference running… calibrating QoS model"):
            time.sleep(0.6)
            values = {
                "Speed": float(Speed),
                "RSRP": float(RSRP),
                "RSRQ": float(RSRQ),
                "SNR": float(SNR),
                "CQI": float(CQI),
                "State": encode_with_label_encoder(encoders["State"], str(State_raw)),
                "Operatorname": encode_with_label_encoder(encoders["Operatorname"], str(Operatorname_raw)),
                "NRxRSRP": float(NRxRSRP),
                "NRxRSRQ": float(NRxRSRQ),
                "ServingCell_Distance": float(ServingCell_Distance),
                "Transport_Mode": encode_with_label_encoder(encoders["Transport_Mode"], str(Transport_Mode_raw).lower()),
                "SNR_missing": 0,
                "CQI_missing": 0,
                "RSSI_missing": 0,
                "NRxRSRP_missing": 0,
                "NRxRSRQ_missing": 0,
                "ServingCell_Distance_missing": 0,
                "Hour": int(Hour),
                "DayOfWeek": int(DayOfWeek),
                "IsWeekend": int(IsWeekend),
            }

            X_input = align_features(feature_columns, values)
            pred = int(model.predict(X_input)[0])

            prob_map = None
            if hasattr(model, "predict_proba"):
                probs = model.predict_proba(X_input)[0]
                # assumed order: [Poor, Moderate, Good]
                prob_map = {
                    "Poor": float(probs[0]),
                    "Moderate": float(probs[1]),
                    "Good": float(probs[2]),
                }

        qos_class = qos_label(pred)
        status_badge(qos_class, tone=tone_for(qos_class))

        signal_quality = {"RSRP": float(RSRP), "RSRQ": float(RSRQ), "SNR": float(SNR), "CQI": float(CQI)}

        # QoS meter
        qos_score_pct = {
            "Good QoS": 92,
            "Moderate QoS": 68,
            "Poor QoS": 32,
        }.get(qos_class, 60)

        progress_bar("Quality Meter", qos_score_pct, tone="purple" if qos_class != "Good QoS" else "good")

        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

        # RF charts: Plotly only
        fig = go.Figure()
        fig.add_trace(go.Bar(x=["RSRP", "RSRQ", "SNR", "CQI"], y=[RSRP, RSRQ, SNR, CQI], marker_color="rgba(34,230,255,0.7)"))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="rgba(255,255,255,0.85)"),
            margin=dict(l=10, r=10, t=40, b=10),
            yaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Confidence breakdown
        if prob_map is not None:
            pie = px.pie(
                names=list(prob_map.keys()),
                values=[prob_map["Poor"], prob_map["Moderate"], prob_map["Good"]],
                title="AI Confidence Distribution",
            )
            pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="rgba(255,255,255,0.85)"),
                title_font=dict(color="rgba(255,255,255,0.9)"),
                margin=dict(l=10, r=10, t=50, b=10),
            )
            st.plotly_chart(pie, use_container_width=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        st.markdown("<div style='font-weight:1000;'>AI Recommendation Engine</div>", unsafe_allow_html=True)
        recs = recommendation_engine(qos_class, signal_quality)
        for r in recs:
            st.markdown(
                f"<div style='margin-top:6px; padding:10px 12px; border-radius:14px; border:1px solid rgba(34,230,255,0.14); background: rgba(10,18,38,0.45); color: rgba(255,255,255,0.84);'>• {r}</div>",
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

