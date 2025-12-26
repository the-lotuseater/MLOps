import os
import sys
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error,r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from urllib.parse import urlparse
import mlflow
from mlflow.models.signature import infer_signature
import mlflow.sklearn
import logging

def init():
    os.environ['MLFLOW_TRACKING_URI']='http://ec2-3-21-102-106.us-east-2.compute.amazonaws.com:5000'

def eval_metrics(actual,pred):
    rmse = np.sqrt(mean_squared_error(actual,pred))
    mae = mean_absolute_error(actual,pred)
    r2 = r2_score(actual,pred)
    return rmse,mae,r2

def main():
    logger.info('Enter main')
    csv_url=(
        "https://raw.githubusercontent.com/mlflow/mlflow/master/tests/datasets/winequality-red.csv"
    )
    try:
        data = pd.read_csv(csv_url,sep=';')
        logger.info('Loaded data as csv')
        train,test = train_test_split(data,test_size=0.2)
        X_train = train.drop(columns=['quality'])
        Y_train = train['quality']
        X_test = test.drop(columns=['quality'])
        Y_test = test['quality']
        logger.info('Created train test split of features and labels')
        alpha =  float(sys.argv[1] if len(sys.argv)>1 else 0.5)
        l1_ratio =  float(sys.argv[2] if len(sys.argv)>2 else 0.5)

        logger.info('Starting training with mlflow')
        with mlflow.start_run():
            lr = ElasticNet(alpha=alpha,l1_ratio=l1_ratio,random_state=28041997)
            lr.fit(X_train,Y_train)
            pred = lr.predict(X_test)
            (rmse,mae,r2) = eval_metrics(Y_test, pred)
            
            print('Elasticnet model (alpha={:f}, l1_ratio=P{:f}):'.format(alpha,l1_ratio))
            print(' RMSE : %s' %rmse)
            print(' MAE: %s' %mae)
            print(' R2: %s' %r2)
            mlflow.log_param("best_alpha", alpha)
            mlflow.log_param("l1_ratio", l1_ratio)
            mlflow.log_metric('rmse',rmse)
            mlflow.log_metric('mae',mae)
            mlflow.log_metric('r2',r2)

            remote_server_uri = 'http://ec2-3-21-102-106.us-east-2.compute.amazonaws.com:5000'
            mlflow.set_tracking_uri(remote_server_uri)

            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

            if tracking_url_type_store!='file':
                mlflow.sklearn.log_model(lr,'model',registered_model_name='ElasticnetWineModel')
            else:
                mlflow.sklearn.log_model(lr,'model')

        logger.info('Exit main')
    except Exception as e:
        logger.exception(e)

if __name__=='__main__':
    init()
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    #data ingestion reading the dataset -- wine quality dataset
    main()