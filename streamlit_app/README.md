# LTE QoS & Call Drop Predictor (Streamlit)

## Project Structure
- `app.py`: main Streamlit entrypoint
- `pages/qos.py`: LTE QoS prediction
- `pages/call_drop.py`: Call Drop prediction

## Models used (from repo)
- QoS: `Quality of Service/random_forest_best.pkl`
- Call Drop: `Call Drop/rf_best_balanced.pkl`

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

> If you run from a different directory, ensure paths resolve to the repo root (the app uses `os.getcwd()` / relative model paths).

## Notes
This app uses best-effort feature alignment using `feature_names_in_` when available on the loaded model.
Exact preprocessing (LabelEncoder / one-hot columns) may require additional saved preprocessing artifacts.

