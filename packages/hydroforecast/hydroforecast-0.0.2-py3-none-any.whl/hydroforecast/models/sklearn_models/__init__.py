import os
import joblib

from lightgbm import LGBMRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.svm import SVR as sk_SVR
from xgboost import XGBRegressor

from hydroforecast.models import BaseModel
from hydroforecast.optimization import SearchParam


class BaseSklearnModel(BaseModel):
    model = None

    def __str__(self):
        pass

    def fit_model(self, train_x, train_y, val_x=None, val_y=None):
        self.model.fit(train_x, train_y)

    def predict(self, x):
        return self.model.predict(x)

    def save_model(self, save_path):
        joblib.dump(self.model, os.path.join(save_path, "model.m"))

    def load_model(self, save_path):
        return joblib.load(save_path)


class LR(BaseSklearnModel):
    MODEL_PARAMS = [SearchParam(name='alpha', dtype='float', low=1e-3, high=1, log=True),
                    SearchParam(name='model_type', dtype='category',
                                category_list=['LinearRegression', 'Lasso', 'Ridge'])]

    def __init__(self, model_type, alpha, input_dim, output_dim, slide_window):
        super().__init__(input_dim, output_dim, slide_window)
        if model_type == 'LinearRegression':
            model = LinearRegression()
        elif model_type == 'Lasso':
            model = Lasso(alpha=alpha)
        elif model_type == 'Ridge':
            model = Ridge(alpha=alpha)
        else:
            raise NotImplementedError
        self.model = model


class SVR(BaseSklearnModel):
    MODEL_PARAMS = [SearchParam(name='kernel', dtype='category', category_list=['linear', 'poly', 'rbf']),
                    SearchParam(name='degree', dtype='int', low=2, high=4, step=1),
                    SearchParam(name='gamma', dtype='float', low=1e-6, high=1, log=True),
                    SearchParam(name='epsilon', dtype='float', low=1e-6, high=1, log=True),
                    SearchParam(name='C', dtype='float', low=1e-1, high=2e2, log=True)]

    def __init__(self, input_dim, output_dim, slide_window, kernel, degree, gamma, C, epsilon):
        super().__init__(input_dim, output_dim, slide_window)
        self.model = sk_SVR(kernel=kernel, degree=degree, gamma=gamma,
                            C=C, epsilon=epsilon, verbose=True, max_iter=5e4)


class GBR(BaseSklearnModel):
    MODEL_PARAMS = [SearchParam(name='min_samples_leaf', dtype='int', low=2, high=100),
                    SearchParam(name='min_samples_split', dtype='int', low=2, high=100),
                    SearchParam(name='n_estimators', dtype='int', low=20, high=200),
                    SearchParam(name='lr', dtype='float', low=1e-3, high=1, log=True),
                    SearchParam(name='max_depth', dtype='int', low=1, high=25)]

    def __init__(self, input_dim, output_dim, slide_window, lr, n_estimators, min_samples_split, min_samples_leaf):
        super().__init__(input_dim, output_dim, slide_window)
        self.model = GradientBoostingRegressor(learning_rate=lr,
                                               n_estimators=n_estimators,
                                               min_samples_split=min_samples_split,
                                               min_samples_leaf=min_samples_leaf)


class XGB(BaseSklearnModel):
    MODEL_PARAMS = [SearchParam(name='min_samples_leaf', dtype='int', low=2, high=100),
                    SearchParam(name='min_samples_split', dtype='int', low=2, high=100),
                    SearchParam(name='n_estimators', dtype='int', low=20, high=200),
                    SearchParam(name='lr', dtype='float', low=1e-3, high=1, log=True),
                    SearchParam(name='max_depth', dtype='int', low=1, high=25)]

    def __init__(self, input_dim, output_dim, slide_window, max_depth, n_estimators, reg_lambda, reg_alpha, eta,
                 subsample, colsample_bytree):
        super().__init__(input_dim, output_dim, slide_window)
        self.model = XGBRegressor(max_depth=max_depth, verbosity=1, n_estimators=n_estimators,
                                  booster="gbtree", reg_lambda=reg_lambda, reg_alpha=reg_alpha,
                                  learning_rate=eta, subsample=subsample,
                                  colsample_bytree=colsample_bytree)

    def fit_model(self, train_x, train_y, val_x=None, val_y=None):
        self.model.fit(train_x, train_y, eval_set=[(val_x, val_y)], early_stopping_rounds=5, eval_metric='rmse')


class LGBMExp(BaseSklearnModel):
    MODEL_PARAMS = [SearchParam(name='reg_lambda', dtype='float', low=1e-5, high=1, log=True),
                    SearchParam(name='reg_alpha', dtype='float', low=1e-9, high=1e-3, log=True),
                    SearchParam(name='max_depth', dtype='int', low=1, high=10, step=1),
                    SearchParam(name='eta', dtype='float', low=1e-3, high=1, log=True),
                    SearchParam(name='n_estimators', dtype='int', low=50, high=200),
                    SearchParam(name='num_leaves', dtype='int', low=10, high=50), ]

    def __init__(self, input_dim, output_dim, slide_window, max_depth, num_leaves, n_estimators, eta, reg_lambda,
                 reg_alpha):
        super().__init__(input_dim, output_dim, slide_window)
        self.model = LGBMRegressor(max_depth=max_depth, num_leaves=num_leaves,
                                   n_estimators=n_estimators, learning_rate=eta,
                                   reg_lambda=reg_lambda, reg_alpha=reg_alpha)

    def fit_model(self, train_x, train_y, val_x=None, val_y=None):
        self.model.fit(train_x, train_y, eval_set=(val_x, val_y), early_stopping_rounds=5, eval_metric='rmse')
