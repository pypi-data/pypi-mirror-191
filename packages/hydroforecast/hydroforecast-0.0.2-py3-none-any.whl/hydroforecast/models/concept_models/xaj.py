import numpy as np

from hydroforecast.models.concept_models import HydroModel, SimResult
from hydroforecast.models.concept_models.flux.baseflow import baseflow_1
from hydroforecast.models.concept_models.flux.evap import evap_21
from hydroforecast.models.concept_models.flux.interflow import interflow_5
from hydroforecast.models.concept_models.flux.saturation import saturation_14, saturation_2
from hydroforecast.models.concept_models.flux.split import split_1
from hydroforecast.optimization import SearchParam


class XAJ(HydroModel):
    jac_mat = np.array([[1, 0, 0, 0],
                        [1, 1, 0, 0],
                        [0, 1, 1, 0],
                        [0, 1, 0, 1]])
    stores_series = [SimResult('S1'), SimResult('S2'), SimResult('S3'), SimResult('S4'), SimResult('S5')]
    fluxes_series = [
        SimResult('rb'), SimResult('pi'), SimResult('e', 'Evaporation'),
        SimResult('r'), SimResult('rs'), SimResult('ri'), SimResult('rg'),
        SimResult('qs', 'Streamflow'), SimResult('qi', 'Streamflow'), SimResult('qg', 'Streamflow')
    ]
    model_params = [
        SearchParam('aim', 'float', low=0, high=1, default=0.9,
                    param_describe='Fraction impervious area'),
        SearchParam('a', 'float', low=-0.49, high=0.49, default=0.2,
                    param_describe='Tension water distribution inflection parameter'),
        SearchParam('b', 'float', low=0, high=10, default=5,
                    param_describe='Tension water distribution shape parameter'),
        SearchParam('stot', 'float', low=1, high=2000, default=50,
                    param_describe='Total soil moisture storage (W+S)', unit='mm'),
        SearchParam('fwm', 'float', low=0.01, high=0.99, default=0.5,
                    param_describe='Fraction of Stot that is Wmax'),
        SearchParam('flm', 'float', low=0.01, high=0.99, default=0.5,
                    param_describe='Fraction of wmax that is LM'),
        SearchParam('c', 'float', low=0.01, high=0.99, default=0.5,
                    param_describe='Fraction of LM for second evaporation change'),
        SearchParam('ex', 'float', low=0, high=10, default=5,
                    param_describe='Free water distribution shape parameter'),
        SearchParam('ki', 'float', low=0, high=1, default=0.5,
                    param_describe='Free water interflow parameter', unit='d^-1'),
        SearchParam('kg', 'float', low=0, high=1, default=0.5,
                    param_describe='Free water groundwater parameter', unit='d^-1'),
        SearchParam('ci', 'float', low=0, high=1, default=0.5,
                    param_describe='Interflow time coefficient', unit='d^-1'),
        SearchParam('cg', 'float', low=0, high=1, default=0.5,
                    param_describe='Baseflow time coefficient', unit='d^-1'),
    ]

    @staticmethod
    def model_func(t, S, param_values, uhs, climate_inter, delta_t, return_fluxes=False):
        S1, S2, S3, S4 = S
        aim, a, b, stot, fwm, flm, c, ex, ki, kg, ci, cg = param_values
        P, Ep, T = climate_inter
        # Maximum tension water depth and Maximum free water depth
        wmax, smax = fwm * stot, (1 - fwm) * stot
        # Tension water threshold for evaporation change
        lm = flm * wmax

        # fluxes functions
        flux_rb = split_1(aim, P)
        flux_pi = split_1(1 - aim, P)
        flux_e = evap_21(lm, c, S1, Ep, delta_t)
        flux_r = saturation_14(a, b, S1, wmax, flux_pi)
        flux_rs = saturation_2(S2, smax, ex, flux_r)
        flux_ri = saturation_2(S2, smax, ex, S2 * ki)
        flux_rg = saturation_2(S2, smax, ex, S2 * kg)
        flux_qs = flux_rb + flux_rs
        flux_qi = interflow_5(ci, S3)
        flux_qg = baseflow_1(cg, S4)

        # stores ODEs
        dS1 = flux_pi - flux_e - flux_r
        dS2 = flux_r - flux_rs - flux_ri - flux_rg
        dS3 = flux_ri - flux_qi
        dS4 = flux_rg - flux_qg

        # output
        dS = [dS1, dS2, dS3, dS4]
        fluxes = [flux_rb, flux_pi, flux_e, flux_r, flux_rs, flux_ri, flux_rg, flux_qs, flux_qi, flux_qg]
        if return_fluxes:
            return dS, fluxes
        else:
            return dS
