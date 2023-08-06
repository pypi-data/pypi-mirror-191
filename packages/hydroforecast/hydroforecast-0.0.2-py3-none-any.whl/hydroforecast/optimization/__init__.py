from typing import List, Union

from hydroforecast.exp.exp_path import ExpPath


class SearchParam(object):
    def __init__(self, name, dtype, default=None,
                 low: Union[int, float] = None, high: Union[int, float] = None,
                 step: Union[int, float] = None, log: bool = None,
                 category_list: List[str] = None, param_describe=None, unit=None):
        self.name = name
        self.param_dtype = dtype
        self.default = default
        self.param_describe = param_describe
        self.unit = unit
        if self.param_dtype == 'category':
            # todo 建立enum描述类别参数和数值参数
            self.category_list = category_list
        else:
            self.low = low
            self.high = high
            self.step = step
            self.log = log


class BaseHyperSearch(object):
    SEARCH_ALGORITHM = "Base"

    def __init__(self, direction: str, n_trial: int, path: ExpPath, seed: int):
        self.study_direction = direction
        self.n_trial = n_trial
        self.exp_path = path
        self.exp_seed = seed

    def optimal(self, exp, train_val_datamodule, search_params: List[SearchParam]):
        pass
