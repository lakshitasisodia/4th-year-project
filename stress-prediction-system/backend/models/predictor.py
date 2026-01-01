import joblib
import pandas as pd
import numpy as np
from config import Config

class StressPredictor:
    
    def __init__(self):
        self.model_d1 = None
        self.model_d2 = None
        self.scaler_d1 = None
        self.scaler_d2 = None
        self.features_d1 = None
        self.features_d2 = None
        self.metrics = None
        self.load_models()
    
    def load_models(self):
        try:
            self.model_d1 = joblib.load(Config.MODEL_D1_PATH)
            self.model_d2 = joblib.load(Config.MODEL_D2_PATH)
            self.scaler_d1 = joblib.load(Config.SCALER_D1_PATH)
            self.scaler_d2 = joblib.load(Config.SCALER_D2_PATH)
            self.features_d1 = joblib.load(Config.FEATURES_D1_PATH)
            self.features_d2 = joblib.load(Config.FEATURES_D2_PATH)
            self.metrics = joblib.load(Config.METRICS_PATH)
            print("All models loaded successfully")
        except Exception as e:
            print(f"Error loading models: {e}")
            raise
    
    def predict_stress_level(self, input_data):
        try:
            df = pd.DataFrame([input_data])
            
            df = df[self.features_d1]
            
            df_scaled = self.scaler_d1.transform(df)
            
            prediction = self.model_d1.predict(df_scaled)[0]
            probabilities = self.model_d1.predict_proba(df_scaled)[0]
            
            result = {
                'prediction': int(prediction),
                'stress_level': Config.STRESS_LEVEL_LABELS[prediction],
                'confidence': {
                    'low': round(float(probabilities[0]) * 100, 2),
                    'moderate': round(float(probabilities[1]) * 100, 2),
                    'high': round(float(probabilities[2]) * 100, 2)
                },
                'recommendation': self._get_recommendation(prediction, probabilities),
                'model_accuracy': round(self.metrics['d1']['accuracy'] * 100, 2)
            }
            
            return result
        
        except Exception as e:
            raise Exception(f"Prediction error: {str(e)}")
    
    def predict_stress_type(self, input_data):
        try:
            df = pd.DataFrame([input_data])
            
            df = df[self.features_d2]
            
            df_scaled = self.scaler_d2.transform(df)
            
            prediction = self.model_d2.predict(df_scaled)[0]
            probabilities = self.model_d2.predict_proba(df_scaled)[0]
            
            result = {
                'prediction': int(prediction),
                'stress_type': Config.STRESS_TYPE_LABELS[prediction],
                'confidence': round(float(max(probabilities)) * 100, 2),
                'probabilities': {
                    'distress': round(float(probabilities[0]) * 100, 2),
                    'eustress': round(float(probabilities[1]) * 100, 2),
                    'no_stress': round(float(probabilities[2]) * 100, 2)
                },
                'recommendation': self._get_type_recommendation(prediction),
                'model_accuracy': round(self.metrics['d2']['accuracy'] * 100, 2)
            }
            
            return result
        
        except Exception as e:
            raise Exception(f"Prediction error: {str(e)}")
    
    def _get_recommendation(self, prediction, probabilities):
        if prediction == 0:
            return "Your stress level is low. Maintain healthy habits and continue your current coping strategies."
        elif prediction == 1:
            return "Your stress level is moderate. Consider stress management techniques like exercise, meditation, or talking to someone."
        else:
            return "Your stress level is high. It's important to seek support from a counselor or mental health professional."
    
    def _get_type_recommendation(self, prediction):
        if prediction == 0:
            return "You're experiencing distress (negative stress). Consider seeking support and practicing stress-reduction techniques."
        elif prediction == 1:
            return "You're experiencing eustress (positive stress). Channel this energy productively while maintaining balance."
        else:
            return "You're currently experiencing minimal stress. Continue maintaining your well-being practices."
    
    def get_model_info(self):
        return {
            'dataset_1': {
                'name': 'Stress Level Predictor',
                'accuracy': round(self.metrics['d1']['accuracy'] * 100, 2),
                'f1_score': round(self.metrics['d1']['f1_macro'] * 100, 2),
                'classes': list(Config.STRESS_LEVEL_LABELS.values())
            },
            'dataset_2': {
                'name': 'Stress Type Predictor',
                'accuracy': round(self.metrics['d2']['accuracy'] * 100, 2),
                'f1_score': round(self.metrics['d2']['f1_macro'] * 100, 2),
                'classes': list(Config.STRESS_TYPE_LABELS.values())
            }
        }