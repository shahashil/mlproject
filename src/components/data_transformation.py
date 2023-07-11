import sys
from dataclasses import dataclass
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
#from src.exception import CustomException
from exception import CustomException
from logger import logging

import os
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'processor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        '''
        This functio is responsible for Data transformation
        '''
        try:
            numerical_columns   = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]
            
            numerical_pipeline = Pipeline(
                steps = [
                    ("imputer", SimpleImputer(strategy="mean")),
                    ("scaler", StandardScaler())
                 ]
            )
            
            categorical_pipeline = Pipeline(
                steps = [
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                ]
            )

            logging.info(f"Categorical columns : {categorical_columns}")
            logging.info(f"Numerical encoding columns : {numerical_columns}")


            preprocessor = ColumnTransformer(
                steps = [
                    ("numerical pipeline", numerical_pipeline, numerical_columns),
                    ("categorical pipeline", categorical_pipeline, categorical_columns)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.reaf_csv(test_path)

            logging.info("Read train/test data completed")

            preprocessing_obj = self.get_data_transformer_object()

            targer_column_name = "math_score"

            input_feature_train_df  = train_df.drop(columns=[targer_column_name], axis=1)
            target_feature_train_df = train_df[targer_column_name]

            input_feature_test_df  = test_df.drop(columns=[targer_column_name], axis=1)
            target_feature_test_df = test_df[targer_column_name]

            logging.info("Applying preprocessing pipeline on the training and testing dataframe ")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr  = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr  = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info("Saved processing object")

            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj       = preprocessing_obj
            )

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)