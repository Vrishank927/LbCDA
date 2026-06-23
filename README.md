LbCDA — Telecom Network Intelligence (ML)

An ML-first project that predicts **(1) Call Drop risk** and **(2) LTE QoS health** from telecom/network indicators, and converts the predictions into actionable insights.

> The repository also includes a **Streamlit** web UI for interactive inference and visualization.

---

## Highlights

- **Call Drop Prediction**: estimates the probability of call drops and maps it to a normalized risk score + category.
- **LTE QoS Prediction**: predicts QoS class (Good / Moderate / Poor) from RF + mobility + context features.
- **Feature-aligned inference**: uses stored feature-column order (single-row DataFrame aligned to training schema).
- **Recommendation Engine**: converts predicted outcomes into operator-friendly recommendations.

---

## Models & Artifacts

The app loads pre-trained model artifacts stored in the repo:

### 1) LTE QoS Model
- **Model**: `Quality of Service/random_forest_best.pkl`
- **Encoders**:
  - `Quality of Service/operator_encoder.pkl`
  - `Quality of Service/state_encoder.pkl`
  - `Quality of Service/transport_encoder.pkl`
- **Feature columns**: `Quality of Service/qos_feature_columns.pkl`

**Inference approach**
- Raw categorical inputs are encoded using the saved LabelEncoders.
- A single-row feature vector is built and aligned to `qos_feature_columns.pkl`.
- The model predicts the QoS class, and (if available) `predict_proba` is used to produce confidence distribution.

### 2) Call Drop Model
- **Model**: `Call Drop/xgboost_best.pkl`
- **Feature columns**: `Call Drop/call_drop_feature_columns.pkl`

**Inference approach**
- A single-row feature vector is created using one-hot flags for categorical context (operator/state/network type/travel type) based on the stored training feature schema.
- Inference uses `predict_proba` (model must expose probability outputs).
- Probability is mapped to:
  - **call-drop percentage**
  - **risk score** (0–100)
  - **risk category** (Low / Medium / High / Critical)

---

## Feature Engineering (High-Level)

### QoS (Classification)
- Numeric RF indicators: e.g., **RSRP, RSRQ, SNR, CQI**
- Mobility/time context: **Hour, DayOfWeek, IsWeekend**
- Categorical context encoded via stored encoders:
  - **Operatorname**
  - **State**
  - **Transport_Mode**
- Final input is a **DataFrame aligned to training columns**.

### Call Drop (Classification/Probabilistic)
- Inputs include:
  - User context: **Rating**
  - Location: **Latitude, Longitude**
  - Categorical context (one-hot via feature-column presence):
    - Operator, State
    - Network type (2G/3G/4G)
    - Travel type (Indoor/Outdoor/Travelling)
- Final input is again aligned to the stored **feature-columns order**.

---

## Post-processing & Decision Logic

### Call Drop risk mapping
The system converts drop probability `p_drop` into a severity signal:
- `p < 0.2`  → **Low Risk**
- `0.2 ≤ p < 0.5` → **Medium Risk**
- `0.5 ≤ p < 0.8` → **High Risk**
- `p ≥ 0.8` → **Critical**

### QoS recommendation engine
Given the predicted QoS class (Good / Moderate / Poor), plus RF signal quality context, the system generates enterprise-friendly recommendations (e.g., parameter tuning, congestion investigation, RF stability actions).

---

## Reproducibility Notes

- Inference expects the repo’s stored artifacts (models, encoders, feature-column pickles).
- The inference code uses **best-effort encoding** (LabelEncoder transform with a fallback for unseen categories).
- Feature vectors are created as **single-row DataFrames** and aligned to training schema to prevent column-order mismatches.

---

## Streamlit (UI) — brief

The ML inference is exposed through a **Streamlit** app (`streamlit_app/`). The UI provides:
- interactive inputs for QoS and Call Drop
- live prediction results with confidence visualization
- an “enterprise dashboard” landing page

---

## Project Layout (relevant ML code)

- `streamlit_app/pages/qos.py` — QoS input schema + QoS inference + recommendations
- `streamlit_app/pages/call_drop.py` — Call Drop input schema + Call Drop inference + risk mapping
- `streamlit_app/utils/model_loader.py` — cached loading of pickled artifacts
- `streamlit_app/utils/prediction.py` — probability → risk/category logic

---

## Run (quick)

```bash
cd streamlit_app
pip install -r requirements.txt
streamlit run app.py
```

---


