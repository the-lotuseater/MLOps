from src.text_summarizer.components.model_trainer import ModelTrainer
from src.text_summarizer.logging import LOGGER
from src.text_summarizer.config.configuration import ConfigurationManager

class ModelTrainerPipeline:

    def __init__(self,config_manager:ConfigurationManager):
        self.config_manager = config_manager

    def start_training(self):
        LOGGER.info("ENTER start_training")
        model_trainer_config = self.config_manager.get_model_trainer_config()
        model_trainer = ModelTrainer(model_trainer_config)
        model_trainer.train()
        LOGGER.info('EXIT start_training')


