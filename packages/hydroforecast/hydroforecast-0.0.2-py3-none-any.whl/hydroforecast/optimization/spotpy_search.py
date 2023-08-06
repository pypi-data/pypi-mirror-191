from typing import List
from spotpy import algorithms, parameter, analyser
import inspect

from hydroforecast.exp.hydrology_exp import HydrologyExp
from hydroforecast.loader.base_module import HydroDataModule
from hydroforecast.optimization import BaseHyperSearch, SearchParam


class SpotpyAlgorithm:
    ABC = algorithms.abc
    DDS = algorithms.dds
    DEMCZ = algorithms.demcz


class model_setup(object):
    def __init__(self, exp: HydrologyExp, datamodule: HydroDataModule, search_params: List[SearchParam]):
        self.exp = exp
        self.datamodule = datamodule
        self.search_params = search_params
        self.params = self.parse_search_params()

    def parameters(self):
        return parameter.generate(self.params)

    def simulation(self, x):
        y_pred = self.exp.train(x, self.datamodule, 0).values
        return y_pred

    def evaluation(self):
        _, y_obs = self.datamodule.get_sample()
        return y_obs

    def objectivefunction(self, simulation, evaluation):
        return self.exp.eval_metric(simulation, evaluation)

    def parse_search_params(self):
        temp_params = []
        for param in self.search_params:
            # todo 其他的分布特征
            if param.param_dtype == 'float':
                temp_param = parameter.Uniform(name=param.name, low=param.low, high=param.high, optguess=param.default)
            else:
                raise NotImplementedError
            temp_params.append(temp_param)
        return temp_params


class SpotpySearch(BaseHyperSearch):
    def __init__(self, direction, path, seed, n_trial: int, sampler=SpotpyAlgorithm.ABC, **sample_args):
        super().__init__(direction, n_trial, path, seed)
        self.sampler = sampler
        self.sample_args = sample_args
        self.sample_args['repetitions'] = n_trial
        self.direction = direction
        self.path = path
        self.seed = seed

    def optimal(self, exp, train_val_datamodule, search_params: List[SearchParam]):
        sampler = self.sampler(model_setup(exp, train_val_datamodule, search_params),
                               dbname='none', dbformat='ram', random_state=self.seed)
        params = inspect.signature(sampler.sample).parameters
        params_dict = {name: param.default for name, param in params.items()}
        for arg_nm, arg_value in self.sample_args.items():
            params_dict[arg_nm] = arg_value
        sampler.sample(*tuple(params_dict.values()))
        results = sampler.getdata()
        best_params = analyser.get_best_parameterset(results)[0]
        return 0, best_params
