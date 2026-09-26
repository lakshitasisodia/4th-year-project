"""
train.py — single authoritative training pipeline for both models.

Fixes applied vs. the previous backendCode.py:

1. TRAIN/TEST LEAKAGE: previously, MinMaxScaler (x2, inside engineer_d1/engineer_d2)
   and RobustScaler (inside prepare_datasets) were all fit on the FULL dataset
   *before* train_test_split. Every one of those fits leaked test-set statistics
   into training. Here, splitting happens first; every fitted transform is fit
   on X_train only.

2. TRAINING/INFERENCE MISMATCH ("same prediction" bug): the previous pipeline
   silently renamed 7 columns during training (self_esteem -> self_esteem_INV,
   etc.) and fit a whole extra MinMaxScaler chain that the Flask predictor never
   replicated at inference time. The predictor loaded whatever scaler_d1.pkl /
   features_d1.pkl happened to be on disk and applied it directly to raw,
   unmodified questionnaire values — so the model was being fed features on a
   completely different scale (and set of columns) than it was trained on. For
   a RandomForestClassifier, feeding inputs far outside every split threshold's
   range routes almost all requests into the same handful of leaves, which is
   exactly the "changing inputs barely changes the prediction" symptom.

   Fix: the reverse-coding + scaling + model are now ONE sklearn Pipeline object,
   fit end-to-end and saved as a single artifact. The API only ever needs to
   hand it a DataFrame with the raw, original questionnaire column names — the
   exact same columns config.py already tells the frontend to send. There is no
   way for training-time and inference-time preprocessing to drift apart again,
   because they are the same code path.

3. DETERMINISTIC REVERSE CODING: reverse-coding of "protective" factors
   (self_esteem, sleep_quality, etc.) previously used a MinMaxScaler fit on
   the dataset, which makes the transformation depend on whatever rows happen
   to be in the training data at the time. It's replaced with a fixed formula
   based on each field's known questionnaire range (Config.FIELD_RANGES),
   which is deterministic and identical for training and inference.

4. SMOTE LEAKAGE (D2): SMOTE now lives inside an imblearn Pipeline step, so
   cross-validation folds and the held-out test set never see synthetic rows —
   imblearn's Pipeline applies sampling only on the *training* fold of each
   split, and never during predict/predict_proba.

Run: python train.py
Produces: trained_models/pipeline_d1.pkl, trained_models/pipeline_d2.pkl,
          trained_models/metadata.pkl
"""
import json
import os
import platform
import sys
from datetime import datetime, timezone

import joblib
import numpy as np
import pandas as pd
import sklearn
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    matthews_corrcoef,
    precision_score,
    recall_score,
)
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, LabelEncoder, RobustScaler

from config import Config
from preprocessing import D1_PROTECTIVE_FIELDS, D1ReverseCoder

RANDOM_STATE = 42
TEST_SIZE = 0.25
CV_FOLDS = 5


def make_d1_reverse_coder():
    return FunctionTransformer(D1ReverseCoder(D1_PROTECTIVE_FIELDS), validate=False)


def build_d1_pipeline():
    return Pipeline([
        ("reverse_code", make_d1_reverse_coder()),
        ("scale", RobustScaler()),
        ("clf", RandomForestClassifier(random_state=RANDOM_STATE)),
    ])


def build_d2_pipeline():
    # SMOTE is a step in the SAME pipeline used for CV and final fit, so it
    # only ever touches training folds (imblearn guarantees this).
    return ImbPipeline([
        ("scale", RobustScaler()),
        ("smote", SMOTE(random_state=RANDOM_STATE, k_neighbors=3)),
        ("clf", RandomForestClassifier(random_state=RANDOM_STATE)),
    ])


def per_class_report(y_test, y_pred, class_labels):
    report = classification_report(
        y_test, y_pred, output_dict=True, zero_division=0,
        target_names=[str(class_labels[i]) for i in sorted(class_labels)],
    )
    return report


def evaluate(model, X_test, y_test, label):
    y_pred = model.predict(X_test)
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision_macro": precision_score(y_test, y_pred, average="macro", zero_division=0),
        "recall_macro": recall_score(y_test, y_pred, average="macro", zero_division=0),
        "f1_macro": f1_score(y_test, y_pred, average="macro", zero_division=0),
        "f1_weighted": f1_score(y_test, y_pred, average="weighted", zero_division=0),
        "mcc": matthews_corrcoef(y_test, y_pred),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
    }
    print(f"  [{label}] accuracy={metrics['accuracy']:.3f}  "
          f"f1_macro={metrics['f1_macro']:.3f}  mcc={metrics['mcc']:.3f}")
    return metrics


