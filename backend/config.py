import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / 'trained_models'


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    PIPELINE_D1_PATH = MODELS_DIR / 'pipeline_d1.pkl'
    PIPELINE_D2_PATH = MODELS_DIR / 'pipeline_d2.pkl'
    METADATA_PATH = MODELS_DIR / 'metadata.pkl'

    D1_FEATURES = [
        'anxiety_level', 'self_esteem', 'mental_health_history', 'depression',
        'headache', 'blood_pressure', 'sleep_quality', 'breathing_problem',
        'noise_level', 'living_conditions', 'safety', 'basic_needs',
        'academic_performance', 'study_load', 'teacher_student_relationship',
        'future_career_concerns', 'social_support', 'peer_pressure',
        'extracurricular_activities', 'bullying'
    ]

    D2_FEATURES = [
        'Gender', 'Age', 'Have you recently experienced stress in your life?',
        'Have you noticed a rapid heartbeat or palpitations?',
        'Have you been dealing with anxiety or tension recently?',
        'Do you face any sleep problems or difficulties falling asleep?',
        'Have you been dealing with anxiety or tension recently?.1',
        'Have you been getting headaches more often than usual?',
        'Do you get irritated easily?',
        'Do you have trouble concentrating on your academic tasks?',
        'Have you been feeling sadness or low mood?',
        'Have you been experiencing any illness or health issues?',
        'Do you often feel lonely or isolated?',
        'Do you feel overwhelmed with your academic workload?',
        'Are you in competition with your peers, and does it affect you?',
        'Do you find that your relationship often causes you stress?',
        'Are you facing any difficulties with your professors or instructors?',
        'Is your working environment unpleasant or stressful?',
        'Do you struggle to find time for relaxation and leisure activities?',
        'Is your hostel or home environment causing you difficulties?',
        'Do you lack confidence in your academic performance?',
        'Do you lack confidence in your choice of academic subjects?',
        'Academic and extracurricular activities conflicting for you?',
        'Do you attend classes regularly?',
        'Have you gained/lost weight?'
    ]

    STRESS_LEVEL_LABELS = {
        0: 'Low Stress',
        1: 'Moderate Stress',
        2: 'High Stress'
    }

    STRESS_TYPE_LABELS = {
        0: 'Distress',
        1: 'Eustress',
        2: 'No Stress'
    }

    # Verified against the complete StressLevelDataset.csv (1100 rows, 0 missing,
    # 0 duplicates). 12 of these 20 ranges were wrong in the original config
    # (e.g. sleep_quality was declared 0-10 but the questionnaire — and every
    # row in the data — only ever uses 0-5). Wrong ranges meant the frontend
    # and backend validators both accepted out-of-distribution values the
    # model was never trained on.
    FIELD_RANGES = {
        'anxiety_level': (0, 21),
        'self_esteem': (0, 30),
        'mental_health_history': (0, 1),
        'depression': (0, 27),
        'headache': (0, 5),
        'blood_pressure': (1, 3),
        'sleep_quality': (0, 5),
        'breathing_problem': (0, 5),
        'noise_level': (0, 5),
        'living_conditions': (0, 5),
        'safety': (0, 5),
        'basic_needs': (0, 5),
        'academic_performance': (0, 5),
        'study_load': (0, 5),
        'teacher_student_relationship': (0, 5),
        'future_career_concerns': (0, 5),
        'social_support': (0, 3),
        'peer_pressure': (0, 5),
        'extracurricular_activities': (0, 5),
        'bullying': (0, 5)
    }
