from dataclasses import dataclass
from pathlib import Path
from src.text_summarizer.utils.common import read_yml,create_dirs
import os
import urllib.request as request
from src.text_summarizer.entity import DataIngestionConfig,DataTransformationConfig
from src.text_summarizer.logging import LOGGER
from src.text_summarizer.constants import CONFIG_FILE_PATH,PARAMS_FILE_PATH


class ConfigurationManager:
    def __init__(   
                    self, 
                    config_path = CONFIG_FILE_PATH,
                    # params_filepath = PARAMS_FILE_PATH
                ):
        self.config = read_yml(str(config_path))
        # self.params = read_yml(str(params_filepath))
        create_dirs([self.config.artifacts_root])

    def get_data_ingestion_config(self):
        config = self.config.data_ingestion
        create_dirs([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir = config.root_dir,
            source_url = config.source_url,
            local_data_file = config.local_data_file,
            unzip_dir=config.unzip_dir
        )
        return data_ingestion_config
    
    def get_data_transformation_config(self):
        config = self.config.data_transformation
        create_dirs([config.root_dir])#create root dir of data transformation

        data_transformation_config = DataTransformationConfig(
            root_dir=config.root_dir,
            data_path=config.data_path,
            tokenizer_name=config.tokenizer_name
        )
        return data_transformation_config
