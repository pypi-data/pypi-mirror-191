import os
from hydroforecast.exp.base_exp import BaseExp
from hydroforecast.exp.exp_path import ExpPath
from hydroforecast.loader.base_module import HydroDataModule
from hydroforecast.models.concept_models import HydroModel
from hydroforecast.optimization import BaseHyperSearch


class HydrologyExp(BaseExp):

    def save_model(self, save_path):
        pass

    def save_result(self, best_params=None):
        pass

    EXP_NAME = 'Hydrology EXP'
    MODEL_NAME = 'Hydrological model family'
    MODEL_PARAMS = []

    def __init__(self, exp_path: ExpPath, model_obj: HydroModel, eval_metric, store_init):
        super(HydrologyExp, self).__init__(exp_path)
        self.eval_metric = eval_metric
        self.store_init = store_init
        self.model_obj = model_obj
        self.MODEL_PARAMS = model_obj.model_params

        self.best_model = None
        self.best_hyperparams: dict = {}

    def build_model(self, params, datamodule):
        return self.model_obj.build_model(params, delta_t=1)

    def calibrate(self, search_method: BaseHyperSearch, train_val_datamodule: HydroDataModule):
        best_search_idx, self.best_hyperparams = search_method.optimal(self, train_val_datamodule, self.MODEL_PARAMS)
        model: HydroModel = self.build_model(self.best_hyperparams, None)
        climate_data, streamflow_obs = train_val_datamodule.get_sample()
        model.run(climate_data, self.store_init)
        # todo save model
        save_path = os.path.join(self.exp_path.checkpoint_path, 'tune_history')
        self.best_model = model

    def train(self, params, train_datamodule: HydroDataModule, search_idx: int, optuna_trial=None):
        model: HydroModel = self.build_model(params, None)
        climate_data, streamflow_obs = train_datamodule.get_sample()
        model.run(climate_data, self.store_init)
        y_pred = model.get_streamflow(climate_data, self.store_init)
        return y_pred

    def forecast(self, datamodule: HydroDataModule):
        """
        :params func: like model.predict
        :params dataset: 
        :return: 
        """
        climate_data = datamodule.get_sample()
        streamflow_forecast = self.best_model.forecast(climate_data)
        return streamflow_forecast
