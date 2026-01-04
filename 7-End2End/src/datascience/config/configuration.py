from src.datascience.constants import *
from src.datascience.utils.common import read_yaml, create_directories
import os
from src.datascience.entity.config_entity import ModelTrainerConfig,DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelEvaluationConfig

class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH,
        schema_filepath = SCHEMA_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)
        create_directories([self.config.artifacts_root])


    def get_data_ingestion_config(self)-> DataIngestionConfig:
        config=self.config.data_ingestion
        create_directories([config.root_dir])

        data_ingestion_config=DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir
        )
        return data_ingestion_config
    
    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation
        schema = self.schema.COLUMNS

        create_directories([config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir,
            STATUS_FILE=config.STATUS_FILE,
            unzip_data_dir = config.unzip_data_dir,
            all_schema=schema,
        )

        return data_validation_config

    def get_data_transformation_config(self):
        config = self.config.data_transformation
        create_directories([config.root_dir])
        data_transformation_config = DataTransformationConfig(
            root_dir=config.root_dir,
            data_path=config.data_path
        )
        return data_transformation_config
    
    def get_model_trainer_config(self):
        config = self.config.model_trainer
        params = self.params
        schema = self.schema

        create_directories([config.root_dir])

        model_trainer_config = ModelTrainerConfig(
            root_dir=config.root_dir,
            train_data_path=config.train_data_path,
            test_data_path=config.test_data_path,
            model_name=config.model_name,
            alpha=params.ElasticNet.alpha,
            l1_ratio=params.ElasticNet.l1_ratio,
            target_column=schema.TARGET_COLUMN.name
        )
        return model_trainer_config

    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        config = self.config.model_evaluation
        params = self.params.ElasticNet
        create_directories([config.root_dir])
        model_val_config = ModelEvaluationConfig(
            root_dir=config.root_dir,
            model_path = config.model_path,
            test_data_path=config.test_data_path,
            metric_file_name=config.metric_file_name,
            all_params=params,
            target_column=self.schema.TARGET_COLUMN.name,
            mlflow_uri=os.environ["MLFLOW_TRACKING_URI"]
        )
        return model_val_config