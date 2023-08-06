# -*- encoding:utf-8 -*-
from ultron.factor.fitness.metrics import Metrics


def metrics_fitness(factor_data, total_data, factor_sets, custom_params,
                    default_value):
    returns = total_data[['trade_date', 'code', 'nxt1_ret']]
    factor_data = factor_data.reset_index()
    data = factor_data.merge(returns, on=['trade_date', 'code'])
    data = data.set_index(['trade_date', 'code']).dropna(subset=['nxt1_ret'])
    factors_socre = data['transformed'].unstack()
    yield_score = data['nxt1_ret'].unstack()
    ms = Metrics(returns=yield_score, factors=factors_socre)
    evaluate_name = custom_params['evaluate']
    method_name = custom_params['method']
    result = ms.fit_metrics()
    fitness = float(
        result.__getattribute__(f"{evaluate_name}").__getattribute__(
            f"{method_name}"))
    return fitness, result
