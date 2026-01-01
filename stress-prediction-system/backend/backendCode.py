import pandas as pd
import numpy as np
import warnings
from scipy.stats import chi2_contingency
from sklearn.covariance import EllipticEnvelope
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.preprocessing import RobustScaler, LabelEncoder, MinMaxScaler
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                            f1_score, classification_report, confusion_matrix,
                            matthews_corrcoef)
from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os

warnings.filterwarnings('ignore')

OUTLIER_CONTAMINATION = 0.05
STRAIGHT_LINE_THRESHOLD = 0.8
CRONBACH_ALPHA_THRESHOLD = 0.7
RANDOM_STATE = 42
TEST_SIZE = 0.25
CV_FOLDS = 5

def detect_straight_lining(df, feature_cols):
    response_variance = df[feature_cols].nunique(axis=1)
    total_questions = len(feature_cols)
    uniformity_ratio = 1 - (response_variance / total_questions)
    straight_liners = uniformity_ratio >= STRAIGHT_LINE_THRESHOLD
    print(f"   Detected {straight_liners.sum()} straight-line respondents ({100*straight_liners.mean():.1f}%)")
    return straight_liners

def calculate_cronbach_alpha(df, items):
    item_data = df[items].dropna()
    n_items = len(items)
    item_variances = item_data.var(axis=0, ddof=1)
    total_var = item_data.sum(axis=1).var(ddof=1)
    alpha = (n_items / (n_items - 1)) * (1 - item_variances.sum() / total_var)
    return alpha

def print_header(title, level=1):
    if level == 1:
        print("\n" + "="*80)
        print(f"  {title}")
        print("="*80)
    else:
        print(f"\n{'─'*70}")
        print(f"  {title}")
        print('─'*70)

def load_datasets():
    print_header("PHASE 1: DATA LOADING")
    
    df1 = pd.read_csv('StressLevelDataset.csv')
    print(f"[OK] Dataset 1: {df1.shape[0]} rows, {df1.shape[1]} columns")
    
    df2 = pd.read_csv('Stress_Dataset.csv')
    print(f"[OK] Dataset 2: {df2.shape[0]} rows, {df2.shape[1]} columns")
    
    print(f"\nD1 columns: {df1.columns.tolist()}")
    print(f"D2 columns: {df2.columns.tolist()}")
    
    print_header("Missing Values", level=2)
    print(f"D1 missing: {df1.isnull().sum().sum()}")
    print(f"D2 missing: {df2.isnull().sum().sum()}")
    
    print_header("Target Distribution", level=2)
    print("D1:")
    print(df1.iloc[:, -1].value_counts().sort_index())
    print("\nD2:")
    print(df2.iloc[:, -1].value_counts())
    
    return df1, df2

def quality_control_d2(df2):
    print_header("PHASE 2: QUALITY CONTROL (D2)")
    
    df_clean = df2.copy()
    initial_rows = len(df_clean)
    
    print_header("Age Outliers", level=2)
    age_col = df_clean.columns[1]
    age_outliers = (df_clean[age_col] > 60) | (df_clean[age_col] < 15)
    print(f"   Age outliers: {age_outliers.sum()}")
    if age_outliers.sum() > 0:
        df_clean = df_clean[~age_outliers]
    
    print_header("Straight-Line Detection", level=2)
    survey_cols = df_clean.columns[2:-1].tolist()
    straight_liners = detect_straight_lining(df_clean, survey_cols)
    if straight_liners.sum() > 0:
        df_clean = df_clean[~straight_liners]
    
    removed = initial_rows - len(df_clean)
    print_header("Summary", level=2)
    print(f"   Initial: {initial_rows}")
    print(f"   Removed: {removed} ({100*removed/initial_rows:.1f}%)")
    print(f"   Final: {len(df_clean)}")
    
    return df_clean