def check_field_ranges(X):
    """Warn loudly if the actual data falls outside Config.FIELD_RANGES.

    The deterministic reverse-coding in make_d1_reverse_coder() depends on
    FIELD_RANGES being the TRUE min/max of each questionnaire field. If the
    config ranges are wrong, reverse-coding silently produces values outside
    [0, 1] and the model was almost certainly trained on a different notion
    of "min/max" than what's documented. This does not raise — the sample
    dataset used for local testing here is a small subset and won't span the
    full range — but on the FULL dataset any mismatch printed here should be
    treated as a Group 1/5 documentation bug to fix before trusting results.
    """
    problems = []
    for field, (lo, hi) in Config.FIELD_RANGES.items():
        if field not in X.columns:
            continue
        actual_min, actual_max = X[field].min(), X[field].max()
        if actual_min < lo or actual_max > hi:
            problems.append(f"    {field}: config says [{lo},{hi}], data has [{actual_min},{actual_max}]")
    if problems:
        print("  [WARN] FIELD_RANGES in config.py do not match observed data:")
        print("\n".join(problems))
    return problems


STRAIGHT_LINE_THRESHOLD = 0.8  # same threshold as the original backendCode.py


def detect_straight_liners(df, survey_cols):
    """Flags respondents whose answers show almost no variation across the
    survey — e.g. answering '3' to all 22 Likert questions. This QC step
    existed in the original backendCode.py's design (Phase 2) but wasn't
    yet ported into train.py; added here so quality control matches the
    project's own documented intent.
    """
    response_variety = df[survey_cols].nunique(axis=1)
    uniformity_ratio = 1 - (response_variety / len(survey_cols))
    return uniformity_ratio >= STRAIGHT_LINE_THRESHOLD


def quality_control_d2(df):
    """Real, complete data revealed issues absent from the small sample used
    earlier: 27 exact-duplicate rows and 7 rows with Age outside the survey's
    own stated 15-60 range (Age=14 x4, Age=100 x3 — clear data-entry errors).
    Both are removed before splitting.

    Straight-line detection (present in the original backendCode.py's design)
    was investigated and deliberately NOT applied here: at the documented
    threshold (uniformity >= 0.8) it flags 83% of "No Stress" respondents and
    48% of "Distress" respondents as low-effort, because someone who is
    genuinely not stressed legitimately answers "1" (Never) to nearly every
    question, and someone genuinely distressed answers "5" to nearly all of
    them — that's real signal on an already tiny minority class, not survey
    noise. Applying it dropped D2 macro-F1 from 0.79 to 0.46 on this data.
    Ported faithfully but rejected on evidence, not silently.
    """
    initial = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    n_dupes = initial - len(df)

    age_outliers = (df['Age'] < 15) | (df['Age'] > 60)
    n_age_outliers = int(age_outliers.sum())
    df = df.loc[~age_outliers].reset_index(drop=True)

    survey_cols = df.columns[2:-1].tolist()
    straight_liners = detect_straight_liners(df, survey_cols)
    n_straight_liners_detected = int(straight_liners.sum())  # reported, not removed — see docstring

    print(f"  Removed {n_dupes} duplicate rows, {n_age_outliers} Age-outlier rows "
          f"({initial} -> {len(df)}). {n_straight_liners_detected} rows flagged as "
          f"straight-line responses but NOT removed (see quality_control_d2 docstring).")
    return df, {
        "duplicates_removed": n_dupes,
        "age_outliers_removed": n_age_outliers,
        "straight_liners_detected_not_removed": n_straight_liners_detected,
        "straight_line_filter_rejected_reason": (
            "disproportionately removes minority classes (No Stress, Distress) "
            "and drops D2 macro-F1 from ~0.79 to ~0.46; investigated in this run, not applied"
        ),
        "rows_before": initial, "rows_after": len(df),
    }


