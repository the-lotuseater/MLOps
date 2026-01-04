from src.datascience import logger
from src.datascience.pipeline.data_ingestion_pipeline import DataIngestionTrainingPipeline
from src.datascience.pipeline.data_validation_pipeline import DataValidationTrainingPipeline
from src.datascience.pipeline.model_trainer_pipeline import ModelTrainerPipeline
from src.datascience.pipeline.model_evaluation_pipeline import ModelEvaluationPipeline
from src.datascience.pipeline.data_transformation import DataTransformationPipeline
import os

logger.info('Welcome to my project.')
def start_pipelines():
    logger.info('Enter start training pipeline.')
    try:
        STAGE_NAME='Data Ingestion Pipeline'
        logger.info(f'>>>> stage {STAGE_NAME} started <<<<')
        obj = DataIngestionTrainingPipeline()
        obj.initiate_data_ingestion()
        logger.info(f'>>>> {STAGE_NAME} completed <<<<')

        STAGE_NAME='Data Validation Pipeline'
        logger.info(f'>>>> stage {STAGE_NAME} started <<<<')
        obj = DataValidationTrainingPipeline()
        obj.initiate_data_validation()
        logger.info(f'>>>> {STAGE_NAME} completed <<<<')

        pipeline = DataTransformationPipeline()
        STAGE_NAME='Data Transformation Pipeline'
        logger.info(f'>>>> stage {STAGE_NAME} started <<<<')
        pipeline.initiate_data_transformation()
        logger.info(f'>>>> {STAGE_NAME} completed <<<<')

        pipeline = ModelTrainerPipeline()
        STAGE_NAME='Model Trainer Pipeline'
        logger.info(f'>>>> stage {STAGE_NAME} started <<<<')
        pipeline.start_train_pipeline()
        logger.info(f'>>>> {STAGE_NAME} completed <<<<')


        pipeline = ModelEvaluationPipeline()
        STAGE_NAME='Model Evaluation Pipeline'
        logger.info(f'>>>> stage {STAGE_NAME} started <<<<')
        pipeline.start_pipline()
        logger.info(f'>>>> {STAGE_NAME} completed <<<<')
    except Exception as e:
        logger.exception(e)
        raise e

    logger.info('Exit start training pipeline.')
    
if __name__=='__main__':
    os.environ["MLFLOW_TRACKING_URI"] = "https://dagshub.com/agbirhade1/MLOps-Project7.mlflow"
    os.environ["MLFLOW_TRACKING_PASSWORD"] = "bb8e44ff7f0afbc4148df5114797562149c14a25" #in dags hub this is data/dvc access key
    os.environ["MLFLOW_TRACKING_USERNAME"] = "agbirhade1"
    start_pipelines()