def engineer_d1(df1):
    print_header("PHASE 3: FEATURE ENGINEERING (D1)")
    
    df_proc = df1.copy()
    target_col = df_proc.columns[-1]
    
    protective_cols = ['self_esteem', 'sleep_quality', 'safety', 'basic_needs',
                      'academic_performance', 'teacher_student_relationship', 'social_support']
    
    existing_protective = [c for c in protective_cols if c in df_proc.columns]
    
    if len(existing_protective) > 0:
        print_header("Reverse Coding Protective Factors", level=2)
        scaler = MinMaxScaler(feature_range=(0, 1))
        normalized = scaler.fit_transform(df_proc[existing_protective])
        
        for i, col in enumerate(existing_protective):
            new_col = f"{col}_INV"
            df_proc[new_col] = 1 - normalized[:, i]
            print(f"   {col} → {new_col}")
        
        df_proc = df_proc.drop(columns=existing_protective)
    
    print_header("Normalizing Features", level=2)
    feature_cols = [c for c in df_proc.columns if c != target_col]
    scaler_all = MinMaxScaler(feature_range=(0, 1))
    df_proc[feature_cols] = scaler_all.fit_transform(df_proc[feature_cols])
    
    print(f"   Final features: {len(feature_cols)}")
    
    return df_proc

def engineer_d2(df2):
    print_header("PHASE 3: FEATURE ENGINEERING (D2)")
    
    df_proc = df2.copy()
    target_col = df_proc.columns[-1]
    
    print_header("Encoding Target", level=2)
    le = LabelEncoder()
    df_proc['Stress_Type_Encoded'] = le.fit_transform(df_proc[target_col])
    stress_map = dict(zip(le.classes_, range(len(le.classes_))))
    print(f"   Mapping: {stress_map}")
    
    df_proc = df_proc.drop(columns=[target_col])
    
    print_header("Normalizing Features", level=2)
    numeric_cols = df_proc.select_dtypes(include=[np.number]).columns
    numeric_cols = [c for c in numeric_cols if c != 'Stress_Type_Encoded']
    
    scaler = MinMaxScaler(feature_range=(0, 1))
    df_proc[numeric_cols] = scaler.fit_transform(df_proc[numeric_cols])
    
    print(f"   Final features: {len(numeric_cols)}")
    
    return df_proc, stress_map

def prepare_datasets(df1, df2):
    print_header("PHASE 4: DATASET PREPARATION")
    
    print_header("Dataset 1", level=2)
    target_col_d1 = [c for c in df1.columns if 'stress' in c.lower() or c == df1.columns[-1]][0]
    X1 = df1.drop(target_col_d1, axis=1)
    y1 = df1[target_col_d1]
    
    print(f"   Features: {X1.shape[1]}")
    print(f"   Classes: {y1.value_counts().sort_index().to_dict()}")
    
    scaler1 = RobustScaler()
    X1_scaled = pd.DataFrame(scaler1.fit_transform(X1), columns=X1.columns, index=X1.index)
    
    X1_train, X1_test, y1_train, y1_test = train_test_split(
        X1_scaled, y1, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y1
    )
    
    print(f"   Train: {X1_train.shape[0]}, Test: {X1_test.shape[0]}")
    
    print_header("Dataset 2", level=2)
    X2 = df2.drop('Stress_Type_Encoded', axis=1)
    y2 = df2['Stress_Type_Encoded']
    
    print(f"   Features: {X2.shape[1]}")
    print(f"   Classes (before SMOTE): {y2.value_counts().sort_index().to_dict()}")
    
    scaler2 = RobustScaler()
    X2_scaled = pd.DataFrame(scaler2.fit_transform(X2), columns=X2.columns, index=X2.index)
    
    X2_train, X2_test, y2_train, y2_test = train_test_split(
        X2_scaled, y2, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y2
    )
    
    class_counts = y2_train.value_counts()
    imbalance = class_counts.max() / class_counts.min()
    
    if imbalance > 3:
        print(f"\n   Applying SMOTE (imbalance: {imbalance:.2f}:1)")
        smote = SMOTE(random_state=RANDOM_STATE, k_neighbors=3)
        X2_train, y2_train = smote.fit_resample(X2_train, y2_train)
        print(f"   Classes (after SMOTE): {pd.Series(y2_train).value_counts().sort_index().to_dict()}")
    
    print(f"   Train: {X2_train.shape[0]}, Test: {X2_test.shape[0]}")
    
    return X1_train, X1_test, y1_train, y1_test, X2_train, X2_test, y2_train, y2_test, scaler1, scaler2

