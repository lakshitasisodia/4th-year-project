"""
tests/test_prediction_behavior.py

Automated tests for the Group 3 "same prediction" investigation, run against
pipelines trained on the complete, real datasets.

Run: pytest tests/test_prediction_behavior.py -v
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from models.predictor import StressPredictor
from utils.validator import InputValidator
from config import Config


@pytest.fixture(scope="module")
def predictor():
    return StressPredictor()


@pytest.fixture(scope="module")
def validator():
    return InputValidator()


LOW_STRESS_D1 = {
    'anxiety_level': 2, 'self_esteem': 28, 'mental_health_history': 0, 'depression': 2,
    'headache': 0, 'blood_pressure': 1, 'sleep_quality': 5, 'breathing_problem': 0,
    'noise_level': 0, 'living_conditions': 4, 'safety': 5, 'basic_needs': 5,
    'academic_performance': 5, 'study_load': 0, 'teacher_student_relationship': 5,
    'future_career_concerns': 0, 'social_support': 3, 'peer_pressure': 0,
    'extracurricular_activities': 0, 'bullying': 0,
}

HIGH_STRESS_D1 = {
    'anxiety_level': 20, 'self_esteem': 1, 'mental_health_history': 1, 'depression': 25,
    'headache': 5, 'blood_pressure': 3, 'sleep_quality': 0, 'breathing_problem': 5,
    'noise_level': 5, 'living_conditions': 0, 'safety': 0, 'basic_needs': 0,
    'academic_performance': 0, 'study_load': 5, 'teacher_student_relationship': 0,
    'future_career_concerns': 5, 'social_support': 0, 'peer_pressure': 5,
    'extracurricular_activities': 5, 'bullying': 5,
}


def d2_input(scale_value, gender=0, age=20):
    data = {f: scale_value for f in Config.D2_FEATURES if f not in ('Gender', 'Age')}
    data['Gender'] = gender
    data['Age'] = age
    return data


# ---------------------------------------------------------------------------
# 1. Identical input twice -> identical prediction (determinism)
# ---------------------------------------------------------------------------

def test_d1_identical_input_gives_identical_prediction(predictor):
    r1 = predictor.predict_stress_level(LOW_STRESS_D1)
    r2 = predictor.predict_stress_level(LOW_STRESS_D1)
    assert r1['prediction'] == r2['prediction']
    assert r1['confidence'] == r2['confidence']


def test_d2_identical_input_gives_identical_prediction(predictor):
    inp = d2_input(3)
    r1 = predictor.predict_stress_type(inp)
    r2 = predictor.predict_stress_type(inp)
    assert r1['prediction'] == r2['prediction']
    assert r1['probabilities'] == r2['probabilities']


# ---------------------------------------------------------------------------
# 2. Clearly low vs high stress inputs -> distinguishable outputs
# ---------------------------------------------------------------------------

def test_d1_low_stress_input_predicts_low(predictor):
    r = predictor.predict_stress_level(LOW_STRESS_D1)
    assert r['stress_level'] == 'Low Stress'
    assert r['confidence']['low'] > r['confidence']['high']


def test_d1_high_stress_input_predicts_high(predictor):
    r = predictor.predict_stress_level(HIGH_STRESS_D1)
    assert r['stress_level'] == 'High Stress'
    assert r['confidence']['high'] > r['confidence']['low']


def test_d1_low_and_high_inputs_produce_different_predictions(predictor):
    r_low = predictor.predict_stress_level(LOW_STRESS_D1)
    r_high = predictor.predict_stress_level(HIGH_STRESS_D1)
    assert r_low['prediction'] != r_high['prediction']


def test_d2_low_scale_vs_high_scale_differ(predictor):
    r_low = predictor.predict_stress_type(d2_input(1))
    r_high = predictor.predict_stress_type(d2_input(5))
    assert r_low['prediction'] != r_high['prediction'] or r_low['probabilities'] != r_high['probabilities']


# ---------------------------------------------------------------------------
# 3. Changing ONE influential feature changes the probability distribution
# ---------------------------------------------------------------------------

def test_d1_single_feature_change_moves_probabilities(predictor):
    baseline = dict(LOW_STRESS_D1)
    changed = dict(LOW_STRESS_D1)
    changed['anxiety_level'] = 20  # push one strongly influential feature to its max

    r_base = predictor.predict_stress_level(baseline)
    r_changed = predictor.predict_stress_level(changed)

    assert r_base['confidence'] != r_changed['confidence'], (
        "Changing anxiety_level alone did not move the probability distribution at all"
    )


# ---------------------------------------------------------------------------
# 4. Substantially changing MULTIPLE features changes the distribution
# ---------------------------------------------------------------------------

def test_d1_multi_feature_change_moves_probabilities_more(predictor):
    baseline = dict(LOW_STRESS_D1)
    single_change = dict(LOW_STRESS_D1)
    single_change['anxiety_level'] = 20

    r_base = predictor.predict_stress_level(baseline)
    r_single = predictor.predict_stress_level(single_change)
    r_full = predictor.predict_stress_level(HIGH_STRESS_D1)

    delta_single = abs(r_base['confidence']['high'] - r_single['confidence']['high'])
    delta_full = abs(r_base['confidence']['high'] - r_full['confidence']['high'])

    assert delta_full >= delta_single, (
        "Changing every feature moved 'high' confidence less than changing just one — "
        "suggests the model isn't responding proportionally to input magnitude"
    )


# ---------------------------------------------------------------------------
# 5. Malformed / missing / out-of-range input is rejected by validation
# ---------------------------------------------------------------------------

def test_d1_missing_field_rejected(validator):
    incomplete = dict(LOW_STRESS_D1)
    del incomplete['anxiety_level']
    is_valid, errors = validator.validate_d1_input(incomplete)
    assert not is_valid
    assert any('anxiety_level' in e for e in errors)


def test_d1_out_of_range_rejected(validator):
    bad = dict(LOW_STRESS_D1)
    bad['sleep_quality'] = 10  # valid under the OLD (wrong) range, invalid under the fixed one
    is_valid, errors = validator.validate_d1_input(bad)
    assert not is_valid
    assert any('sleep_quality' in e for e in errors)


def test_d1_wrong_type_rejected(validator):
    bad = dict(LOW_STRESS_D1)
    bad['anxiety_level'] = "high"  # malformed: string instead of number
    is_valid, errors = validator.validate_d1_input(bad)
    assert not is_valid


def test_d1_non_dict_input_rejected(validator):
    is_valid, errors = validator.validate_d1_input(["not", "a", "dict"])
    assert not is_valid


def test_d2_gender_out_of_range_rejected(validator):
    bad = d2_input(3)
    bad['Gender'] = 5
    is_valid, errors = validator.validate_d2_input(bad)
    assert not is_valid


def test_d2_age_out_of_range_rejected(validator):
    bad = d2_input(3, age=100)  # the exact bad value found in the raw dataset
    is_valid, errors = validator.validate_d2_input(bad)
    assert not is_valid


def test_d2_scale_value_out_of_range_rejected(validator):
    bad = d2_input(3)
    bad['Do you get irritated easily?'] = 9
    is_valid, errors = validator.validate_d2_input(bad)
    assert not is_valid


# ---------------------------------------------------------------------------
# 6. Output schema sanity: probabilities sum to ~1, class labels resolve
# ---------------------------------------------------------------------------

def test_d1_probabilities_sum_to_one(predictor):
    r = predictor.predict_stress_level(LOW_STRESS_D1)
    total = sum(r['confidence'].values())
    assert abs(total - 100.0) < 0.5  # confidences are already *100 and rounded


def test_d2_probabilities_sum_to_one(predictor):
    r = predictor.predict_stress_type(d2_input(3))
    total = sum(r['probabilities'].values())
    assert abs(total - 100.0) < 0.5


def test_d1_prediction_label_is_valid(predictor):
    r = predictor.predict_stress_level(LOW_STRESS_D1)
    assert r['stress_level'] in Config.STRESS_LEVEL_LABELS.values()


def test_d2_prediction_label_is_valid(predictor):
    r = predictor.predict_stress_type(d2_input(3))
    assert r['stress_type'] in predictor.metadata['d2']['class_labels'].values()
