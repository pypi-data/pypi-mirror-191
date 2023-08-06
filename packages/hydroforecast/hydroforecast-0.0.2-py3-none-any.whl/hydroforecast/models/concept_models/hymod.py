from typing import Dict

import numpy as np

from hydroforecast.models.concept_models.flux.baseflow import baseflow_1
from hydroforecast.models.concept_models.flux.evap import evap_7
from hydroforecast.models.concept_models.flux.saturation import saturation_2
from hydroforecast.models.concept_models.flux.split import split_1
from hydroforecast.models.concept_models import SimResult, HydroModel
from hydroforecast.optimization import SearchParam


class HYMOD(HydroModel):
    jac_mat = np.array([[1, 0, 0, 0, 0],
                        [1, 1, 0, 0, 0],
                        [0, 1, 1, 0, 0],
                        [0, 0, 1, 1, 0],
                        [1, 0, 0, 0, 1]])
    stores_series = [SimResult('S1'), SimResult('S2'), SimResult('S3'), SimResult('S4'), SimResult('S5')]
    fluxes_series = [SimResult('ea', 'Evaporation'), SimResult('pe'), SimResult('pf'), SimResult('ps'),
                     SimResult('qf1'),
                     SimResult('qf2'), SimResult('qf3', 'Streamflow'), SimResult('qs', 'Streamflow')]
    error_series = SimResult('error')

    model_params = [
        SearchParam('s_max', 'float', low=1, high=2e3, default=10),
        SearchParam('b', 'float', low=0, high=20, default=10),
        SearchParam('a', 'float', low=0, high=1, default=0.5),
        SearchParam('kf', 'float', low=0, high=1, default=0.5),
        SearchParam('ks', 'float', low=0, high=1, default=0.5),
    ]

    @staticmethod
    def model_func(t, S, param_values, uhs, climate_inter, delta_t, return_fluxes=False):
        S1, S2, S3, S4, S5 = S
        s_max, b, a, kf, ks = tuple([v for v in param_values.values()]) \
            if isinstance(param_values, Dict) else param_values
        P, Ep, T = climate_inter
        # fluxes functions
        flux_ea = evap_7(S1, s_max, Ep, delta_t)
        flux_pe = saturation_2(S1, s_max, b, P)
        flux_pf = split_1(a, flux_pe)
        flux_ps = split_1(1 - a, flux_pe)
        flux_qf1 = baseflow_1(kf, S2)
        flux_qf2 = baseflow_1(kf, S3)
        flux_qf3 = baseflow_1(kf, S4)
        flux_qs = baseflow_1(ks, S5)

        # stores ODEs
        dS1 = P - flux_ea - flux_pe
        dS2 = flux_pf - flux_qf1
        dS3 = flux_qf1 - flux_qf2
        dS4 = flux_qf2 - flux_qf3
        dS5 = flux_ps - flux_qs

        dS = [dS1, dS2, dS3, dS4, dS5]
        fluxes = [flux_ea, flux_pe, flux_pf, flux_ps, flux_qf1, flux_qf2, flux_qf3, flux_qs]
        if return_fluxes:
            return dS, fluxes
        else:
            return dS
