import sys,os,time
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact,
)

from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.utils.main_utils.utils import save_object, save_numpy_array_data

class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        try:
            logging.info(f"{'>>'*20} Data Transformation {'<<'*20}")
            self.data_validation_artifact:DataValidationArtifact=data_validation_artifact
            self.data_transformation_config:DataTransformationConfig=data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
    
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    def get_data_tranformer_object(cls)->Pipeline:
        """
        Argument:
            cls:DataTranformation
        retrn:
            a pipeline object
        """
        logging.info("Entered get_data_transformer_object method")
        try:
            imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"Created KNN Imputer object{DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            processor:Pipeline=Pipeline(steps=[('imputer', imputer)])
            logging.info("Created knn imputer object")
            return processor
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("Entered initiate_data_transformation method")
        try:
            logging.info(f"Obtaining preprocessing object.")
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            #training dataframe
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df=train_df[TARGET_COLUMN]
            target_feature_train_df=target_feature_train_df.replace(-1,0)

            #test dataframe
            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df=test_df[TARGET_COLUMN]
            target_feature_test_df=target_feature_test_df.replace(-1, 0)

            preprocessor=self.get_data_tranformer_object()
            preprocessor_object=preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature=preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature=preprocessor_object.transform(input_feature_test_df)

            train_arr=np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr=np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]


            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_object)

            #preparing artifact
            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifact
        
        
        
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e