"""Shared, importable preprocessing pieces used inside the saved pipelines.

This has to live in its own module (not inside train.py) so that joblib can
always resolve the class by its import path when the Flask app unpickles the
trained pipeline — pickling a class/function defined in __main__ or in a
script that isn't on the importer's path is a classic footgun.
"""
from config import Config

D1_PROTECTIVE_FIELDS = [
    "self_esteem", "sleep_quality", "safety", "basic_needs",
    "academic_performance", "teacher_student_relationship", "social_support",
]


class D1ReverseCoder:
    """Deterministic reverse-coding transform for D1 protective factors.

    inv = (max - value) / (max - min), using the fixed questionnaire ranges
    in Config.FIELD_RANGES. No .fit() step, no dependency on the dataset —
    the same code runs identically during training and from the live API.
    """

    def __init__(self, fields):
        self.fields = fields

    def __call__(self, X):
        X = X.copy()
        for field in self.fields:
            lo, hi = Config.FIELD_RANGES[field]
            X[field] = (hi - X[field]) / (hi - lo)
        return X
