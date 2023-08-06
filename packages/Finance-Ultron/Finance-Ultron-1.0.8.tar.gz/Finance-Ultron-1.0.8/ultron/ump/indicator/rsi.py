# -*- encoding:utf-8 -*-
"""
相对强弱指数（RSI）是通过比较一段时期内的平均收盘涨数和平均收盘跌数来分析市场买沽盘的意向和实力，
从而作出未来市场的走势

计算方法：

具体计算实现可阅读代码中_calc_rsi_from_pd()的实现
1. 根据收盘价格计算价格变动可以使用diff()也可以使用pct_change()
2. 分别筛选gain交易日的价格变动序列gain，和loss交易日的价格变动序列loss
3. 分别计算gain和loss的N日移动平均
4. rs = gain_mean / loss_mean
5. rsi = 100 - 100 / (1 + rs)

"""
import numpy as np
import pandas as pd

from ultron.ump.indicator.base import g_calc_type, ECalcType
from ultron.kdutils import scaler as scaler_util
from ultron.kdutils.decorator import catch_error
from ultron.ump.core.helper import pd_rolling_mean
"""_calc_rsi_from_pd计算rs时使用gain，否则使用change"""
g_rsi_gain = True


# noinspection PyUnresolvedReferences
def _calc_rsi_from_ta(prices, time_period=14):
    """
    使用talib计算rsi, 即透传talib.RSI计算结果
    :param prices: 收盘价格序列，pd.Series或者np.array
    :param time_period: rsi的N日参数, 默认14
    """

    import talib
    if isinstance(prices, pd.Series):
        prices = prices.values
    rsi = talib.RSI(prices, timeperiod=time_period)
    return rsi


# noinspection PyTypeChecker
def _calc_rsi_from_pd(prices, time_period=14):
    """
    通过rsi公式手动计算rsi
    :param prices: 收盘价格序列，pd.Series或者np.array
    :param time_period: rsi的N日参数, 默认14
    """

    if not isinstance(prices, pd.Series):
        prices = pd.Series(prices)

    # 根据收盘价格计算价格变动可以使用diff()也可以使用pct_change()
    if g_rsi_gain:
        # 使用前后价格变动gain
        diff_price = prices.diff()
    else:
        # 使用前后价格变动change比例
        diff_price = prices.pct_change()
    diff_price[0] = 0

    # 分别筛选gain交易日的价格变动序列gain，和loss交易日的价格变动序列loss
    gain = np.where(diff_price > 0, diff_price, 0)
    loss = np.where(diff_price < 0, abs(diff_price), 0)
    # 分别计算gain和loss的N日移动平均
    gain_mean = pd_rolling_mean(gain, window=time_period)
    loss_mean = pd_rolling_mean(loss, window=time_period)
    # rsi = 100 - 100 / (1 +  gain_mean / loss_mean)
    rs = gain_mean / loss_mean
    rsi = 100 - 100 / (1 + rs)
    return rsi


"""通过在ABuNDBase中尝试import talib来统一确定指标计算方式, 外部计算只应该使用calc_rsi"""
calc_rsi = _calc_rsi_from_pd if g_calc_type == ECalcType.E_FROM_PD else _calc_rsi_from_ta