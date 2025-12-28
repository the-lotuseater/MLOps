from src.datascience import logger
from src.datascience.pipeline.data_ingestion_pipeline import DataIngestionTrainingPipeline

logger.info('Welcome to my project.')
def start_training_pipeline():
    logger.info('Enter start training pipeline.')
    STAGE_NAME='Data Ingestion Pipeline'
    try:
        logger.info(f'>>>> stage {STAGE_NAME} started <<<<')
        obj = DataIngestionTrainingPipeline()
        obj.initiate_data_ingestion()
        logger.info(f'>>>> {STAGE_NAME} completed <<<<')
    except Exception as e:
        logger.exception(e)
        raise e

    logger.info('Exit start training pipeline.')
    
if __name__=='__main__':
    start_training_pipeline()