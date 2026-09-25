
import json
from pathlib import Path
import joblib
import pandas as pd
from config import Config

class StressPredictor:
    def __init__(self):
        self.model_d1=None; self.model_d2=None; self.metadata_d1=None; self.metadata_d2=None
        self.load_models()
    def load_models(self):
        try:
            self.model_d1=joblib.load(Config.MODEL_D1_PIPELINE_PATH)
            self.model_d2=joblib.load(Config.MODEL_D2_PIPELINE_PATH)
            self.metadata_d1=self._metadata(Config.D1_METADATA_PATH)
            self.metadata_d2=self._metadata(Config.D2_METADATA_PATH)
        except Exception as e:
            raise RuntimeError("Rebuilt ML pipelines are missing. Run train_pipeline.py first.") from e
    @staticmethod
    def _metadata(path):
        return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def _predict(model,data,labels):
        X=pd.DataFrame([data]); pred=int(model.predict(X)[0]); probs=model.predict_proba(X)[0]
        pmap={labels[int(c)]:round(float(p)*100,2) for c,p in zip(model.classes_,probs)}
        return pred,pmap
    def predict_stress_level(self,data):
        pred,p=self._predict(self.model_d1,data,Config.STRESS_LEVEL_LABELS)
        return {"prediction":pred,"stress_level":Config.STRESS_LEVEL_LABELS[pred],
                "confidence":{"low":p["Low Stress"],"moderate":p["Moderate Stress"],"high":p["High Stress"]},
                "recommendation":self._get_recommendation(pred),
                "model_accuracy":round(self.metadata_d1["metrics"]["accuracy"]*100,2),
                "model_f1_macro":round(self.metadata_d1["metrics"]["f1_macro"]*100,2)}
    def predict_stress_type(self,data):
        pred,p=self._predict(self.model_d2,data,Config.STRESS_TYPE_LABELS)
        return {"prediction":pred,"stress_type":Config.STRESS_TYPE_LABELS[pred],
                "confidence":round(max(p.values()),2),
                "probabilities":{"distress":p["Distress"],"eustress":p["Eustress"],"no_stress":p["No Stress"]},
                "recommendation":self._get_type_recommendation(pred),
                "model_accuracy":round(self.metadata_d2["metrics"]["accuracy"]*100,2),
                "model_f1_macro":round(self.metadata_d2["metrics"]["f1_macro"]*100,2)}
    @staticmethod
    def _get_recommendation(pred):
        return {0:"Your stress level is low. Maintain healthy habits and continue your current coping strategies.",
                1:"Your stress level is moderate. Consider stress-management techniques such as exercise, relaxation, or talking to someone you trust.",
                2:"Your stress level is high. Consider seeking support from a qualified counselor or mental-health professional."}[pred]
    @staticmethod
    def _get_type_recommendation(pred):
        return {0:"The model classified the response pattern as distress. Consider stress-reduction strategies and, if needed, professional support.",
                1:"The model classified the response pattern as eustress. Maintain balance and monitor whether the pressure remains manageable.",
                2:"The model classified the response pattern as no stress. Continue maintaining healthy well-being practices."}[pred]
    def get_model_info(self):
        return {"dataset_1":{"name":"Stress Level Predictor","accuracy":round(self.metadata_d1["metrics"]["accuracy"]*100,2),
                             "f1_score":round(self.metadata_d1["metrics"]["f1_macro"]*100,2),
                             "classes":list(Config.STRESS_LEVEL_LABELS.values()),"selected_algorithm":self.metadata_d1["selected_algorithm"]},
                "dataset_2":{"name":"Stress Type Predictor","accuracy":round(self.metadata_d2["metrics"]["accuracy"]*100,2),
                             "f1_score":round(self.metadata_d2["metrics"]["f1_macro"]*100,2),
                             "classes":list(Config.STRESS_TYPE_LABELS.values()),"selected_algorithm":self.metadata_d2["selected_algorithm"]}}
