from src.datascience.config.configuration import ConfigurationManager
from src.datascience.components.data_transformation import DataTransformation
from pathlib import Path

STAGE_NAME='Data Transformation Stage'
class DataTransformationPipeline:

    def __init__(self):
        pass

    def initiate_data_transformation(self):
        try:
            with open(Path('artifacts/data_validation/status.txt'),'r') as f:
                status=f.read().split(':')[-1]
                if status=='False':
                    raise Exception('Data validation was unsuccesfully! Skipping Data Transformation')
            print(f'>>>> Data Validation was successful proceeding with {STAGE_NAME} <<<<')
            config = ConfigurationManager()
            data_transformation_config  = config.get_data_transformation_config()
            data_transformation = DataTransformation(config = data_transformation_config)
            data_transformation.train_test_splitting()
        except Exception as e:
            raise e
