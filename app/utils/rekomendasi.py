import os
import joblib
import numpy as np

_DIR = os.path.dirname(__file__)
_XGB = os.path.join(_DIR, 'model_rekomendasi_xgb.pkl')
_RF = os.path.join(_DIR, 'model_rekomendasi_rf.pkl')

_artifact = None
_model = None
_le = None
if os.path.exists(_XGB):
    _artifact = joblib.load(_XGB)
elif os.path.exists(_RF):
    _artifact = joblib.load(_RF)
if isinstance(_artifact, dict) and 'model' in _artifact:
    _model = _artifact.get('model')
    _le = _artifact.get('label_encoder')
else:
    _model = _artifact

def prediksi_paket(X_input):
    X_input = np.array(X_input).reshape(1, -1)
    y_pred = _model.predict(X_input)
    if _le is not None:
        y_label = _le.inverse_transform(y_pred)[0]
    else:
        s = str(y_pred[0]).strip()
        if s in {"Paket 1", "Paket 2", "Paket 3"}:
            y_label = s
        elif s in {"0", "1", "2"}:
            y_label = f"Paket {int(s)+1}"
        else:
            y_label = "Paket 1"
    y_proba = _model.predict_proba(X_input) if hasattr(_model, 'predict_proba') else None
    return y_label, (y_proba[0] if y_proba is not None else None)
