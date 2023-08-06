# -*- encoding:utf-8 -*-
# 基础库导入

import os, sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath('../'))

from ultron.env import *
from ultron.ump.factor import FactorPreAtrNStop, FactorAtrNStop, FactorCloseAtrNStop, FactorBuyBreak

from ultron.ump.metrics import grid_helper as GridHelper
from ultron.ump.metrics.grid_search import GridSearch

enable_example_env()

stop_win_range = np.arange(2.0, 2.5, 0.5)
stop_loss_range = np.arange(0.5, 1, 0.5)

sell_atr_nstop_factor_grid = {
    'class': [FactorAtrNStop],
    'stop_loss_n': stop_loss_range,
    'stop_win_n': stop_win_range
}

print('FactorAtrNStop止盈参数stop_win_n设置范围:{}'.format(stop_win_range))
print('FactorAtrNStop止损参数stop_loss_n设置范围:{}'.format(stop_loss_range))

close_atr_range = np.arange(1.0, 1.5, 0.5)
pre_atr_range = np.arange(1.0, 1.5, 0.5)

sell_atr_pre_factor_grid = {
    'class': [FactorPreAtrNStop],
    'pre_atr_n': pre_atr_range
}

sell_atr_close_factor_grid = {
    'class': [FactorCloseAtrNStop],
    'close_atr_n': close_atr_range
}

print('暴跌保护止损参数pre_atr_n设置范围:{}'.format(pre_atr_range))
print('盈利保护止盈参数close_atr_n设置范围:{}'.format(close_atr_range))

sell_factors_product = GridHelper.gen_factor_grid(
    GridHelper.K_GEN_FACTOR_PARAMS_SELL, [
        sell_atr_nstop_factor_grid, sell_atr_pre_factor_grid,
        sell_atr_close_factor_grid
    ],
    need_empty_sell=True)

print('卖出因子参数共有{}种组合方式'.format(len(sell_factors_product)))
print('卖出因子组合0: 形式为{}'.format(sell_factors_product[0]))

sell_factors_product = GridHelper.gen_factor_grid(
    GridHelper.K_GEN_FACTOR_PARAMS_SELL, [
        sell_atr_nstop_factor_grid, sell_atr_pre_factor_grid,
        sell_atr_close_factor_grid
    ],
    need_empty_sell=True)

print('卖出因子参数共有{}种组合方式'.format(len(sell_factors_product)))
print('卖出因子组合0: 形式为{}'.format(sell_factors_product[0]))

buy_bk_factor_grid1 = {'class': [FactorBuyBreak], 'xd': [42]}

buy_bk_factor_grid2 = {'class': [FactorBuyBreak], 'xd': [60]}

buy_factors_product = GridHelper.gen_factor_grid(
    GridHelper.K_GEN_FACTOR_PARAMS_BUY,
    [buy_bk_factor_grid1, buy_bk_factor_grid2])

print('买入因子参数共有{}种组合方式'.format(len(buy_factors_product)))
print('买入因子组合形式为{}'.format(buy_factors_product))

read_cash = 1000000
choice_symbols = ['usAAPL', 'usBIDU', 'usFB', 'usTSLA']

#### 加载指数行情
pick_kl_pd_dict = {}

benchmark_kl_pd = pd.read_csv(os.path.join('data',
                                           'us.IXIC_20120723_20160726.csv'),
                              index_col=0)
benchmark_kl_pd.index = pd.to_datetime(benchmark_kl_pd.index)
benchmark_kl_pd.name = 'us_NYSE:.IXIC'

aaple_kl_pd = pd.read_csv(os.path.join('data', 'usAAPL_20140609_20160726.csv'),
                          index_col=0)
aaple_kl_pd.index = pd.to_datetime(aaple_kl_pd.index)
aaple_kl_pd.name = 'usAAPL'
pick_kl_pd_dict['usAAPL'] = aaple_kl_pd

bidu_kl_pd = pd.read_csv(os.path.join('data', 'usBIDU_20130726_20160726.csv'),
                         index_col=0)
bidu_kl_pd.index = pd.to_datetime(bidu_kl_pd.index)
bidu_kl_pd.name = 'usBIDU'
pick_kl_pd_dict['usBIDU'] = bidu_kl_pd

fb_kl_pd = pd.read_csv(os.path.join('data', 'usFB_20140723_20160726.csv'),
                       index_col=0)
fb_kl_pd.index = pd.to_datetime(fb_kl_pd.index)
fb_kl_pd.name = 'usFB'
pick_kl_pd_dict['usFB'] = fb_kl_pd

tsla_kl_pd = pd.read_csv(os.path.join('data', 'usTSLA_20130726_20160726.csv'),
                         index_col=0)
tsla_kl_pd.index = pd.to_datetime(tsla_kl_pd.index)
tsla_kl_pd.name = 'usTSLA'
pick_kl_pd_dict['usTSLA'] = tsla_kl_pd

grid_search = GridSearch(read_cash,
                         choice_symbols,
                         benchmark_kl_pd=benchmark_kl_pd,
                         buy_factors_product=buy_factors_product,
                         sell_factors_product=sell_factors_product)

#### 外部设置K线
grid_search.kl_pd_manager.set_pick_time(pick_kl_pd_dict)

grid_search.fit(n_jobs=1)