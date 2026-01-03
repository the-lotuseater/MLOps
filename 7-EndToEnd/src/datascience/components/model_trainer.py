import pandas as pd
import os
from src.datascience import logger
from sklearn.linear_model import ElasticNet
import joblib
from src.datascience.entity.config_entity import ModelTrainerConfig


class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def train(self):
        train_data = pd.read_csv(self.config.train_data_path)
        test_data = pd.read_csv(self.config.test_data_path)

        X_train = train_data.drop(columns=[self.config.target_column])
        Y_train = train_data[[self.config.target_column]]

        X_test = test_data.drop(columns=[self.config.target_column])
        Y_test = test_data[[self.config.target_column]]

        model = ElasticNet(alpha=self.config.alpha,
                            l1_ratio=self.config.l1_ratio,
                        )
        model.fit(X_train,Y_train)

        joblib.dump(model,os.path.join(self.config.root_dir,self.config.model_name))
        print('Finished Saving trained model')