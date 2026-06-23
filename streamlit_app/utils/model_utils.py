from __future__ import annotations

import os
import traceback
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import joblib
import pandas as pd
import streamlit as st


def repo_base_dir() -> Path:
    # streamlit_app/utils/model_utils.py -> repo root
    return Path(__file__).resolve().parents[2]


def safe_load_joblib(path: Path) -> Any:
    return joblib.load(path)


@st.cache_resource
def load_model_artifact(model_path: Path) -> Any:
    if not model_path.exists():
        st.error(f"Model artifact not found:\n{model_path}")
        return None
    return safe_load_joblib(model_path)


@st.cache_resource
def load_feature_columns(feature_path: Path) -> Optional[List[str]]:
    if not feature_path.exists():
        st.error(f"Feature columns artifact not found:\n{feature_path}")
        return None
    cols = safe_load_joblib(feature_path)
    # Expect list-like of column names
    return list(cols)


@st.cache_resource
def load_label_encoder(encoder_path: Path):
    if not encoder_path.exists():
        return None
    return safe_load_joblib(encoder_path)


def encode_with_label_encoder(
    encoder,
    raw_value: str,
    unknown_policy: str = "fallback_min"
) -> float:
    """Return numeric code compatible with sklearn LabelEncoder.

    unknown_policy:
      - "fallback_min": use encoder.transform([encoder.classes_[0]])
      - "raise": re-raise sklearn error
    """

    if encoder is None:
        raise ValueError("Encoder is None; cannot encode categorical value.")

    try:
        return float(encoder.transform([raw_value])[0])
    except Exception:
        if unknown_policy == "raise":
            raise

        # fallback_min
        if hasattr(encoder, "classes_") and len(encoder.classes_) > 0:
            return float(encoder.transform([encoder.classes_[0]])[0])
        # Last resort
        return 0.0


def align_features(
    feature_columns: List[str],
    values: Dict[str, Any],
) -> pd.DataFrame:
    """Create a single-row DataFrame with columns in exact training order."""
    row = {col: 0 for col in feature_columns}
    for key, value in values.items():
        if key in row:
            row[key] = value
    return pd.DataFrame([row], columns=feature_columns)


def diagnostic_dump(
    *,
    label: str,
    X_input: pd.DataFrame,
    model: Any,
    feature_columns: Optional[List[str]] = None,
) -> Dict[str, Any]:
    info: Dict[str, Any] = {}
    info["label"] = label
    info["X_input.shape"] = tuple(X_input.shape)
    info["X_input.columns.head"] = list(X_input.columns[:20])
    info["X_input.columns.tail"] = list(X_input.columns[-20:])
    info["X_input.dtypes"] = {c: str(t) for c, t in X_input.dtypes.items()}

    if feature_columns is not None:
        info["expected_feature_count"] = len(feature_columns)
        info["provided_feature_count"] = X_input.shape[1]

    if hasattr(model, "n_features_in_"):
        info["model.n_features_in_"] = int(model.n_features_in_)

    return info


def render_exception(e: Exception):
    # UI-friendly error without dumping huge internal state by default
    st.error(f"Prediction failed: {e}")
    st.code(traceback.format_exc())


