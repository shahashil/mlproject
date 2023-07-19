import os
import sys
import numpy as np
import pandas as pd
import dill
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
#from src.exception import CustomException
from exception import CustomException
from logger import logging

def save_object(file_path, obj):
    try:
        dir_name = os.path.dirname(file_path)
        os.makedirs(dir_name, exist_ok=True)
        with open(file_path,"wb") as file_obj:
            dill.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)

def load_object(file_path):
    try:
        with open(file_path,"rb") as file_obj:
            return dill.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)        



def evaluate_models(X_train,y_train,X_test,y_test,models,param):
    try:
        report = {}

        for model_name in models.keys():
            model = models[model_name]
            para=param[model_name]
            
            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)                        
            # model.fit(X_train,y_train)

            y_train_pred = model.predict(X_train)
            y_test_pred  = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score  = r2_score(y_test,y_test_pred)

            report[model_name] = test_model_score
        
        return report
    except Exception as e:
        raise CustomException(e, sys)
    