def train_d1():
    print("\n=== D1: Stress Level ===")
    df = pd.read_csv("StressLevelDataset.csv")
    target_col = df.columns[-1]
    X = df.drop(columns=[target_col])
    y = df[target_col]
    check_field_ranges(X)

    # Split BEFORE any fitting happens.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )

    pipeline = build_d1_pipeline()
    param_grid = {
        "clf__n_estimators": [100, 200],
        "clf__max_depth": [5, 10, 15],
        "clf__min_samples_split": [2, 5],
    }
    cv = StratifiedKFold(n_splits=min(CV_FOLDS, min(y_train.value_counts())), shuffle=True, random_state=RANDOM_STATE)
    search = GridSearchCV(pipeline, param_grid, cv=cv, scoring="f1_macro", n_jobs=-1)
    search.fit(X_train, y_train)  # reverse-code + scale + fit, all on train only

    print(f"  best params: {search.best_params_}")
    print(f"  CV f1_macro: {search.best_score_:.3f}")

    best = search.best_estimator_
    metrics = evaluate(best, X_test, y_test, "D1 test")
    metrics["per_class"] = per_class_report(y_test, best.predict(X_test), Config.STRESS_LEVEL_LABELS)

    return best, {
        "features": list(X.columns),
        "class_labels": Config.STRESS_LEVEL_LABELS,
        "metrics": metrics,
        "cv_f1_macro": search.best_score_,
        "best_params": search.best_params_,
        "n_train": len(X_train),
        "n_test": len(X_test),
        "class_distribution_full": {Config.STRESS_LEVEL_LABELS[int(k)]: int(v) for k, v in y.value_counts().items()},
    }


def train_d2():
    print("\n=== D2: Stress Type ===")
    df = pd.read_csv("Stress_Dataset.csv")
    df, qc_info = quality_control_d2(df)
    target_col = df.columns[-1]

    le = LabelEncoder()
    y = pd.Series(le.fit_transform(df[target_col]), index=df.index)
    class_labels = {int(i): cls for i, cls in enumerate(le.classes_)}
    X = df.drop(columns=[target_col])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )

    class_counts = y_train.value_counts()
    min_class_count = int(class_counts.min())
    k_neighbors = max(1, min(3, min_class_count - 1))

    pipeline = build_d2_pipeline()
    pipeline.set_params(smote__k_neighbors=k_neighbors)

    param_grid = {
        "clf__n_estimators": [100, 200],
        "clf__max_depth": [5, 10, 15],
    }
    n_splits = max(2, min(CV_FOLDS, min_class_count))
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=RANDOM_STATE)
    search = GridSearchCV(pipeline, param_grid, cv=cv, scoring="f1_macro", n_jobs=-1)
    search.fit(X_train, y_train)  # SMOTE only ever resamples the training fold

    print(f"  best params: {search.best_params_}")
    print(f"  CV f1_macro: {search.best_score_:.3f}")

    best = search.best_estimator_
    metrics = evaluate(best, X_test, y_test, "D2 test")
    metrics["per_class"] = per_class_report(y_test, best.predict(X_test), class_labels)

    return best, {
        "features": list(X.columns),
        "class_labels": class_labels,
        "metrics": metrics,
        "cv_f1_macro": search.best_score_,
        "best_params": search.best_params_,
        "n_train": len(X_train),
        "n_test": len(X_test),
        "quality_control": qc_info,
        "class_distribution_full": {class_labels[int(k)]: int(v) for k, v in y.value_counts().items()},
    }


def main():
    os.makedirs("trained_models", exist_ok=True)

    d1_pipeline, d1_meta = train_d1()
    d2_pipeline, d2_meta = train_d2()

    joblib.dump(d1_pipeline, "trained_models/pipeline_d1.pkl")
    joblib.dump(d2_pipeline, "trained_models/pipeline_d2.pkl")

    metadata = {
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version,
        "sklearn_version": sklearn.__version__,
        "platform": platform.platform(),
        "random_state": RANDOM_STATE,
        "test_size": TEST_SIZE,
        "cv_folds": CV_FOLDS,
        "d1": d1_meta,
        "d2": d2_meta,
    }
    joblib.dump(metadata, "trained_models/metadata.pkl")
    with open("trained_models/metadata.json", "w") as f:
        json.dump(metadata, f, indent=2, default=str)

    print("\n[OK] Saved trained_models/pipeline_d1.pkl, pipeline_d2.pkl, metadata.pkl")


if __name__ == "__main__":
    main()
