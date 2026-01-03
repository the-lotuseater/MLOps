
from src.datascience.components.model_trainer import ModelTrainer
from src.datascience.config.configuration import ConfigurationManager

STAGE_NAME = "Model Trainer Stage"
class ModelTrainerPipeline:
    def __init__(self):
        pass
    
    def start_train_pipeline(self):
        try:
            print(f">>>>>> stage {STAGE_NAME} started <<<<<<")
            configManager = ConfigurationManager()
            config = configManager.get_model_trainer_config()
            trainer = ModelTrainer(config = config)
            trainer.train()
            print(f">>>>>> stage {STAGE_NAME} completed <<<<<<")
        except Exception as e:
            print(f">>>>>> stage {STAGE_NAME} failed <<<<<<")
            raise e