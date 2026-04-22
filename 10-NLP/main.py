from src.text_summarizer.logging import LOGGER
from src.text_summarizer.pipeline.stage_1_data_ingestion import DataIngestionTrainingPipeline

def start_stage_1():
    LOGGER.info('ENTER start_stage_1')
    try:
        data_ingestion_pipeline = DataIngestionTrainingPipeline()
        data_ingestion_pipeline.initiate_data_ingestion()
    except Exception as  e:
       raise e
    LOGGER.info("Exit stage_1")


if __name__=='__main__':
    STAGE = 'Data Ingestion Stage'
    start_stage_1()