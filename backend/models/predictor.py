import joblib
import numpy as np
import pandas as pd

from config import Config


class StressPredictor:
    """Loads the two fitted end-to-end pipelines (reverse-coding + scaling +
    model, all one object per dataset) and the training metadata. Because
    preprocessing lives INSIDE the saved pipeline, this class only ever has
    to hand it a DataFrame of raw questionnaire values using the exact
    column names in Config.D1_FEATURES / Config.D2_FEATURES — the same
    names the frontend already sends. There is no separate scaler/feature
    file to keep in sync by hand.
    """

    def __init__(self):
        self.pipeline_d1 = None
        self.pipeline_d2 = None
        self.metadata = None
        self.load_models()

    def load_models(self):
        try:
            self.pipeline_d1 = joblib.load(Config.PIPELINE_D1_PATH)
            self.pipeline_d2 = joblib.load(Config.PIPELINE_D2_PATH)
            self.metadata = joblib.load(Config.METADATA_PATH)
            print("All models loaded successfully")
        except Exception as e:
            print(f"Error loading models: {e}")
            raise

    def predict_stress_level(self, input_data):
        try:
            df = pd.DataFrame([input_data])[Config.D1_FEATURES]

            prediction = int(self.pipeline_d1.predict(df)[0])
            probabilities = self.pipeline_d1.predict_proba(df)[0]

            result = {
                'prediction': prediction,
                'stress_level': Config.STRESS_LEVEL_LABELS[prediction],
                'confidence': {
                    'low': round(float(probabilities[0]) * 100, 2),
                    'moderate': round(float(probabilities[1]) * 100, 2),
                    'high': round(float(probabilities[2]) * 100, 2)
                },
                'recommendation': self._get_recommendation(prediction),
                'model_accuracy': round(self.metadata['d1']['metrics']['accuracy'] * 100, 2),
                'model_f1_macro': round(self.metadata['d1']['metrics']['f1_macro'] * 100, 2),
            }
            return result
        except Exception as e:
            raise Exception(f"Prediction error: {str(e)}")

    def predict_stress_type(self, input_data):
        try:
            df = pd.DataFrame([input_data])[Config.D2_FEATURES]

            prediction = int(self.pipeline_d2.predict(df)[0])
            probabilities = self.pipeline_d2.predict_proba(df)[0]
            label_map = self.metadata['d2']['class_labels']  # {0: 'Distress', ...} from training-time LabelEncoder

            result = {
                'prediction': prediction,
                'stress_type': label_map[prediction],
                'confidence': round(float(max(probabilities)) * 100, 2),
                'probabilities': {
                    label_map[i]: round(float(p) * 100, 2) for i, p in enumerate(probabilities)
                },
                'recommendation': self._get_type_recommendation(label_map[prediction]),
                'model_accuracy': round(self.metadata['d2']['metrics']['accuracy'] * 100, 2),
                'model_f1_macro': round(self.metadata['d2']['metrics']['f1_macro'] * 100, 2),
            }
            return result
        except Exception as e:
            raise Exception(f"Prediction error: {str(e)}")

    def _get_recommendation(self, prediction):
        if prediction == 0:
            return "Your stress level is low. Maintain healthy habits and continue your current coping strategies."
        elif prediction == 1:
            return "Your stress level is moderate. Consider stress management techniques like exercise, meditation, or talking to someone."
        else:
            return "Your stress level is high. It's important to seek support from a counselor or mental health professional."

    def _get_type_recommendation(self, label):
        if label.startswith('Distress'):
            return "You're experiencing distress (negative stress). Consider seeking support and practicing stress-reduction techniques."
        elif label.startswith('Eustress'):
            return "You're experiencing eustress (positive stress). Channel this energy productively while maintaining balance."
        else:
            return "You're currently experiencing minimal stress. Continue maintaining your well-being practices."

    def get_model_info(self):
        return {
            'dataset_1': {
                'name': 'Stress Level Predictor',
                'accuracy': round(self.metadata['d1']['metrics']['accuracy'] * 100, 2),
                'f1_score': round(self.metadata['d1']['metrics']['f1_macro'] * 100, 2),
                'classes': list(Config.STRESS_LEVEL_LABELS.values()),
                'trained_at': self.metadata['trained_at'],
            },
            'dataset_2': {
                'name': 'Stress Type Predictor',
                'accuracy': round(self.metadata['d2']['metrics']['accuracy'] * 100, 2),
                'f1_score': round(self.metadata['d2']['metrics']['f1_macro'] * 100, 2),
                'classes': list(self.metadata['d2']['class_labels'].values()),
                'trained_at': self.metadata['trained_at'],
            }
        }
