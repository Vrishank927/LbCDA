from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

import numpy as np


@dataclass
class CallDropPrediction:
    call_drop_pct: float
    risk_score: float
    risk_category: str
    probability: np.ndarray


def risk_from_probability(p: float) -> tuple[float, str]:
    """Map call-drop probability into a normalized risk score and a category."""
    risk_score = float(np.clip(p * 100.0, 0.0, 100.0))
    if p < 0.2:
        return risk_score, "Low Risk"
    if p < 0.5:
        return risk_score, "Medium Risk"
    if p < 0.8:
        return risk_score, "High Risk"
    return risk_score, "Critical"


def compute_call_drop(pred_model: Any, X) -> Optional[CallDropPrediction]:
    """Return rich call-drop prediction output."""
    if not hasattr(pred_model, "predict_proba"):
        return None

    proba = pred_model.predict_proba(X)[0]

    # Convention: assume binary classes where index 1 is call-drop.
    # If model was trained differently, you can re-map here.
    p_drop = float(proba[1])
    pct = round(p_drop * 100.0, 2)
    risk_score, risk_category = risk_from_probability(p_drop)
    return CallDropPrediction(
        call_drop_pct=pct,
        risk_score=risk_score,
        risk_category=risk_category,
        probability=proba,
    )

