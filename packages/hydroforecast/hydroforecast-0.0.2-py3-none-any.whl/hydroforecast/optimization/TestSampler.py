from typing import Any, Dict

from optuna import Study
from optuna.distributions import BaseDistribution
from optuna.samplers import BaseSampler
from optuna.trial import FrozenTrial


class SceuaSampler(BaseSampler):
    def infer_relative_search_space(self, study: Study, trial: FrozenTrial) -> Dict[str, BaseDistribution]:
        pass

    def sample_relative(self, study: Study, trial: FrozenTrial, search_space: Dict[str, BaseDistribution]) -> Dict[
        str, Any]:
        pass

    def sample_independent(self, study: Study, trial: FrozenTrial, param_name: str,
                           param_distribution: BaseDistribution) -> Any:
        pass