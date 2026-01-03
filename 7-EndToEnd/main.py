from src.datascience import logger
from src.datascience.pipeline.data_ingestion_pipeline import DataIngestionTrainingPipeline
from src.datascience.pipeline.data_validation_pipeline import DataValidationTrainingPipeline
from src.datascience.pipeline.model_trainer_pipeline import ModelTrainerPipeline
from src.datascience.pipeline.data_transformation import DataTransformationPipeline

logger.info('Welcome to my project.')
def start_training_pipeline():
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

    except Exception as e:
        logger.exception(e)
        raise e

    logger.info('Exit start training pipeline.')
    
if __name__=='__main__':
    start_training_pipeline()