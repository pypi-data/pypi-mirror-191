# -*- encoding:utf-8 -*-
"""
MACD

MACD称为指数平滑异动移动平均线，是从双指数移动平均线发展而来的，由快的加权移动均线（EMA12）减去慢的加权移动均线（EMA26）
得到DIF，再用DIF - (快线-慢线的9日加权移动均线DEA）得到MACD柱。MACD的意义和双移动平均线基本相同，即由快、慢均线的离散、
聚合表征当前的多空状态和股价可能的发展变化趋势，但阅读起来更方便。当MACD从负数转向正数，是买的信号。当MACD从正数转向负数，
是卖的信号。当MACD以大角度变化，表示快的移动平均线和慢的移动平均线的差距非常迅速的拉开，代表了一个市场大趋势的转变。

"""

import numpy as np
import pandas as pd

from ultron.ump.indicator.base import g_calc_type, ECalcType
from ultron.kdutils import scaler as scaler_util
from ultron.kdutils.decorator import catch_error
from ultron.ump.core.helper import pd_ewm_mean


# noinspection PyUnresolvedReferences
def _calc_macd_from_ta(price, fast_period=12, slow_period=26, signal_period=9):
    """
    使用talib计算macd, 即透传talib.MACD计算结果
    :param price: 收盘价格序列，pd.Series或者np.array
    :param fast_period: 快的加权移动均线线, 默认12，即EMA12
    :param slow_period: 慢的加权移动均线, 默认26，即EMA26
    :param signal_period: dif的指数移动平均线，默认9
    """

    import talib
    if isinstance(price, pd.Series):
        price = price.values

    dif, dea, bar = talib.MACD(price,
                               fastperiod=fast_period,
                               slowperiod=slow_period,
                               signalperiod=signal_period)
    return dif, dea, bar


def _calc_macd_from_pd(price, fast_period=12, slow_period=26, signal_period=9):
    """
    通过macd公式手动计算macd
    :param price: 收盘价格序列，pd.Series或者np.array
    :param fast_period: 快的加权移动均线线, 默认12，即EMA12
    :param slow_period: 慢的加权移动均线, 默认26，即EMA26
    :param signal_period: dif的指数移动平均线，默认9
    """

    if isinstance(price, pd.Series):
        price = price.values

    # 快的加权移动均线
    ewma_fast = pd_ewm_mean(price, span=fast_period)
    # 慢的加权移动均线
    ewma_slow = pd_ewm_mean(price, span=slow_period)
    # dif = 快线 - 慢线
    dif = ewma_fast - ewma_slow
    # dea = dif的9日加权移动均线
    dea = pd_ewm_mean(dif, span=signal_period)
    bar = (dif - dea)
    return dif, dea, bar


"""通过在NDBase中尝试import talib来统一确定指标计算方式"""
calc_macd = _calc_macd_from_pd if g_calc_type == ECalcType.E_FROM_PD else _calc_macd_from_ta
