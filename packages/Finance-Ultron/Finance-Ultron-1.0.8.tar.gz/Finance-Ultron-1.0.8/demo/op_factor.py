import os, pdb, itertools, copy, datetime

os.environ['ULTRON_DATA'] = 'keim'

import random
import numpy as np
import pandas as pd
from ultron.env import *
from ultron.factor.genetic.geneticist.operators import custom_transformer
from ultron.factor.genetic.geneticist.engine import Engine

enable_example_env()

market_data = pd.read_csv(os.path.join(g_project_data, 'market_data.csv'),
                          index_col=0)
market_data['trade_date'] = pd.to_datetime(market_data['trade_date'])

tournament_size = 20  ### 初始种群数量
standard_score = 0.75  ### 筛选评估分

custom_params = {
    'tournament_size': tournament_size,
    'standard_score': standard_score,
    'rootid': 'ultron10001'
}


def next_returs_impl(price_data, key, name):
    price_tb = price_data[key].unstack()
    price_tb.fillna(method='pad', inplace=True)
    return_tb = np.log(price_tb.shift(-1) / price_tb)
    return_tb = return_tb.replace([np.inf, -np.inf], np.nan)
    return_tb = return_tb.stack().reindex(price_data.index)
    return_tb.name = name
    return return_tb


next_rets = next_returs_impl(market_data.set_index(['trade_date', 'code']),
                             'closePrice', 'nxt1_ret').reset_index()
next_rets['trade_date'] = pd.to_datetime(next_rets['trade_date'])

sel_factor = pd.read_csv(os.path.join(g_project_data, 'sel_factor.csv'),
                         index_col=0)

total_data = pd.read_csv(os.path.join(g_project_data, 'factor.csv'),
                         index_col=0)
factor_data = total_data[['trade_date', 'code'] +
                         sel_factor['factor'].unique().tolist()]
factor_data['trade_date'] = pd.to_datetime(factor_data['trade_date'])

features = [
    col for col in factor_data.columns
    if col not in ['trade_date', 'code', 'inventory', 'profitratio']
]

total_data = factor_data.merge(next_rets, on=['trade_date', 'code'])


def save_model(gen, rootid, best_programs, custom_params):
    pdb.set_trace()
    print('0--->')


def evaluation(factor_data, total_data, factor_sets, custom_params,
               default_value):
    returns = total_data[['trade_date', 'code', 'nxt1_ret']]
    factor_data = factor_data.reset_index()
    dt = factor_data.merge(returns, on=['trade_date', 'code'])
    factor_ic = dt.groupby(['trade_date']).apply(lambda x: x[
        ['transformed', 'nxt1_ret']].corr(method='spearman').values[0, 1])
    ic = factor_ic.mean()
    return abs(ic)


operators_sets = [
    'MA', 'MADecay', 'MMAX', 'MARGMAX', 'MMIN', 'MARGMIN', 'MRANK',
    'MQUANTILE', 'MSUM', 'MVARIANCE', 'MSTD', 'RSI', 'DELTA', 'SHIFT', 'MCORR'
]
operators_sets = custom_transformer(operators_sets)

gentic = Engine(population_size=10,
                tournament_size=3,
                init_depth=10,
                generations=1000,
                n_jobs=1,
                stopping_criteria=100,
                p_crossover=0.1,
                p_point_mutation=0.5,
                p_subtree_mutation=0.1,
                p_hoist_mutation=0.1,
                p_point_replace=0.1,
                rootid=custom_params['rootid'],
                factor_sets=features,
                standard_score=standard_score,
                operators_set=operators_sets,
                backup_cycle=20,
                convergence=0.002,
                fitness=evaluation,
                save_model=save_model,
                custom_params=custom_params)

gentic.train(total_data=total_data)