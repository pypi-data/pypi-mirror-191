# -*- encoding:utf-8 -*-
"""
ATR

ATR又称 Average true range平均真实波动范围，简称ATR指标，是由J.Welles Wilder 发明的，ATR指标主要是用来衡量市场波动的强烈度，
即为了显示市场变化率的指标。

计算方法：
1. TR=∣最高价-最低价∣，∣最高价-昨收∣，∣昨收-最低价∣中的最大值
2. 真实波幅（ATR）= MA(TR,N)（TR的N日简单移动平均）
3. 常用参数N设置为14日或者21日
"""

import pandas as pd
import numpy as np
from ultron.ump.core.helper import pd_ewm_mean
from ultron.kdutils import scaler as scaler_util
from ultron.ump.indicator.base import g_calc_type, ECalcType


def _calc_atr_from_ta(high, low, close, time_period=14):
    """
    使用talib计算atr，即透传talib.ATR计算结果
    :param high: 最高价格序列，pd.Series或者np.array
    :param low: 最低价格序列，pd.Series或者np.array
    :param close: 收盘价格序列，pd.Series或者np.array
    :param time_period: atr的N值默认值14，int
    :return: atr值序列，np.array对象
    """
    import talib
    if isinstance(high, pd.Series):
        high = high.values
    if isinstance(low, pd.Series):
        low = low.values
    if isinstance(close, pd.Series):
        close = close.values

    atr = talib.ATR(high, low, close, timeperiod=time_period)
    return atr


def _calc_atr_from_pd(high, low, close, time_period=14):
    """
    通过atr公式手动计算atr
    :param high: 最高价格序列，pd.Series或者np.array
    :param low: 最低价格序列，pd.Series或者np.array
    :param close: 收盘价格序列，pd.Series或者np.array
    :param time_period: atr的N值默认值14，int
    :return: atr值序列，np.array对象
    """
    if isinstance(close, pd.Series):
        # shift(1)构成昨天收盘价格序列
        pre_close = close.shift(1).values
    else:
        from scipy.ndimage.interpolation import shift
        # 也可以暂时转换为pd.Series进行shift
        pre_close = shift(close, 1)
    pre_close[0] = pre_close[1]

    if isinstance(high, pd.Series):
        high = high.values
    if isinstance(low, pd.Series):
        low = low.values

    # ∣最高价 - 最低价∣
    tr_hl = np.abs(high - low)
    # ∣最高价 - 昨收∣
    tr_hc = np.abs(high - pre_close)
    # ∣昨收 - 最低价∣
    tr_cl = np.abs(pre_close - low)
    # TR =∣最高价 - 最低价∣，∣最高价 - 昨收∣，∣昨收 - 最低价∣中的最大值
    tr = np.maximum(np.maximum(tr_hl, tr_hc), tr_cl)
    # （ATR）= MA(TR, N)（TR的N日简单移动平均）, 这里没有完全按照标准公式使用简单移动平均，使用了pd_ewm_mean，即加权移动平均
    atr = pd_ewm_mean(pd.Series(tr), span=time_period, min_periods=1)
    # 返回atr值序列，np.array对象
    return atr.values


"""通过在NDBase中尝试import talib来统一确定指标计算方式"""
calc_atr = _calc_atr_from_pd if g_calc_type == ECalcType.E_FROM_PD else _calc_atr_from_ta


def atr14(high, low, close):
    """
    通过high, low, close计算atr14序列值
    :param high: 最高价格序列，pd.Series或者np.array
    :param low: 最低价格序列，pd.Series或者np.array
    :param close: 收盘价格序列，pd.Series或者np.array
    :return: atr值序列，np.array对象
    """
    atr = calc_atr(high, low, close, 14)
    return atr


def atr21(high, low, close):
    """
    通过high, low, close计算atr21序列值
    :param high: 最高价格序列，pd.Series或者np.array
    :param low: 最低价格序列，pd.Series或者np.array
    :param close: 收盘价格序列，pd.Series或者np.array
    :return: atr值序列，np.array对象
    """
    atr = calc_atr(high, low, close, 21)
    return atr


def atr14_min(high, low, close):
    """
    确定常数阀值时使用，通过high, low, close计算atr14序列值，返回计算结果atr14序列中的最小值
    :param high: 最高价格序列，pd.Series或者np.array
    :param low: 最低价格序列，pd.Series或者np.array
    :param close: 收盘价格序列，pd.Series或者np.array
    :return: atr值序列，atr14序列中的最小值，float
    """
    _atr14 = atr14(high, low, close)
    _atr14 = pd.Series(_atr14)
    _atr14.fillna(method='bfill', inplace=True)
    _atr14 = _atr14.min()
    return _atr14


def atr14_max(high, low, close):
    """
    确定常数阀值时使用，通过high, low, close计算atr14序列值，返回计算结果atr14序列中的最大值
    :param high: 最高价格序列，pd.Series或者np.array
    :param low: 最低价格序列，pd.Series或者np.array
    :param close: 收盘价格序列，pd.Series或者np.array
    :return: atr值序列，atr14序列中的最大值，float
    """
    _atr14 = atr14(high, low, close)
    _atr14 = pd.Series(_atr14)
    _atr14.fillna(method='bfill', inplace=True)
    _atr14 = _atr14.max()
    return _atr14


def atr21_min(high, low, close):
    """
    确定常数阀值时使用，通过high, low, close计算atr21序列值，返回计算结果atr21序列中的最小值
    :param high: 最高价格序列，pd.Series或者np.array
    :param low: 最低价格序列，pd.Series或者np.array
    :param close: 收盘价格序列，pd.Series或者np.array
    :return: atr值序列，atr21序列中的最小值，float
    """
    _atr21 = atr21(high, low, close)
    _atr21 = pd.Series(_atr21)
    _atr21.fillna(method='bfill', inplace=True)
    _atr21 = _atr21.min()
    return _atr21


def atr21_max(high, low, close):
    """
    确定常数阀值时使用，通过high, low, close计算atr21序列值，返回计算结果atr21序列中的最大值
    :param high: 最高价格序列，pd.Series或者np.array
    :param low: 最低价格序列，pd.Series或者np.array
    :param close: 收盘价格序列，pd.Series或者np.array
    :return: atr值序列，atr21序列中的最大值，float
    """
    _atr21 = atr21(high, low, close)
    _atr21 = pd.Series(_atr21)
    _atr21.fillna(method='bfill', inplace=True)
    _atr21 = _atr21.max()
    return _atr21