
from __future__ import annotations
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

D1_FEATURES = [
    "anxiety_level","self_esteem","mental_health_history","depression","headache",
    "blood_pressure","sleep_quality","breathing_problem","noise_level",
    "living_conditions","safety","basic_needs","academic_performance","study_load",
    "teacher_student_relationship","future_career_concerns","social_support",
    "peer_pressure","extracurricular_activities","bullying",
]
D1_PROTECTIVE = [
    "self_esteem","sleep_quality","safety","basic_needs",
    "academic_performance","teacher_student_relationship","social_support",
]
D1_OUTPUT_FEATURES = [c for c in D1_FEATURES if c not in D1_PROTECTIVE] + [f"{c}_INV" for c in D1_PROTECTIVE]
D2_FEATURES = [
    "Gender","Age","Have you recently experienced stress in your life?",
    "Have you noticed a rapid heartbeat or palpitations?",
    "Have you been dealing with anxiety or tension recently?",
    "Do you face any sleep problems or difficulties falling asleep?",
    "Have you been dealing with anxiety or tension recently?.1",
    "Have you been getting headaches more often than usual?","Do you get irritated easily?",
    "Do you have trouble concentrating on your academic tasks?","Have you been feeling sadness or low mood?",
    "Have you been experiencing any illness or health issues?","Do you often feel lonely or isolated?",
    "Do you feel overwhelmed with your academic workload?",
    "Are you in competition with your peers, and does it affect you?",
    "Do you find that your relationship often causes you stress?",
    "Are you facing any difficulties with your professors or instructors?",
    "Is your working environment unpleasant or stressful?",
    "Do you struggle to find time for relaxation and leisure activities?",
    "Is your hostel or home environment causing you difficulties?",
    "Do you lack confidence in your academic performance?",
    "Do you lack confidence in your choice of academic subjects?",
    "Academic and extracurricular activities conflicting for you?",
    "Do you attend classes regularly?","Have you gained/lost weight?",
]

class D1FeatureBuilder(BaseEstimator, TransformerMixin):
    RANGES = {
        "self_esteem":(0,30),"sleep_quality":(0,10),"safety":(0,10),
        "basic_needs":(0,10),"academic_performance":(0,5),
        "teacher_student_relationship":(0,10),"social_support":(0,12),
    }
    def fit(self, X, y=None):
        X = pd.DataFrame(X)
        missing = [c for c in D1_FEATURES if c not in X.columns]
        if missing: raise ValueError(f"Missing D1 features: {missing}")
        return self
    def transform(self, X):
        X = pd.DataFrame(X).copy()
        missing = [c for c in D1_FEATURES if c not in X.columns]
        if missing: raise ValueError(f"Missing D1 features: {missing}")
        out = X[D1_FEATURES].copy()
        for col in D1_PROTECTIVE:
            lo, hi = self.RANGES[col]
            out[f"{col}_INV"] = (hi - out[col]) / (hi - lo)
        return out.drop(columns=D1_PROTECTIVE)[D1_OUTPUT_FEATURES]
    def get_feature_names_out(self, input_features=None):
        return D1_OUTPUT_FEATURES