def train_models(X_train, y_train, name):
    print_header(f"Training {name}", level=2)
    
    print("\n   [1/2] Logistic Regression...")
    logreg_params = {
        'C': [0.01, 0.1, 1, 10],
        'solver': ['lbfgs', 'saga'],
        'max_iter': [1000]
    }
    
    logreg_grid = GridSearchCV(
        LogisticRegression(random_state=RANDOM_STATE),
        logreg_params,
        cv=CV_FOLDS,
        scoring='f1_macro',
        n_jobs=-1
    )
    logreg_grid.fit(X_train, y_train)
    print(f"      Best params: {logreg_grid.best_params_}")
    print(f"      CV F1: {logreg_grid.best_score_:.4f}")
    
    print("\n   [2/2] Random Forest...")
    rf_params = {
        'n_estimators': [50, 100, 200],
        'max_depth': [5, 10, 15],
        'min_samples_split': [2, 5],
        'class_weight': ['balanced']
    }
    
    rf_grid = GridSearchCV(
        RandomForestClassifier(random_state=RANDOM_STATE),
        rf_params,
        cv=CV_FOLDS,
        scoring='f1_macro',
        n_jobs=-1
    )
    rf_grid.fit(X_train, y_train)
    print(f"      Best params: {rf_grid.best_params_}")
    print(f"      CV F1: {rf_grid.best_score_:.4f}")
    
    return logreg_grid.best_estimator_, rf_grid.best_estimator_

def evaluate_model(model, X_test, y_test, model_name, dataset_name):
    print_header(f"{model_name} - {dataset_name}", level=2)
    
    y_pred = model.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='macro', zero_division=0)
    rec = recall_score(y_test, y_pred, average='macro', zero_division=0)
    f1_m = f1_score(y_test, y_pred, average='macro', zero_division=0)
    f1_w = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    mcc = matthews_corrcoef(y_test, y_pred)
    
    print(f"\n   Accuracy:     {acc:.4f}")
    print(f"   Precision:    {prec:.4f}")
    print(f"   Recall:       {rec:.4f}")
    print(f"   F1-Macro:     {f1_m:.4f}")
    print(f"   F1-Weighted:  {f1_w:.4f}")
    print(f"   MCC:          {mcc:.4f}")
    
    return y_pred, {'accuracy': acc, 'f1_macro': f1_m, 'mcc': mcc}

def analyze_importance(model, X_train, X_test, y_test, name):
    print_header(f"Feature Importance - {name}", level=2)
    
    if hasattr(model, 'feature_importances_'):
        gini = pd.Series(model.feature_importances_, index=X_train.columns).sort_values(ascending=False)
        
        print("\n   Computing permutation importance...")
        perm = permutation_importance(model, X_test, y_test, n_repeats=30, random_state=RANDOM_STATE, n_jobs=-1)
        perm_df = pd.DataFrame({
            'mean': perm.importances_mean,
            'std': perm.importances_std
        }, index=X_train.columns).sort_values('mean', ascending=False)
        
        print("\n   Top 10 (Gini):")
        for i, (feat, imp) in enumerate(gini.head(10).items(), 1):
            print(f"      {i:2d}. {feat:30s} {imp:.4f}")
        
        print("\n   Top 10 (Permutation):")
        for i, (feat, row) in enumerate(perm_df.head(10).iterrows(), 1):
            print(f"      {i:2d}. {feat:30s} {row['mean']:.4f} ± {row['std']:.4f}")
        
        return gini, perm_df
    else:
        coef = pd.Series(np.abs(model.coef_).mean(axis=0), index=X_train.columns).sort_values(ascending=False)
        
        print("\n   Top 10 (Coefficient):")
        for i, (feat, imp) in enumerate(coef.head(10).items(), 1):
            print(f"      {i:2d}. {feat:30s} {imp:.4f}")
        
        return coef, None

