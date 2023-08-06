# -*- encoding:utf-8 -*-
"""
股价的标准差及其信赖区间，从而确定股价的波动范围及未来走势，利用波带显示股价的安全高低价位，因而也被称为布林带。
其上下限范围不固定，随股价的滚动而变化。布林指标和麦克指标MIKE一样同属路径指标，股价波动在上限和下限的区间之内，
这条带状区的宽窄，随着股价波动幅度的大小而变化，股价涨跌幅度加大时，带状区变宽，涨跌幅度狭小盘整时，带状区则变窄

计算公式
中轨线=N日的移动平均线
上轨线=中轨线+nb_dev * N日的移动标准差
下轨线=中轨线－nb_dev * N日的移动标准差
（nb_dev为参数，可根据股票的特性来做相应的调整，一般默为2）
"""

import numpy as np
import pandas as pd

from ultron.ump.indicator.base import g_calc_type, ECalcType
from ultron.ump.core.helper import pd_rolling_mean, pd_rolling_std


def _calc_boll_from_ta(prices, time_period=20, nb_dev=2):
    """
    使用talib计算boll, 即透传talib.BBANDS计算结果
    :param prices: 收盘价格序列，pd.Series或者np.array
    :param time_period: boll的N值默认值20，int
    :param nb_dev: boll的nb_dev值默认值2，int
    :return: tuple(upper, middle, lower)
    """
    import talib
    if isinstance(prices, pd.Series):
        prices = prices.values

    upper, middle, lower = talib.BBANDS(prices,
                                        timeperiod=time_period,
                                        nbdevup=nb_dev,
                                        nbdevdn=nb_dev,
                                        matype=0)

    return upper, middle, lower


def _calc_boll_from_pd(prices, time_period=20, nb_dev=2):
    """
    通过boll公式手动计算boll
    :param prices: 收盘价格序列，pd.Series或者np.array
    :param time_period: boll的N值默认值20，int
    :param nb_dev: boll的nb_dev值默认值2，int
    :return: tuple(upper, middle, lower)
    """
    # 中轨线 = N日的移动平均线
    middle = pd_rolling_mean(prices,
                             window=time_period,
                             min_periods=time_period)
    # N日的移动标准差
    n_std = pd_rolling_std(prices, window=20, center=False)
    # 上轨线=中轨线+nb_dev * N日的移动标准差
    upper = middle + nb_dev * n_std
    # 下轨线 = 中轨线－nb_dev * N日的移动标准差
    lower = middle - nb_dev * n_std

    # noinspection PyUnresolvedReferences
    return upper.values, middle.values, lower.values


"""通过在ABuNDBase中尝试import talib来统一确定指标计算方式, 外部计算只应该使用calc_boll"""
calc_boll = _calc_boll_from_pd if g_calc_type == ECalcType.E_FROM_PD else _calc_boll_from_ta
