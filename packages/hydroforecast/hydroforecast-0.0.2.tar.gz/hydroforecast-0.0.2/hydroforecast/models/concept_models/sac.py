import numpy as np

from hydroforecast.models.concept_models import HydroModel, SimResult
from hydroforecast.models.concept_models.flux.baseflow import baseflow_1
from hydroforecast.models.concept_models.flux.evap import evap_1, evap_7
from hydroforecast.models.concept_models.flux.interflow import interflow_5
from hydroforecast.models.concept_models.flux.percolation import percolation_4
from hydroforecast.models.concept_models.flux.saturation import saturation_1
from hydroforecast.models.concept_models.flux.soilmoisture import soilmoisture_1, soilmoisture_2
from hydroforecast.models.concept_models.flux.split import split_1
from hydroforecast.optimization import SearchParam


def deficit_based_distribution(S1, S1max, S2, S2max):
    rd1 = (S1 - S1max) / S1max
    rd2 = (S2 - S2max) / S2max
    if rd1 + rd2 != 0:
        f1 = rd1 / (rd1 + rd2)
        f2 = rd2 / (rd1 + rd2)
    else:
        f1 = S1max / (S1max + S2max)
        f2 = S2max / (S1max + S2max)
    return f1, f2


class SAC(HydroModel):
    jac_mat = np.array([[1, 1, 0, 0, 0],
                        [1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1],
                        [0, 1, 1, 1, 1],
                        [0, 1, 1, 1, 1]])
    stores_series = [SimResult('S1'), SimResult('S2'), SimResult('S3'), SimResult('S4'), SimResult('S5')]
    fluxes_series = [SimResult('peff'), SimResult('pcfwp'), SimResult('pcfws'), SimResult('pc'),
                     SimResult('ru'), SimResult('euztw', 'Evaporation'), SimResult('rlp'), SimResult('rls'),
                     SimResult('euzfw', 'Evaporation'), SimResult('pctw'), SimResult('elztw', 'Evaporation'),
                     SimResult('twexu'), SimResult('twexl'), SimResult('twexlp'), SimResult('twexls'),
                     SimResult('qbfp', 'Streamflow'), SimResult('qbfs', 'Streamflow'), SimResult('qdir', 'Streamflow'),
                     SimResult('qsur', 'Streamflow'), SimResult('qint', 'Streamflow')]
    model_params = [
        SearchParam('pctim', 'float', low=0, high=1, default=0.9,
                    param_describe='Fraction impervious area'),
        SearchParam('smax', 'float', low=1, high=2000, default=20,
                    param_describe='Maximum total storage depth', unit='mm'),
        SearchParam('f1', 'float', low=0.005, high=0.995, default=0.5,
                    param_describe='fraction of smax that is Maximum upper zone tension water storage', unit='mm'),
        SearchParam('f2', 'float', low=0.005, high=0.995, default=0.5,
                    param_describe='fraction of smax-S1max that is Maximum upper zone free water storage', unit='mm'),
        SearchParam('kuz', 'float', low=0, high=1, default=0.5,
                    param_describe='Interflow runoff coefficient', unit='d^-1'),
        SearchParam('rexp', 'float', low=0, high=7, default=2,
                    param_describe='Base percolation rate non-linearity factor'),
        SearchParam('f3', 'float', low=0.005, high=0.995, default=0.5, unit='mm',
                    param_describe='fraction of smax-S1max-S2max that is Maximum lower zone tension water storage'),
        SearchParam('f4', 'float', low=0, high=10, default=5, unit='mm',
                    param_describe='fraction of smax-S1max-S2max-S3max that is' +
                                   ' Maximum lower zone primary free water storage'),
        SearchParam('pfree', 'float', low=0, high=1, default=0.5,
                    param_describe='Fraction of percolation directed to free water stores'),
        SearchParam('klzp', 'float', low=0, high=1, default=0.5,
                    param_describe='Primary baseflow runoff coefficient', unit='d^-1'),
        SearchParam('klzs', 'float', low=0, high=1, default=0.5,
                    param_describe='Supplemental baseflow runoff coefficient', unit='d^-1'),
    ]

    @staticmethod
    def model_func(t, S, param_values, uhs, climate_inter, delta_t, return_fluxes=False):
        S1, S2, S3, S4, S5 = S
        P, Ep, T = climate_inter
        pctim, smax, f1, f2, kuz, rexp, f3, f4, pfree, klzp, klzs = param_values
        # Derived parameters
        # Maximum upper zone tension water storage [mm]
        uztwm = f1 * smax
        # Maximum upper zone free water storage [mm]
        uzfwm = max(0.005 / 4, f2 * (smax - uztwm))
        # Maximum lower zone tension water storage [mm]
        lztwm = max(0.005 / 4, f3 * (smax - uztwm - uzfwm))
        # Maximum lower zone primary free water storage [mm]
        lzfwpm = max(0.005 / 4, f4 * (smax - uztwm - uzfwm - lztwm))
        # Maximum lower zone supplemental free water storage [mm]
        lzfwsm = max(0.005 / 4, (1 - f4) * (smax - uztwm - uzfwm - lztwm))
        # Base percolation rate [mm/d]
        pbase = lzfwpm * klzp + lzfwsm * klzs
        # Base percolation rate multiplication factor [-]: can return Inf, hence the min(10000,...)
        zperc = min(100000, (lztwm + lzfwsm * (1 - klzs)) / (lzfwsm * klzs + lzfwpm * klzp) + (lzfwpm * (1 - klzp)) / (
                lzfwsm * klzs + lzfwpm * klzp))

        # fluxes functions
        # Original formulation using MARRMoT fluxes is very slow on sacramento,
        # individual functions have been explicitly coded underneath.
        flux_qdir = split_1(pctim, P)
        flux_peff = split_1(1 - pctim, P)
        flux_ru = soilmoisture_1(S1, uztwm, S2, uzfwm)
        flux_euztw = evap_7(S1, uztwm, Ep, delta_t)
        flux_twexu = saturation_1(flux_peff, S1, uztwm)
        flux_qsur = saturation_1(flux_twexu, S2, uzfwm)
        flux_qint = interflow_5(kuz, S2)
        flux_euzfw = evap_1(S2, max(0, Ep - flux_euztw), delta_t)
        flux_pc = percolation_4(pbase, zperc, rexp, max(0, lztwm - S3) + max(0, lzfwpm - S4) + max(0, lzfwsm - S5),
                                lztwm + lzfwpm + lzfwsm, S2, uzfwm, delta_t)
        flux_pctw = split_1(1 - pfree, flux_pc)
        flux_elztw = evap_7(S3, lztwm, max(0, Ep - flux_euztw - flux_euzfw), delta_t)
        flux_twexl = saturation_1(flux_pctw, S3, lztwm)
        flux_twexlp = split_1(deficit_based_distribution(S4, lzfwpm, S5, lzfwsm), flux_twexl)
        flux_twexls = split_1(deficit_based_distribution(S5, lzfwsm, S4, lzfwpm), flux_twexl)
        flux_pcfwp = split_1(pfree * deficit_based_distribution(S4, lzfwpm, S5, lzfwsm), flux_pc)
        flux_pcfws = split_1(pfree * deficit_based_distribution(S5, lzfwsm, S4, lzfwpm), flux_pc)
        flux_rlp = soilmoisture_2(S3, lztwm, S4, lzfwpm, S5, lzfwsm)
        flux_rls = soilmoisture_2(S3, lztwm, S5, lzfwsm, S4, lzfwpm)
        flux_qbfp = baseflow_1(klzp, S4)
        flux_qbfs = baseflow_1(klzs, S5)

        # stores ODEs
        dS1 = flux_peff + flux_ru - flux_euztw - flux_twexu
        dS2 = flux_twexu - flux_euzfw - flux_qsur - flux_qint - flux_ru - flux_pc
        dS3 = flux_pctw + flux_rlp + flux_rls - flux_elztw - flux_twexl
        dS4 = flux_twexlp + flux_pcfwp - flux_rlp - flux_qbfp
        dS5 = flux_twexls + flux_pcfws - flux_rls - flux_qbfs

        # output
        dS = [dS1, dS2, dS3, dS4, dS5]
        fluxes = [flux_qdir, flux_peff, flux_ru, flux_euztw, flux_twexu,
                  flux_qsur, flux_qint, flux_euzfw, flux_pc, flux_pctw,
                  flux_elztw, flux_twexl, flux_twexlp, flux_twexls, flux_pcfwp,
                  flux_pcfws, flux_rlp, flux_rls, flux_qbfp, flux_qbfs]
        if return_fluxes:
            return dS, fluxes
        else:
            return dS
