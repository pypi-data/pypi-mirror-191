import pandas as pd

from hydroforecast.models.concept_models.xaj import XAJ

data = pd.read_csv(r'F:\pycharm\My Project\My Lib\hydrology-forecast\data\01013500_lump_p_pe_q.txt', header=None)
param_values = ()
XAJ()
