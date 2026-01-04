from src.datascience.config.configuration import ConfigurationManager
from src.datascience.components.model_evaluation import ModelEvaluation

class ModelEvaluationPipeline:
    def __init__(self):
        pass

    def start_pipline(self):
        try:
            config = ConfigurationManager()
            model_eval_config = config.get_model_evaluation_config()
            model_eval = ModelEvaluation(config=model_eval_config)  
            model_eval.log_into_mlflow()
        except Exception as e:
            raise e

    