def visualize(gini_d1, perm_d1, y1_test, y1_pred, gini_d2, perm_d2, y2_test, y2_pred, met_d1, met_d2):
    print_header("PHASE 8: VISUALIZATIONS")
    
    sns.set_style("whitegrid")
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    top_gini = gini_d1.head(10)
    axes[0].barh(range(len(top_gini)), top_gini.values, color='steelblue')
    axes[0].set_yticks(range(len(top_gini)))
    axes[0].set_yticklabels(top_gini.index)
    axes[0].set_xlabel('Importance')
    axes[0].set_title('D1: Top 10 Features (Gini)', fontweight='bold')
    axes[0].invert_yaxis()
    
    if perm_d1 is not None:
        top_perm = perm_d1.head(10)
        axes[1].barh(range(len(top_perm)), top_perm['mean'].values, xerr=top_perm['std'].values, color='coral', capsize=4)
        axes[1].set_yticks(range(len(top_perm)))
        axes[1].set_yticklabels(top_perm.index)
        axes[1].set_xlabel('Importance')
        axes[1].set_title('D1: Top 10 Features (Permutation)', fontweight='bold')
        axes[1].invert_yaxis()
    
    plt.tight_layout()
    plt.savefig('D1_Feature_Importance.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    top_gini2 = gini_d2.head(10)
    axes[0].barh(range(len(top_gini2)), top_gini2.values, color='mediumseagreen')
    axes[0].set_yticks(range(len(top_gini2)))
    axes[0].set_yticklabels(top_gini2.index)
    axes[0].set_xlabel('Importance')
    axes[0].set_title('D2: Top 10 Features (Gini)', fontweight='bold')
    axes[0].invert_yaxis()
    
    if perm_d2 is not None:
        top_perm2 = perm_d2.head(10)
        axes[1].barh(range(len(top_perm2)), top_perm2['mean'].values, xerr=top_perm2['std'].values, color='mediumpurple', capsize=4)
        axes[1].set_yticks(range(len(top_perm2)))
        axes[1].set_yticklabels(top_perm2.index)
        axes[1].set_xlabel('Importance')
        axes[1].set_title('D2: Top 10 Features (Permutation)', fontweight='bold')
        axes[1].invert_yaxis()
    
    plt.tight_layout()
    plt.savefig('D2_Feature_Importance.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    cm1 = confusion_matrix(y1_test, y1_pred)
    sns.heatmap(cm1, annot=True, fmt='d', cmap='Blues', square=True, ax=axes[0], linewidths=1, linecolor='black')
    axes[0].set_xlabel('Predicted')
    axes[0].set_ylabel('True')
    axes[0].set_title('D1: Confusion Matrix', fontweight='bold')
    
    cm2 = confusion_matrix(y2_test, y2_pred)
    sns.heatmap(cm2, annot=True, fmt='d', cmap='Greens', square=True, ax=axes[1], linewidths=1, linecolor='black')
    axes[1].set_xlabel('Predicted')
    axes[1].set_ylabel('True')
    axes[1].set_title('D2: Confusion Matrix', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('Confusion_Matrices.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    metrics = {
        'D1': [met_d1['accuracy'], met_d1['f1_macro'], met_d1['mcc']],
        'D2': [met_d2['accuracy'], met_d2['f1_macro'], met_d2['mcc']]
    }
    
    x = np.arange(3)
    w = 0.35
    
    ax.bar(x - w/2, metrics['D1'], w, label='Dataset 1', color='steelblue')
    ax.bar(x + w/2, metrics['D2'], w, label='Dataset 2', color='mediumseagreen')
    
    ax.set_ylabel('Score')
    ax.set_title('Model Performance Comparison', fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(['Accuracy', 'F1-Macro', 'MCC'])
    ax.legend()
    ax.set_ylim(0, 1.1)
    ax.grid(axis='y', alpha=0.3)
    
    for i, (v1, v2) in enumerate(zip(metrics['D1'], metrics['D2'])):
        ax.text(i - w/2, v1 + 0.02, f'{v1:.3f}', ha='center', fontsize=9)
        ax.text(i + w/2, v2 + 0.02, f'{v2:.3f}', ha='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('Performance_Comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("   [OK] Visualizations saved")

def main():
    print("\n" + "█"*80)
    print("  STRESS CLASSIFICATION PIPELINE")
    print("█"*80)
    
    df1, df2 = load_datasets()
    df2_clean = quality_control_d2(df2)
    df1_proc = engineer_d1(df1)
    df2_proc, stress_map = engineer_d2(df2_clean)
    
    X1_tr, X1_te, y1_tr, y1_te, X2_tr, X2_te, y2_tr, y2_te, sc1, sc2 = prepare_datasets(df1_proc, df2_proc)
    
    print_header("PHASE 5: MODEL TRAINING")
    
    print("\n" + "="*80)
    print("  DATASET 1")
    print("="*80)
    logreg_d1, rf_d1 = train_models(X1_tr, y1_tr, "D1")
    
    print("\n" + "="*80)
    print("  DATASET 2")
    print("="*80)
    logreg_d2, rf_d2 = train_models(X2_tr, y2_tr, "D2")
    
    print_header("PHASE 6: EVALUATION")
    
    print("\n" + "="*80)
    print("  DATASET 1")
    print("="*80)
    
    y_pred_lr1, met_lr1 = evaluate_model(logreg_d1, X1_te, y1_te, "Logistic Regression", "D1")
    y_pred_rf1, met_rf1 = evaluate_model(rf_d1, X1_te, y1_te, "Random Forest", "D1")
    
    print("\n" + "="*80)
    print("  DATASET 2")
    print("="*80)
    
    y_pred_lr2, met_lr2 = evaluate_model(logreg_d2, X2_te, y2_te, "Logistic Regression", "D2")
    y_pred_rf2, met_rf2 = evaluate_model(rf_d2, X2_te, y2_te, "Random Forest", "D2")
    
    print_header("PHASE 7: FEATURE IMPORTANCE")
    
    print("\n" + "="*80)
    print("  DATASET 1 - RANDOM FOREST")
    print("="*80)
    gini_d1, perm_d1 = analyze_importance(rf_d1, X1_tr, X1_te, y1_te, "D1")
    
    print("\n" + "="*80)
    print("  DATASET 2 - RANDOM FOREST")
    print("="*80)
    gini_d2, perm_d2 = analyze_importance(rf_d2, X2_tr, X2_te, y2_te, "D2")
    
    try:
        visualize(gini_d1, perm_d1, y1_te, y_pred_rf1, gini_d2, perm_d2, y2_te, y_pred_rf2, met_rf1, met_rf2)
    except Exception as e:
        print(f"   Visualization error: {e}")
    
    os.makedirs("trained_models", exist_ok=True)
    
    joblib.dump(rf_d1, "trained_models/rf_d1.pkl")
    joblib.dump(rf_d2, "trained_models/rf_d2.pkl")
    joblib.dump(sc1, "trained_models/scaler_d1.pkl")
    joblib.dump(sc2, "trained_models/scaler_d2.pkl")
    joblib.dump(X1_te.columns.tolist(), "trained_models/features_d1.pkl")
    joblib.dump(X2_te.columns.tolist(), "trained_models/features_d2.pkl")
    joblib.dump((X1_te, y1_te), "trained_models/test_d1.pkl")
    joblib.dump((X2_te, y2_te), "trained_models/test_d2.pkl")
    joblib.dump({'d1': met_rf1, 'd2': met_rf2}, "trained_models/metrics.pkl")
    
    print_header("COMPLETE")
    
    print("\n┌" + "─"*78 + "┐")
    print("│" + " "*30 + "FINAL SUMMARY" + " "*35 + "│")
    print("├" + "─"*78 + "┤")
    print("│  Dataset 1 - Random Forest" + " "*50 + "│")
    print(f"│    • Accuracy:  {met_rf1['accuracy']:.4f}" + " "*56 + "│")
    print(f"│    • F1-Macro:  {met_rf1['f1_macro']:.4f}" + " "*56 + "│")
    print(f"│    • MCC:       {met_rf1['mcc']:.4f}" + " "*56 + "│")
    print("│" + " "*78 + "│")
    print("│  Dataset 2 - Random Forest" + " "*50 + "│")
    print(f"│    • Accuracy:  {met_rf2['accuracy']:.4f}" + " "*56 + "│")
    print(f"│    • F1-Macro:  {met_rf2['f1_macro']:.4f}" + " "*56 + "│")
    print(f"│    • MCC:       {met_rf2['mcc']:.4f}" + " "*56 + "│")
    print("└" + "─"*78 + "┘\n")
    
    print("[OK] All models saved to trained_models/")
    
    return {
        'models': {'d1_lr': logreg_d1, 'd1_rf': rf_d1, 'd2_lr': logreg_d2, 'd2_rf': rf_d2},
        'test_data': {'d1': (X1_te, y1_te), 'd2': (X2_te, y2_te)},
        'importance': {'d1_gini': gini_d1, 'd1_perm': perm_d1, 'd2_gini': gini_d2, 'd2_perm': perm_d2},
        'metrics': {'d1_rf': met_rf1, 'd2_rf': met_rf2},
        'scalers': {'d1': sc1, 'd2': sc2}
    }

if __name__ == "__main__":
    results = main()