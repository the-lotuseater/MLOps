from src.text_summarizer.config.configuration import ConfigurationManager
from src.text_summarizer.components.data_transformation import DataTransformation
from src.text_summarizer.logging import LOGGER
from src.text_summarizer.entity import DataTransformationConfig


class DataTransformationPipeline:

    def __init__(self,config_manager:ConfigurationManager):
        self.config_manager = config_manager

    def initiate_data_transformation(self):
        data_transformation_config = self.config_manager.get_data_transformation_config()
        data_transformation = DataTransformation(data_transformation_config)
        data_transformation.convert()