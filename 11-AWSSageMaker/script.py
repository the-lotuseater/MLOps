
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,classification_report, confusion_matrix,precision_score

import sklearn
import joblib

import boto3
from io import StringIO

import argparse
import os
import numpy as np
import pandas as pd

def model_fn(model_dir):
    clf = joblib.load(os.path.join(model_dir,'model.joblib'))
    return clf

if __name__=='__main__':
    print('Info extracting args')
    parser = argparse.ArgumentParser()
    ##hyperparameter for random forest

    parser.add_argument('--n_estimators',type=int, default=100)
    parser.add_argument('--random_state',type=int, default=0)


    #output dirs declaration
    parser.add_argument('--model-dir',type=str,default=os.environ.get('SM_MODEL_DIR'))
    parser.add_argument('--train',type=str,default=os.environ.get('SM_CHANNEL_TRAIN'))
    parser.add_argument('--test',type=str,default=os.environ.get('SM_CHANNEL_TEST'))
    parser.add_argument('--train-file',type=str,default='train_V1.csv')
    parser.add_argument('--test-file',type=str,default='test_V1.csv')


    args, _ = parser.parse_known_args()
    print(f'sklearn version={sklearn.__version__}')
    print(f'joblib version={joblib.__version__}')

    print(f'[INFO] reading data')
    print()

    train_df = pd.read_csv(os.path.join(args.train, args.train_file))
    test_df = pd.read_csv(os.path.join(args.test, args.test_file))


    # train_df = train_df.fillna(train_df.median())
    # test_df  = test_df.fillna(train_df.median())  # use train median for both
    cols = list(train_df.columns)
    features = cols[:-1]
    label = cols[-1]

    X_train = train_df[features]
    X_test = test_df[features]
    y_train = train_df[label]
    y_test = test_df[label]


    print(f'X_train shape={X_train.shape}')
    print(f'Y_train shape={y_train.shape}')
    print(f'X_test shape={X_test.shape}')
    print(f'y_test shape={y_test.shape}')
    model = RandomForestClassifier(
                n_estimators = args.n_estimators,
                random_state=args.random_state,
                verbose=2,
                n_jobs=1
            )
    model.fit(X_train,y_train)


    model_path = os.path.join(args.model_dir,'model.joblib')

    joblib.dump(model,model_path)

    print(f'Saved model at path={model_path}')
    y_pred_test = model.predict(X_test)

    test_acc = accuracy_score(y_test,y_pred_test)
    test_rep = classification_report(y_test,y_pred_test)


    print()
    print('---METRICS RESULTS for TESTING DATA---')
    print(f'Total rows are:{ X_test.shape[0]}')
    print(f'[TESTING] Model Accuracy is: {test_acc}')
    print(f'[TESTING] Testing report: {test_rep}')
