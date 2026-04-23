from src.text_summarizer.config.configuration import ConfigurationManager
from src.text_summarizer.components.data_ingestion import DataIngestion
from src.text_summarizer.logging import LOGGER

class DataIngestionTrainingPipeline:

    def __init__(self,config_manager:ConfigurationManager):
        self.config_manager = config_manager

    def initiate_data_ingestion(self):
        data_ingestion_config = self.config_manager.get_data_ingestion_config()
        data_ingestion = DataIngestion(config = data_ingestion_config)
        data_ingestion.download_file()
        data_ingestion.extract_zip_file()        