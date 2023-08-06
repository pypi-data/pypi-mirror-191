# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd


def qs_percentile(data, universe, lower, upper):
    # rval: of type pd.DataFrame
    rval = data.copy()
    nrow, ncol = rval.shape
    rval[~universe] = np.nan
    # qlow, qup: of type pd.Series
    qlow = rval.quantile(q=lower, axis=1)
    qup = rval.quantile(q=upper, axis=1)
    # qlow, qup: of type pd.DataFrame
    qlow = qlow.repeat(ncol).values.reshape((nrow, ncol))
    qlow = pd.DataFrame(qlow, index=rval.index, columns=rval.columns)
    qup = qup.repeat(ncol).values.reshape((nrow, ncol))
    qup = pd.DataFrame(qup, index=rval.index, columns=rval.columns)

    blo = rval >= qlow
    bup = rval <= qup
    idx = blo & bup
    rval[~idx] = np.nan
    return rval


def cross_section_universe_equal(universe):
    rval = universe.div(np.sum(universe, axis=1) + 1e-16, axis=0)
    return rval


def cross_section_nan_scale(data):
    data = data.copy()
    denominator = data.abs().sum(axis=1, skipna=True)
    rval = data.div(denominator, axis=0)
    return rval


def cross_section_rank(data):
    data = data.copy()
    rval = data.rank(axis=1,
                     method='average',
                     na_option='keep',
                     ascending=True,
                     pct=False)
    return rval


def cross_section_scale(data):
    data = data.copy()
    denominator = data.abs().sum(axis=1, skipna=True)
    rval = data.div(denominator, axis=0)
    rval.fillna(0, inplace=True)
    return rval


def cross_section_mean_deviation(data, universe):
    data = data.copy()
    data[~universe] = np.nan
    rval = data.subtract(data.mean(axis=1, skipna=True), axis=0)
    return rval


def cross_section_demean_rank(data, universe):
    data = data.copy()
    data[~universe] = np.nan
    rank = data.rank(axis=1,
                     method='average',
                     na_option='keep',
                     ascending=True,
                     pct=False)
    rval = cross_section_mean_deviation(rank, universe)
    return rval


def ts_grade(data, step):
    raw_in = data.copy()
    if isinstance(data, pd.Series):
        data = pd.DataFrame(data=data)
    nrow, ncol = data.shape
    x = data.copy()
    flag = x.isnull()
    x[flag] = 0
    x = x.values

    rval = np.full(data.shape, 0.0)
    for i in range(1, nrow):
        for j in range(ncol):
            multiple = x[i, j] / step
            multiple_round = np.round(multiple + 1e-16 * np.sign(multiple))
            multiple_ceil = np.ceil(multiple)
            if multiple_round != multiple and x[i, j] > rval[i - 1, j]:
                rval[i, j] = (multiple_ceil - 1) * step
            else:
                rval[i, j] = multiple_ceil * step
    if isinstance(raw_in, pd.DataFrame):
        rval = pd.DataFrame(data=rval,
                            index=raw_in.index,
                            columns=raw_in.columns)
    elif isinstance(raw_in, pd.Series):
        rval = pd.Series(data=rval.reshape(len(rval), ), index=raw_in.index)
    rval[flag] = np.nan
    return rval


def ts_delay(data, winsize):
    rval = data.shift(periods=winsize, freq=None, axis=0)
    return rval


def ts_true_high(c, hi):
    # c: close
    # hi: high
    c_delayed = ts_delay(c, 1)
    factor = np.maximum(c_delayed.values, hi.values)
    rval = pd.DataFrame(factor)
    rval.index = c.index
    rval.columns = c.columns
    return rval


def ts_true_low(c, lo):
    # c: close
    # lo: low
    c_delayed = ts_delay(c, 1)
    factor = np.minimum(c_delayed.values, lo.values)
    rval = pd.DataFrame(factor)
    rval.index = c.index
    rval.columns = c.columns
    return rval


def ts_true_range(c, hi, lo):

    true_high = ts_true_high(c, hi)
    true_low = ts_true_low(c, lo)
    rval = true_high - true_low
    return rval


def ts_std_mean0(data, winsize):
    rval = data.pow(2).rolling(window=winsize, center=False, axis=0).mean()
    rval = rval.pow(1 / 2)
    return rval


def ts_zscore_normalization(data, bound=None, winsize=None):

    def get_plus(ser):
        if sum(ser.isnull()) == 0:
            _plus = 0
        else:
            _plus = ser.index.get_loc(ser[ser.isnull()].index[-1]) + 1
        return _plus

    nrow, ncol = data.shape
    rval = np.full((nrow, ncol), np.nan)

    plus_series = data.apply(get_plus).tolist()
    for j, col in enumerate(data):
        plus = plus_series[j]
        if winsize + plus > nrow:
            continue

        x = data[col].values

        x_truncated = np.zeros_like(x)
        x_truncated[plus + 1:winsize + plus + 1] = x[plus + 1:winsize + plus +
                                                     1]

        std_ = np.zeros_like(x)

        for i in range(winsize + plus, nrow):
            if i == winsize + plus:
                val = x_truncated[i - winsize + 1:i + 1]
                std0 = np.sqrt(np.mean(val**2))
                val_x_outlier = val[np.abs(val) <=
                                    bound * std0]  # FIXME why not clip
                # val_x_outlier = np.clip(val, -bound * std0, bound * std0)
                std_x_outlier = np.sqrt(np.mean(val_x_outlier**2))

                threshold = bound * std_x_outlier
                np.clip(val, -threshold, threshold, val)

                std_[i] = np.sqrt(np.mean(val**2))
                x_truncated[i - winsize + 1:i + 1] = val
            else:
                std_m1 = std_[i - 1]
                if std_m1 == 0:
                    std_m1 = 1e-7
                x_truncated[i] = np.clip(x[i], -bound * std_m1, bound * std_m1)
                var_ = std_m1**2 * winsize - x_truncated[
                    i - winsize]**2 + x_truncated[i]**2

                if var_ < 0:
                    var_ = 0
                std_[i] = np.sqrt(var_ / winsize)

                rval[i, j] = x_truncated[i] / std_m1
    rval = rval / bound
    rval = pd.DataFrame(data=rval, index=data.index, columns=data.columns)
    return rval
