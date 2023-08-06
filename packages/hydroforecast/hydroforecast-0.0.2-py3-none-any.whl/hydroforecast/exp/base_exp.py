import os


class BaseExp(object):
    EXP_NAME = 'base EXP'
    MODEL_NAME = 'None'
    MODEL_PARAMS = []

    def __init__(self, exp_path):
        """
        :param exp_path:
        """
        self.exp_path = exp_path

    def calibrate(self, search_method, train_val_datamodule):
        raise NotImplementedError

    def forecast(self, datamodule):
        raise NotImplementedError

    def save_model(self, save_path):
        raise NotImplementedError

    def save_result(self, best_params=None):
        raise NotImplementedError

    def build_model(self, params, datamodule):
        raise NotImplementedError

    def modify_model_param(self, params):
        self.MODEL_PARAMS = params

    def load_best_model(self, best_param=None):
        if not os.path.exists(os.path.join(self.exp_path.checkpoint_path, 'tune_history', 'best')):
            print('best model is not found, train a model first')
        raise NotImplementedError
