
from pathlib import Path
import json
import joblib
import pandas as pd
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, matthews_corrcoef, confusion_matrix, classification_report
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.preprocessing import StandardScaler
from models.preprocessing import D1FeatureBuilder, D1_FEATURES, D2_FEATURES

BASE_DIR=Path(__file__).resolve().parent
MODEL_DIR=BASE_DIR/"trained_models"
RANDOM_STATE=42
TEST_SIZE=0.25
CV_FOLDS=5

def clean_d2(df):
    df=df.copy(); target=df.columns[-1]; age=df.columns[1]; survey=df.columns[2:-1].tolist()
    df=df.loc[df[age].between(15,60)].copy()
    uniformity=1-(df[survey].nunique(axis=1)/len(survey))
    df=df.loc[uniformity<0.80].copy()
    def encode(v):
        s=str(v).strip().lower()
        if s.startswith("distress"): return 0
        if s.startswith("eustress"): return 1
        if "no stress" in s: return 2
        raise ValueError(f"Unknown D2 target: {v!r}")
    df["__target__"]=df[target].map(encode)
    if df["__target__"].isna().any(): raise ValueError("Unrecognized D2 target label.")
    return df

def d1_candidates():
    lr=ImbPipeline([("features",D1FeatureBuilder()),("scale",StandardScaler()),("model",LogisticRegression(random_state=RANDOM_STATE,max_iter=2000))])
    rf=ImbPipeline([("features",D1FeatureBuilder()),("model",RandomForestClassifier(random_state=RANDOM_STATE,n_jobs=-1))])
    return [(lr,{"model__C":[0.01,0.1,1,10],"model__solver":["lbfgs","saga"]}),
            (rf,{"model__n_estimators":[100,200,400],"model__max_depth":[None,8,15],"model__min_samples_split":[2,5],"model__class_weight":[None,"balanced"]})]

def d2_candidates():
    lr=ImbPipeline([("scale",StandardScaler()),("smote",SMOTE(random_state=RANDOM_STATE,k_neighbors=3)),("model",LogisticRegression(random_state=RANDOM_STATE,max_iter=3000))])
    rf=ImbPipeline([("smote",SMOTE(random_state=RANDOM_STATE,k_neighbors=3)),("model",RandomForestClassifier(random_state=RANDOM_STATE,n_jobs=-1))])
    return [(lr,{"model__C":[0.01,0.1,1,10],"model__solver":["lbfgs","saga"]}),
            (rf,{"model__n_estimators":[100,200,400],"model__max_depth":[None,8,15],"model__min_samples_split":[2,5],"model__class_weight":[None,"balanced"]})]

def tune(X,y,candidates):
    cv=StratifiedKFold(CV_FOLDS,shuffle=True,random_state=RANDOM_STATE)
    searches=[]
    for estimator,grid in candidates:
        s=GridSearchCV(estimator,grid,scoring="f1_macro",cv=cv,n_jobs=-1,refit=True,return_train_score=False)
        s.fit(X,y); searches.append(s)
        print("CV macro-F1:",round(s.best_score_,4),"params:",s.best_params_)
    return max(searches,key=lambda s:s.best_score_)

def evaluate(model,X,y):
    p=model.predict(X)
    return {
        "accuracy":float(accuracy_score(y,p)),
        "precision_macro":float(precision_score(y,p,average="macro",zero_division=0)),
        "recall_macro":float(recall_score(y,p,average="macro",zero_division=0)),
        "f1_macro":float(f1_score(y,p,average="macro",zero_division=0)),
        "f1_weighted":float(f1_score(y,p,average="weighted",zero_division=0)),
        "mcc":float(matthews_corrcoef(y,p)),
        "confusion_matrix":confusion_matrix(y,p,labels=[0,1,2]).tolist(),
        "classification_report":classification_report(y,p,labels=[0,1,2],output_dict=True,zero_division=0),
    }

def save(name,search,metrics,features,classes,shape):
    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(search.best_estimator_,MODEL_DIR/f"{name}_pipeline.pkl")
    meta={"dataset":name,"selected_algorithm":search.best_estimator_.steps[-1][1].__class__.__name__,"cv_macro_f1":float(search.best_score_),
          "best_params":search.best_params_,"input_features":features,"output_classes":classes,
          "dataset_shape_after_cleaning":list(shape),"metrics":metrics,"random_state":RANDOM_STATE,
          "test_size":TEST_SIZE,"cv_folds":CV_FOLDS,"preprocessing":"saved inside pipeline"}
    (MODEL_DIR/f"{name}_metadata.json").write_text(json.dumps(meta,indent=2),encoding="utf-8")

def main():
    d1=pd.read_csv(BASE_DIR/"StressLevelDataset.csv")
    d2=clean_d2(pd.read_csv(BASE_DIR/"Stress_Dataset.csv"))
    X1,y1=d1[D1_FEATURES],d1["stress_level"].astype(int)
    X2,y2=d2[D2_FEATURES],d2["__target__"].astype(int)
    X1tr,X1te,y1tr,y1te=train_test_split(X1,y1,test_size=TEST_SIZE,random_state=RANDOM_STATE,stratify=y1)
    X2tr,X2te,y2tr,y2te=train_test_split(X2,y2,test_size=TEST_SIZE,random_state=RANDOM_STATE,stratify=y2)
    best1=tune(X1tr,y1tr,d1_candidates()); best2=tune(X2tr,y2tr,d2_candidates())
    m1=evaluate(best1.best_estimator_,X1te,y1te); m2=evaluate(best2.best_estimator_,X2te,y2te)
    save("d1",best1,m1,D1_FEATURES,["Low Stress","Moderate Stress","High Stress"],d1.shape)
    save("d2",best2,m2,D2_FEATURES,["Distress","Eustress","No Stress"],d2.shape)
    print("D1:",m1["accuracy"],m1["f1_macro"],m1["mcc"])
    print("D2:",m2["accuracy"],m2["f1_macro"],m2["mcc"])
    print("Artifacts:",MODEL_DIR)

if __name__=="__main__": main()
