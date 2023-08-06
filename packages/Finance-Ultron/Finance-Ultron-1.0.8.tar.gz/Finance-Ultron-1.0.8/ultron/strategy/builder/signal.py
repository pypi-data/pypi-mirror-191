# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from ultron.strategy.builder.factor import *
from ultron.strategy.builder.universe import Universe


def calc_weighted_signal(signals, factor_list, factor_weight):
    index = signals[list(signals.keys())[0]].index
    columns = signals[list(signals.keys())[0]].columns

    weights = factor_weight

    rval = pd.DataFrame(0, index=index, columns=columns)
    for i, strategy in enumerate(factor_list):
        rval += weights[i] * signals[strategy]
    return rval


def calc_1k_signal(signals, factor_list, factor_weight, oneover_k_equal=True):
    if not oneover_k_equal:
        weights = factor_weight
    else:
        weights = len(factor_list) * [1]

    index = signals[list(signals.keys())[0]].index
    columns = signals[list(signals.keys())[0]].columns

    rval = pd.DataFrame(0, index=index, columns=columns)
    for i, strategy in enumerate(factor_list):
        score = signals[strategy]
        score.fillna(0, inplace=True)
        score = np.sign(score)
        rval += weights[i] * score

    # nominal invest capital scale: 50% long, 50% short
    pos = rval.copy()
    pos[pos < 0] = np.nan
    pos.fillna(0, inplace=True)
    pos = pos.div(np.sum(pos, axis=1) + 1e-16, axis=0) * .5
    neg = rval.copy()
    neg[neg > 0] = np.nan
    neg.fillna(0, inplace=True)
    neg = neg.div(np.sum(neg, axis=1) + 1e-16, axis=0) * .5

    rval = pos + neg
    return rval


def calc_composite_signal(signals,
                          factor_list,
                          factor_weight,
                          composite_equal=True):
    if not composite_equal:
        weights = factor_weight
    else:
        weights = len(factor_weight) * [1]

    index = signals[list(signals.keys())[0]].index
    columns = signals[list(signals.keys())[0]].columns

    rval = pd.DataFrame(0, index=index, columns=columns)
    for i, strategy in enumerate(factor_list):
        score = signals[strategy]
        score.fillna(0, inplace=True)
        score = np.sign(score)
        rval += weights[i] * score

    # calc target position weights
    rval = rval.div(rval.abs().sum(axis=1) + 1e-16, axis=0)
    return rval


def calc_factors_score_signal(signals,
                              factor_list,
                              factor_weight,
                              investment_ratio=0.4):

    def get_nth_largest_value(df, n):
        argout = df.apply(lambda x: x.nlargest(n).values[-1], axis=1)
        return argout

    def get_nth_smallest_value(df, n):
        argout = df.apply(lambda x: x.nsmallest(n).values[-1], axis=1)
        return argout

    weights = factor_weight

    index = signals[list(signals.keys())[0]].index
    columns = signals[list(signals.keys())[0]].columns

    rval = pd.DataFrame(0, index=index, columns=columns)
    for i, strategy in enumerate(factor_list):
        score = cross_section_rank(signals[strategy])
        rval += weights[i] * score

    nrow, ncol = rval.shape
    count = rval.count(axis=1)
    num = count * investment_ratio  #self.signalMultiFactorsScoreInvestmentRatio
    num = num.round(0)
    num = int(num.tolist()[-1])

    i0 = count[count >= num * 2].index.tolist()[0]

    # upper part
    bnd = pd.Series(np.nan, index=count.index)
    bnd[i0:] = get_nth_largest_value(rval[i0:], num)
    bnd = bnd.repeat(ncol).values.reshape((nrow, ncol))
    pos = rval.copy()
    pos[pos < bnd] = np.nan
    pos.fillna(0, inplace=True)

    # lower part
    bnd = pd.Series(np.nan, index=count.index)
    bnd[i0:] = get_nth_smallest_value(rval[i0:], num)
    bnd = bnd.repeat(ncol).values.reshape((nrow, ncol))
    neg = rval.copy()
    neg[neg > bnd] = np.nan
    neg.fillna(0, inplace=True)

    rval = np.sign(pos) - np.sign(neg)
    rval = rval.div(rval.abs().sum(axis=1) + 1e-16, axis=0)
    return rval


def build_qs_signal(data,
                    split_strategy_type,
                    bound,
                    winsize,
                    rank,
                    upper,
                    lower,
                    zscore_normalization=True,
                    equal_weighted=True,
                    nominal_invest_weight=True,
                    qs_row_scale=True):
    universe = Universe.all(data)
    if zscore_normalization:
        data = data.copy()
        data = ts_zscore_normalization(data=data, bound=bound, winsize=winsize)
    upp = qs_percentile(data, universe, (upper - 1) / rank, upper / rank)
    upp.fillna(0, inplace=True)
    upp = abs(upp)

    lop = qs_percentile(data, universe, (lower - 1) / rank, lower / rank)
    lop.fillna(0, inplace=True)
    lop = abs(lop)

    if equal_weighted:
        upp = np.sign(upp)
        lop = np.sign(lop)
    rval = upp - lop

    if nominal_invest_weight:
        weights = cross_section_universe_equal(universe)
    else:
        weights = pd.DataFrame(1, index=data.index, columns=data.columns)
    rval = rval * weights

    if qs_row_scale:
        rval = cross_section_scale(rval)
    rval[~universe] = np.nan
    return rval


def build_cs_signal(data,
                    bound,
                    winsize,
                    zscore_normalization=True,
                    equal_weighted=True):
    universe = Universe.all(data)
    if zscore_normalization:
        data = ts_zscore_normalization(data=data, bound=bound, winsize=winsize)
    rval = cross_section_demean_rank(data, universe=universe)
    if equal_weighted:
        rval = np.sign(rval)
    rval = cross_section_nan_scale(rval)
    return rval


def build_ts_signal(data,
                    bound,
                    winsize,
                    zscore_normalization=True,
                    nominal_invest_weight=True,
                    ts_row_scale=True):
    universe = Universe.all(data)
    if zscore_normalization:
        x = ts_zscore_normalization(data=data, bound=bound, winsize=winsize)
    else:
        x = data.copy()

    if nominal_invest_weight:
        weights = cross_section_universe_equal(universe=universe)
    else:
        weights = pd.DataFrame(data=np.nan,
                               index=universe.index,
                               columns=universe.columns)
        ones = pd.DataFrame(data=1.0,
                            index=universe.index,
                            columns=universe.columns)
        weights[universe] = ones[universe]

    rval = x * weights
    if ts_row_scale:
        rval = cross_section_scale(rval)
    return rval