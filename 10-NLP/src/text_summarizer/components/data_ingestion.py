from dataclasses import dataclass
from pathlib import Path
from src.text_summarizer.utils.common import read_yml,create_dirs
import os
import urllib.request as request
from src.text_summarizer.entity import DataIngestionConfig
from src.text_summarizer.logging import LOGGER
import zipfile

class DataIngestion:
    def __init__(self,config:DataIngestionConfig):
        self.config = config

    def download_file(self):
        '''
            Given a local data file path download the file 
        '''
        if not os.path.exists(self.config.local_data_file):
            file_name, _ = request.urlretrieve(
                url = self.config.source_url,
                filename = self.config.local_data_file
            )
            LOGGER.info(f'File name={file_name} is downloaded.')
        else:
            LOGGER.info(f'File already exists.')

    def extract_zip_file(self):
        '''
            unzip the file in the given config file
        '''
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path,exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file,'r') as zip_ref:
            zip_ref.extractall(unzip_path)


