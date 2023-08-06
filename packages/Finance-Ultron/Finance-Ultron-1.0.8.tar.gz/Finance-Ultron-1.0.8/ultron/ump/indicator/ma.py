# -*- encoding:utf-8 -*-
"""
    移动平均线，Moving Average，简称MA，原本的意思是移动平均，由于我们将其制作成线形，所以一般称之为移动平均线，简称均线。
    它是将某一段时间的收盘价之和除以该周期。 比如日线MA5指5天内的收盘价除以5 。
    移动平均线是由著名的美国投资专家Joseph E.Granville（葛兰碧，又译为格兰威尔）于20世纪中期提出来的。
    均线理论是当今应用最普遍的技术指标之一，它帮助交易者确认现有趋势、判断将出现的趋势、发现过度延生即将反转的趋势
"""

from collections import Iterable
import pandas as pd
from enum import Enum
from ultron.ump.indicator.base import g_calc_type, ECalcType
from ultron.ump.core.helper import pd_rolling_mean, pd_ewm_mean
from ultron.ump.core.fixes import six
from ultron.kdutils.decorator import catch_error


class EMACalcType(Enum):
    """计算移动移动平均使用的方法"""
    """简单移动平均线"""
    E_MA_MA = 0
    """加权移动平均线"""
    E_MA_EMA = 1


# noinspection PyUnresolvedReferences
def _calc_ma_from_ta(prices, time_period=10, from_calc=EMACalcType.E_MA_MA):
    """
    使用talib计算ma，即透传talib.MA or talib.EMA计算结果
    :param prices: 收盘价格序列，pd.Series或者np.array
    :param time_period: 移动平均的N值，int
    :param from_calc: EMACalcType enum对象，移动移动平均使用的方法
    """

    import talib
    if isinstance(prices, pd.Series):
        prices = prices.values

    if from_calc == EMACalcType.E_MA_MA:
        ma = talib.MA(prices, timeperiod=time_period)
    else:
        ma = talib.EMA(prices, timeperiod=time_period)
    return ma


def _calc_ma_from_pd(prices, time_period=10, from_calc=EMACalcType.E_MA_MA):
    """
    通过pandas计算ma或者ema
    :param prices: 收盘价格序列，pd.Series或者np.array
    :param time_period: 移动平均的N值，int
    :param from_calc: EMACalcType enum对象，移动移动平均使用的方法
    """

    if isinstance(prices, pd.Series):
        prices = prices.values

    if from_calc == EMACalcType.E_MA_MA:
        ma = pd_rolling_mean(prices,
                             window=time_period,
                             min_periods=time_period)
    else:
        ma = pd_ewm_mean(prices, span=time_period, min_periods=time_period)
    return ma


def calc_ma_from_prices(prices,
                        time_period=10,
                        min_periods=None,
                        from_calc=EMACalcType.E_MA_MA):
    """
    通过pandas计算ma或者ema, 添加min_periods参数
    :param prices: 收盘价格序列，pd.Series或者np.array
    :param time_period: 移动平均的N值，int
    :param min_periods: int，默认None则使用time_period
    :param from_calc: EMACalcType enum对象，移动移动平均使用的方法
    """

    if isinstance(prices, pd.Series):
        prices = prices.values

    min_periods = time_period if min_periods is None else min_periods
    if from_calc == EMACalcType.E_MA_MA:
        ma = pd_rolling_mean(prices,
                             window=time_period,
                             min_periods=min_periods)
    else:
        ma = pd_ewm_mean(prices, span=time_period, min_periods=min_periods)
    return ma


"""通过在ABuNDBase中尝试import talib来统一确定指标计算方式, 外部计算只应该使用calc_ma"""
calc_ma = _calc_ma_from_pd if g_calc_type == ECalcType.E_FROM_PD else _calc_ma_from_ta
