from src.text_summarizer.logging import LOGGER
from src.text_summarizer.pipeline.stage_1_data_ingestion import DataIngestionTrainingPipeline
from src.text_summarizer.pipeline.stage_2_data_transformation import DataTransformationPipeline

def start_stage_1():
    LOGGER.info('ENTER start_stage_1')
    try:
        data_ingestion_pipeline = DataIngestionTrainingPipeline()
        data_ingestion_pipeline.initiate_data_ingestion()
    except Exception as  e:
        LOGGER.info(e)
        raise e
    LOGGER.info("Exit stage_1")


def start_stage_2():
    LOGGER.info('ENTER stage 2')
    try:
        data_transformation_pipeline = DataTransformationPipeline()
        data_transformation_pipeline.initiate_data_transformation()
    except Exception as e:
        LOGGER.info(e)
        raise e
    LOGGER.info("EXIT stage 2")

if __name__=='__main__':
    STAGE = 'Data Ingestion Stage'
    start_stage_1()
    start_stage_2()