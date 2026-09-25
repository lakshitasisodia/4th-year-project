import json
from pathlib import Path
import joblib
import pandas as pd
from models.preprocessing import D1_FEATURES, D2_FEATURES

BASE=Path(__file__).resolve().parents[1]
MODELS=BASE/"trained_models"

def test_artifacts_exist():
    assert (MODELS/"d1_pipeline.pkl").exists()
    assert (MODELS/"d2_pipeline.pkl").exists()
    assert (MODELS/"d1_metadata.json").exists()
    assert (MODELS/"d2_metadata.json").exists()

def test_d1_pipeline_accepts_raw_schema():
    model=joblib.load(MODELS/"d1_pipeline.pkl")
    row=pd.DataFrame([{c:0 for c in D1_FEATURES}])
    row["blood_pressure"]=1
    assert len(model.predict(row))==1

def test_d2_pipeline_accepts_raw_schema():
    model=joblib.load(MODELS/"d2_pipeline.pkl")
    row=pd.DataFrame([{c:1 for c in D2_FEATURES}])
    row["Gender"]=0
    row["Age"]=20
    assert len(model.predict(row))==1

def test_metadata_is_machine_readable():
    for name in ("d1","d2"):
        meta=json.loads((MODELS/f"{name}_metadata.json").read_text())
        assert "metrics" in meta
        assert "f1_macro" in meta["metrics"]
        assert "selected_algorithm" in meta
