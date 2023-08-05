from pandas import DataFrame
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, SGDRegressor
from sklearn.metrics import mean_squared_error
from fsplib.Dataset import Dataset
import lightgbm as lgb
import numpy as np
# import neptune


class Model():

    def __init__(self, dataset: Dataset):
        self.dataset = dataset
        self.model = None


    def fit(self, X_train, y_train, X_test, y_test):
        self.model.fit(X_train, y_train)
        err = mean_squared_error(y_test,
                                 self.model.predict(X_test),
                                 squared=False)
        print(err)
        self.val_scores.append(err)

    def train(self, cv):
        self.val_scores = []
        for X_train, y_train, X_test, y_test in self.dataset.split(cv):
            self.fit(X_train, y_train, X_test, y_test)

    def save_model():
        ...

    def predict(self, test):
        ...


class LGBModel(Model):
    '''_summary_
    '''

    def __init__(self, dataset: Dataset) -> None:
        '''_summary_
        '''
        self.params = {
            'boosting_type': 'gbdt',
            'objective': 'regression',
            'metric': 'RMSE',
            'num_leaves': 31,
            'learning_rate': 0.05,
            'verbose': 1,
            'n_estimators': 100,
            'device': 'gpu'
        }
        super().__init__(dataset)
        self.model = lgb.LGBMModel()
        self.model.set_params(**self.params)


class LinModel(Model):

    def __init__(self, dataset: Dataset):
        super().__init__(dataset)
        self.model = LinearRegression(n_jobs=-1)

    def predict(self, test):
        return self.model.predict(test)


class LinModel2(Model):

    def __init__(self, dataset: Dataset):

        self.params = {
            'loss': 'squared_error',
            'penalty': 'l2',
            'alpha': 0.1,
            'verbose': 0,
            'shuffle': False,
            'early_stopping': True,
            'warm_start': True,
            'eta0': 0.01
        }
        super().__init__(dataset)
        self.model = SGDRegressor(**self.params)

