from enum import Enum
from typing import List

import optuna
import json
from hydroforecast.exp.exp_path import ExpPath
import os

from hydroforecast.optimization import BaseHyperSearch, SearchParam


class OptunaSampler(Enum):
    No = None
    Random = optuna.samplers.RandomSampler()
    TPE = optuna.samplers.TPESampler()
    CmaEs = optuna.samplers.CmaEsSampler()
    QMS = optuna.samplers.QMCSampler()


class OptunaPruner(Enum):
    No = None
    Patient = optuna.pruners.PatientPruner(optuna.pruners.MedianPruner(), patience=3)
    Percentile = pruner = optuna.pruners.PercentilePruner(
        25.0, n_startup_trials=5, n_warmup_steps=30, interval_steps=10
    ),
    Median = optuna.pruners.MedianPruner(n_startup_trials=5, n_warmup_steps=30, interval_steps=10)
    SuccessiveHalving = optuna.pruners.SuccessiveHalvingPruner()
    Hyperband = optuna.pruners.HyperbandPruner()


class OptunaHyperSearch(BaseHyperSearch):
    SEARCH_ALGORITHM = "Optuna"

    def __init__(self, direction: str, n_trial: int, path: ExpPath, seed: int):
        super().__init__(direction, n_trial, path, seed)
        self.study_nm = 'seed_{}'.format(self.exp_seed)
        self.storage = 'sqlite:///{}'.format(os.path.join(path.db_save_path, 'study.db'))
        self.study = optuna.create_study(study_name=self.study_nm, direction=self.study_direction,
                                         storage=self.storage, load_if_exists=True)

    def save_search_result(self, final=False):
        df = self.study.trials_dataframe(attrs=('number', 'value', 'duration', 'params', 'state'))
        if final:
            best_params = self.study.best_trial.params
            best_params['trial_id'] = self.study.best_trial.number
            with open(self.exp_path.tune_path + '\\best_param.json', 'w') as f:
                f.write(json.dumps(best_params))
        df.to_csv(self.exp_path.tune_path + '\\trials_dataframe.csv')

    def load_search_result(self):
        reloaded_study = optuna.load_study(study_name=self.study_nm, storage=self.storage)
        return reloaded_study

    def check_if_complete(self):
        if len(self.study.trials) < self.n_trial:
            print(self.study.study_name + " have search for {} times, continue to calibrate".format(
                len(self.study.trials)))
            return False
        else:
            print(self.study.study_name + " have already search for {} times, it is no necessary to continue".format(
                len(self.study.trials)))
            return True

    def optimal(self, exp, train_val_datamodule, search_params: List[SearchParam]):
        def objective(trial: optuna.Trial):
            params_dict = {}
            for param in search_params:
                if param.param_dtype == 'category':
                    params_dict[param.name] = trial.suggest_categorical(param.name, param.category_list)
                elif param.param_dtype == 'int':
                    if param.log:
                        params_dict[param.name] = trial.suggest_int(name=param.name, low=param.low, high=param.high,
                                                                    log=param.log)
                    else:
                        params_dict[param.name] = trial.suggest_int(name=param.name, low=param.low,
                                                                    high=param.high,
                                                                    step=param.step if param.step else 1)
                elif param.param_dtype == 'float':
                    if param.log:
                        params_dict[param.name] = trial.suggest_float(name=param.name, low=param.low, high=param.high,
                                                                      log=param.log)
                    else:
                        if param.step:
                            params_dict[param.name] = trial.suggest_float(name=param.name, low=param.low,
                                                                          high=param.high, step=param.step)
                        else:
                            params_dict[param.name] = trial.suggest_float(name=param.name, low=param.low,
                                                                          high=param.high)
                else:
                    raise NotImplementedError
            eval_result = exp.evaluate(params_dict, train_val_datamodule, trial.number, trial)
            self.save_search_result()
            return eval_result

        if_complete = self.check_if_complete()
        if if_complete:
            return self.study.best_trial.number, self.study.best_params
        else:
            self.study.optimize(objective, n_trials=self.n_trial - len(self.study.trials))
            self.save_search_result(final=True)
            return self.study.best_trial.number, self.study.best_params
