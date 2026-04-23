from dataclasses import dataclass
from pathlib import Path
from src.text_summarizer.utils.common import read_yml,create_dirs
import os
import urllib.request as request
from src.text_summarizer.entity import DataIngestionConfig,ModelTrainerConfig,DataTransformationConfig
from src.text_summarizer.logging import LOGGER
from src.text_summarizer.constants import CONFIG_FILE_PATH,PARAMS_FILE_PATH

class ConfigurationManager:
    def __init__(   
                    self, 
                    config_path = CONFIG_FILE_PATH,
                    params_filepath = PARAMS_FILE_PATH
                ):
        self.config = read_yml(str(config_path))
        self.params = read_yml(str(params_filepath))
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
        self.data_transformation_output = data_transformation_config.root_dir

        return data_transformation_config
    
    def get_model_trainer_config(self):
        transformation_output = self.data_transformation_output# needed for constructing the input data for the model
        model_trainer_config_params = self.config.model_trainer
        data_path = os.path.join(transformation_output,'samsum_dataset')
        create_dirs([model_trainer_config_params.root_dir])
        train_params = self.params.TrainingArguments
        model_trainer_config = ModelTrainerConfig(
            model_ckpt = model_trainer_config_params.model_ckpt,
            num_train_epochs = train_params.num_train_epochs,
            warmup_steps = train_params.warmup_steps,
            per_device_train_batch_size=train_params.per_device_train_batch_size,
            weight_decay=int(float(train_params.weight_decay)),
            logging_steps=train_params.logging_steps,
            evaluation_strategy=train_params.evaluation_strategy,
            eval_steps=train_params.eval_steps,
            save_steps=int(float(train_params.save_steps)),
            gradient_accumulation_steps=train_params.gradient_accumulation_steps,
            data_path=data_path,
            device=model_trainer_config_params.device
        )
        return model_trainer_config

