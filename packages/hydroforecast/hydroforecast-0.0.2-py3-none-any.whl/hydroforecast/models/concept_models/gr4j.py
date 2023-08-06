import numpy as np

from exp.hyper_search import SearchParam
from flux.baseflow import baseflow_3
from flux.evap import evap_11
from flux.saturation import saturation_4
from hydroforecast.models.concept_models import SimResult, HydroModel
from hydroforecast.models.concept_models.flux.percolation import percolation_3
from hydroforecast.models.concept_models.flux.recharge import recharge_2
from hydroforecast.models.concept_models.uh.unit_hydrograph import uh_1_half, uh_2_full, route, update_uh


class GR4J(HydroModel):
    # 对应 obj.JacobPattern
    jac_mat = np.array([[1, 1],
                        [1, 1]])
    # 对应 obj.StoreNames,这是水文模型计算中一些中间值，可以理解成土壤含水量，后面有S0就是他的初始值
    stores_series = [SimResult('S1'), SimResult('S2')]
    # 对应 obj.FluxNames, 这个是水文模型计算中一些产流值，比如蒸发，下渗，壤中流，径流等，即各模块的计算结果
    # 其中 对象设置了info信息，这里与obj.FluxGroups对应，obj.FluxGroups.Ea=[3, 5]代表总蒸发是根据fluxes_series中这几个参数计算的
    # 注意matlab的索引起始是1，所以在python应该减一，所以在2，4两个位置的info属性就是Evaporation
    fluxes_series = [SimResult('pn'), SimResult('en'), SimResult('ef', 'Evaporation'),
                     SimResult('ps'), SimResult('es', 'Evaporation'), SimResult('perc'),
                     SimResult('q9'), SimResult('q1'), SimResult('fr'), SimResult('fq'),
                     SimResult('qr'), SimResult('qt', 'Streamflow'), SimResult('ex')]
    # 这里还创建一个记录计算错误的对象
    error_series = SimResult('error')
    # 记录模型特有的参数，包括名称，上下限，默认值（在范围内即可），还有参数描述，这个在一个文档里,最好还可以加个单位
    model_params = [
        SearchParam('x1', 'float', low=1, high=2e3, default=10, param_describe='Maximum soil moisture storage', unit='mm'),
        SearchParam('x2', 'float', low=-20, high=20, default=10, param_describe='Subsurface water exchange', unit='mm·d-1'),
        SearchParam('x3', 'float', low=1, high=300, default=1, param_describe='Routing store depth', unit='mm'),
        SearchParam('x4', 'float', low=0.5, high=15, default=0, param_describe='Unit Hydrograph time base', unit='d'),
    ]

    def __init__(self, param_values):
        super().__init__(param_values)
        x1, x2, x3, x4 = param_values
        # 注意要在创建函数中创建单位线属性，每个模型不一样，有的不用创建
        self.uhs = (uh_1_half(x4, self.delta_t), uh_2_full(2 * x4, self.delta_t))

    @staticmethod
    def model_func(t, S, param_values, uhs, climate_inter, delta_t, return_fluxes=False):
        # stores
        S1, S2 = S

        # params
        x1, x2, x3, x4 = param_values

        # unit hydrographs and still-to-flow vectors
        uh_q9, uh_q1 = uhs

        # climate input
        P, Ep, T = climate_inter

        # fluxes functions
        flux_pn = np.max(P - Ep, 0)
        flux_en = np.max(Ep - P, 0)
        flux_ef = P - flux_pn
        flux_ps = saturation_4(S1, x1, flux_pn)
        flux_es = evap_11(S1, x1, flux_en)
        flux_perc = percolation_3(S1, x1)
        flux_q9 = route(.9 * (flux_pn - flux_ps + flux_perc), uh_q9)
        flux_q1 = route(.1 * (flux_pn - flux_ps + flux_perc), uh_q1)
        flux_fr = recharge_2(3.5, S2, x3, x2)
        flux_fq = flux_fr
        flux_qr = baseflow_3(S2, x3)
        flux_qt = flux_qr + np.max(flux_q1 + flux_fq, 0)
        # this flux is not included in original MARRMoT, but it is useful to calculate the water balance
        flux_ex = flux_fr + np.max(flux_q1 + flux_fq, 0) - flux_q1

        # stores ODEs
        dS1 = flux_ps - flux_es - flux_perc
        dS2 = flux_q9 + flux_fr - flux_qr

        dS = [dS1, dS2]
        fluxes = [flux_pn, flux_en, flux_ef, flux_ps, flux_es,
                  flux_perc, flux_q9, flux_q1, flux_fr, flux_fq,
                  flux_qr, flux_qt, flux_ex]

        # 这里是固定写法
        if return_fluxes:
            return dS, fluxes
        else:
            return dS

    def step(self, fluxes):
        # 部分模型需要重写step函数，用于单位线更新
        uh_q9, uh_q1 = self.uhs
        flux_pn, flux_ps, flux_prec = fluxes[0], fluxes[3], fluxes[5]
        uh_q9 = update_uh(uh_q9, 0.9 * (flux_pn - flux_ps + flux_prec))
        uh_q1 = update_uh(uh_q1, 0.1 * (flux_pn - flux_ps + flux_prec))
        self.uhs = (uh_q9, uh_q1)
