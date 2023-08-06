# -*- encoding:utf-8 -*-
"""
    相关性降维
"""
import pdb
import numpy as np
from enum import Enum
from ultron.utilities.logger import kd_logger
from ultron.kdutils.progress import Progress
from ultron.ump.similar.corrcoef import corr_xy, corr_matrix, ECoreCorrType


class FCorrType(Enum):
    """
        FCorrType:因子相关性计算
    """
    """横截面相关系数计算"""
    F_CS_CORR = 'cs_corr'
    """时序相关系数计算"""
    F_TS_CORR = 'ts_corr'


class Corrcoef(object):

    def __init__(self, features=None, thresh=0.7, method='squares'):
        self._features = features
        self._thresh = thresh
        self._method = method
        self._filter = []

    def _corr_xy(self, x, y, similar_type, **kwargs):
        return corr_xy(x, y, similar_type=similar_type, **kwargs)

    def _ts_corr(self, factors_data, similar_type, **kwargs):
        grouped = factors_data.set_index(['trade_date'
                                          ]).groupby(level=['trade_date'])
        p = 0
        with Progress(len(self._features) - 1, 0, 'TS CORR') as pg:
            for i in range(0, len(self._features) - 1):
                p += 1
                for j in range(1, len(self._features)):
                    x_col = self._features[i]
                    y_col = self._features[j]
                    if x_col in self._filter or y_col in self._filter or x_col == y_col:
                        continue
                    res = []
                    for k, g in grouped:
                        corr = corr_xy(g[x_col], g[y_col], similar_type,
                                       **kwargs)
                        res.append(corr)
                    corr_mean = np.array(res).mean()
                    kd_logger.info("{0},{1} corr:{2}".format(
                        x_col, y_col, corr_mean))
                    if abs(corr_mean) > self._thresh:
                        self._filter.append(y_col)
                pg.show(p)

    def _cs_corr(self, factors_data, similar_type, **kwargs):
        p = 0
        with Progress(len(self._features) - 1, 0, 'CS CORR') as pg:
            for i in range(0, len(self._features) - 1):
                p += 1
                for j in range(1, len(self._features)):
                    x_col = self._features[i]
                    y_col = self._features[j]
                    if x_col in self._filter or y_col in self._filter or x_col == y_col:
                        continue
                    corr = self._corr_xy(factors_data[x_col],
                                         factors_data[y_col], similar_type,
                                         **kwargs)
                    kd_logger.info("{0},{1} corr:{2}".format(
                        x_col, y_col, corr))
                    if abs(corr) > self._thresh:
                        self._filter.append(y_col)
                pg.show(p)

    def run(self, factors_data, similar_type, **kwargs):
        if self._method == FCorrType.F_CS_CORR:
            self._cs_corr(factors_data=factors_data,
                          similar_type=similar_type,
                          **kwargs)
        elif self._method == FCorrType.F_TS_CORR:
            self._ts_corr(factors_data=factors_data,
                          similar_type=similar_type,
                          **kwargs)
        return factors_data.drop(self._filter, axis=1)
