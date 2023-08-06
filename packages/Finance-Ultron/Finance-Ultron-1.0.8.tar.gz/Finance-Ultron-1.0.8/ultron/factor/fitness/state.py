# -*- encoding:utf-8 -*-
"""
    横截面下因子评估方式--因子状态
"""
import pdb, functools
import numpy as np
import pandas as pd
from collections import namedtuple
from ultron.utilities.logger import kd_logger
from ultron.kdutils.progress import Progress


class StateTuple(
        namedtuple('StateTuple',
                   ('mean', 'median', 'std', 'max', 'min', 'nanr', 'zeror'))):
    __slots__ = ()

    def __repr__(self):
        return "\nmean:{}\nmedian:{}\nstd:{}\nmax:{}\nmin:{}\nnanr:{}\nzeror:{}".format(
            self.mean, self.median, self.std, self.max, self.min, self.nanr,
            self.zeror)


def valid_check(func):
    """检测度量的输入是否正常，非正常显示info，正常继续执行被装饰方法"""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.valid:
            return func(self, *args, **kwargs)
        else:
            kd_logger.info('metrics input is invalid or zero order gen!')

    return wrapper


class State(object):

    @classmethod
    def general(cls, factors, dummy, show_log=True):
        return cls(factors, dummy, show_log).fit_state()

    def __init__(self, factors, dummy=None, show_log=True):
        self.valid = False
        self.factors = factors
        self.dummy = dummy
        self.show_log = show_log
        if self.factors is not None and self.dummy is not None:
            self.valid = True

    @valid_check
    def fit_state(self):
        total_count = np.nansum(self.dummy.values)
        factors_dummy = self.factors.values * self.dummy.values

        nan_mean = np.nanmean(factors_dummy)
        nan_median = np.nanmedian(factors_dummy)
        nan_std = np.nanstd(factors_dummy)
        nan_max = np.nanmax(factors_dummy)
        nan_min = np.nanmin(factors_dummy)

        nanr = 1 - np.sum(abs(factors_dummy) >= 0) / total_count
        zeror = np.sum(factors_dummy == 0) / total_count
        return StateTuple(mean=nan_mean,
                          median=nan_median,
                          std=nan_std,
                          max=nan_max,
                          min=nan_min,
                          nanr=nanr,
                          zeror=zeror)
