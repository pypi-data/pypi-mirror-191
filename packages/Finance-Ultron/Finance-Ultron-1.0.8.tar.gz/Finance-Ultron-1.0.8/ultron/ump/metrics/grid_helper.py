# -*- encoding:utf-8 -*-
"""
    组合参数辅助模块
"""

import copy
from itertools import product
from ultron.ump.metrics.grid_search import ParameterGrid

# TODO 使用enum代替K常量
# 代表买因子参数组合
K_GEN_FACTOR_PARAMS_BUY = 0
# 代表卖因子参数组合
K_GEN_FACTOR_PARAMS_SELL = 1


def gen_factor_grid(type_param, factors, need_empty_sell=False):
    """
    :param type_param: grid目标，为K_GEN_FACTOR_PARAMS_BUY或K_GEN_FACTOR_PARAMS_SELL需要重构
    :param factors: 可迭代序列，元素为因子dict 如：
                    {'class': [AbuFactorBuyBreak], 'xd': [42]}, {'class': [AbuFactorBuyBreak],'xd': [60]}
    :param need_empty_sell: 只针对卖出因子组合添加一个完全不使用任何卖出因子的组合
    :return: 返回因子dict的组合参数序列
    """

    # 通过ParameterGrid将factor包装，即通过ParameterGrid将dict对象product(*values)，详阅读ParameterGrid
    grid_params = [ParameterGrid(factor) for factor in factors]
    # 进行product调用ParameterGrid__iter__进行product(*values)
    factor_params = product(*grid_params)
    factor_params = [list(pd_cls) for pd_cls in factor_params]

    if len(factors) > 1:
        # 把单独一个factor的加进去
        for grid_single in grid_params:
            for single in grid_single:
                factor_params.append([single])
    if need_empty_sell and type_param == K_GEN_FACTOR_PARAMS_SELL:
        # 只有sell的factor要加个空的，买的因子要是全空就没办法玩了
        factor_params.append([])  # 最后加一个完全不使用因子的

    return factor_params