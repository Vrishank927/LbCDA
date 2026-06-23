from __future__ import annotations

from pathlib import Path

import joblib
import streamlit as st


def repo_base_dir() -> Path:
    # streamlit_app/utils/model_loader.py -> repo root
    return Path(__file__).resolve().parents[2]


@st.cache_resource
def load_artifact(path: Path):
    if not path.exists():
        return None
    return joblib.load(path)

