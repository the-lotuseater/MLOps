from src.text_summarizer.components.model_trainer import ModelTrainer
from src.text_summarizer.components.model_evaluation import ModelEvaluation
from src.text_summarizer.logging import LOGGER
from src.text_summarizer.config.configuration import ConfigurationManager

class ModelTrainerPipeline:

    def __init__(self,config_manager:ConfigurationManager):
        self.config_manager = config_manager

    def start_evaluation(self):
        LOGGER.info("ENTER evaluation")
        model_eval_config = self.config_manager.get_model_evaluation_config()
        model_eval = ModelEvaluation(model_eval_config,self.config_manager.params.device)
        model_eval.initiate_evaluation()
        LOGGER.info('EXIT start_training')


