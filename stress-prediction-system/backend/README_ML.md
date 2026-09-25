# Rebuilt ML Pipeline

## Training

From `stress-prediction-system/backend`:

```bash
python -m pip install -r requirements.txt
python train_pipeline.py
```

Training creates:

- `trained_models/d1_pipeline.pkl`
- `trained_models/d2_pipeline.pkl`
- `trained_models/d1_metadata.json`
- `trained_models/d2_metadata.json`

The saved `.pkl` files contain the complete preprocessing + estimator pipeline. The Flask API does not load separate scalers or feature-list artifacts.

## Methodological safeguards

- Train/test split occurs before learned preprocessing.
- Hyperparameter selection uses stratified 5-fold CV on the training partition only.
- Model selection uses macro-F1.
- SMOTE is applied only to D2 training folds through an imbalanced-learn Pipeline, never to the held-out test set.
- D1 inverse coding is deterministic and shared by training and inference.
- D2 target labels are explicitly mapped: Distress=0, Eustress=1, No Stress=2.
- Final metrics are calculated once on the untouched test partition.

## Important

Do not use old `rf_*.pkl`, `scaler_*.pkl`, `features_*.pkl`, or `metrics.pkl` artifacts for the rebuilt system. They were produced by the previous pipeline and can be inconsistent with the current source.

Run the training script after cloning before starting Flask.
