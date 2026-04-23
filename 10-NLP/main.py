from src.text_summarizer.logging import LOGGER
from src.text_summarizer.pipeline.stage_1_data_ingestion import DataIngestionTrainingPipeline
from src.text_summarizer.pipeline.stage_2_data_transformation import DataTransformationPipeline
from src.text_summarizer.pipeline.stage_3_model_trainer import ModelTrainerPipeline
from src.text_summarizer.config.configuration import ConfigurationManager

class PipelineOrchestrator:

    def __init__(self):
        self.config_manager = ConfigurationManager()

    def start_stage_1(self):
        LOGGER.info('ENTER start_stage_1')
        try:
            data_ingestion_pipeline = DataIngestionTrainingPipeline(self.config_manager)
            return data_ingestion_pipeline.initiate_data_ingestion()
        except Exception as  e:
            LOGGER.info(e)
            raise e
        LOGGER.info("Exit stage_1")


    def start_stage_2(self):
        LOGGER.info('ENTER stage 2')
        try:
            data_transformation_pipeline = DataTransformationPipeline(self.config_manager)
            data_transformation_pipeline.initiate_data_transformation()
        except Exception as e:
            LOGGER.info(e)
            raise e
        LOGGER.info("EXIT stage 2")

    def start_stage_3(self):
        LOGGER.info("ENTER stage 3")
        try:
            model_trainer_pipeline = ModelTrainerPipeline(self.config_manager)
            model_trainer_pipeline.start_training()
        except Exception as e:
            LOGGER.info(e)
            raise e
        LOGGER.info("EXIT stage 3")

if __name__=='__main__':
    pipeline_orchestrator = PipelineOrchestrator()
    pipeline_orchestrator.start_stage_1()
    pipeline_orchestrator.start_stage_2()
    pipeline_orchestrator.start_stage_3()