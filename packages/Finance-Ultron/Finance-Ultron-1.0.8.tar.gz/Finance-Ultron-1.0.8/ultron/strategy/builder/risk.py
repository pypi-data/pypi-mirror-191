# -*- coding: utf-8 -*-
import abc
import pandas as pd
import numpy as np
from ultron.strategy.builder.factor import ts_std_mean0, ts_grade, cross_section_demean_rank, cross_section_scale


def calc_portfolio_net_return(portfolio, return_, commission_rate=None):
    x = portfolio.shift(periods=1, freq=None) * return_
    turnover = portfolio.diff(periods=1) - x
    commission = turnover.abs() * commission_rate
    return x - commission


class LeverageRisk(metaclass=abc.ABCMeta):

    def __init__(self, **kwargs):
        self._risk_list = kwargs['risk_list']
        self._weight_list = kwargs['weight_list']
        self._risk_builder = kwargs['risk_builder']
        self._risk_control = kwargs['risk_control']

    def calc_ratio(self, factors, **kwargs):
        if self._risk_builder.lower() == 'riskweighted':
            rval = self.weighted_ratio(factors)
        else:
            raise NotImplementedError(
                'unknown leverage-risk-builder method {}'.format(
                    self._risk_builder))

        return rval

    def weighted_ratio(self, factors):
        risk_weight_list = self._weight_list
        risk_list = self._risk_list
        if isinstance(risk_weight_list, list):
            risk_weight_list = np.array(risk_weight_list)
            risk_weight_list = pd.DataFrame(risk_weight_list).T
        weights = cross_section_scale(risk_weight_list)
        weights = weights.values[0].tolist()

        index = factors[risk_list[0]].index
        columns = factors[risk_list[0]].columns
        rval = pd.DataFrame(0, index=index, columns=columns)
        for i, risk in enumerate(risk_list):
            rval += weights[i] * factors[risk]
        return rval

    def constrained_leverage_portfolio(self, portfolio):
        rval = portfolio.copy()
        ratio = rval.abs().sum(axis=1)
        ratio[ratio < 1] = 1
        rval = rval.div(ratio + 1e-16, axis=0)
        return rval

    def run(self, portfolio, factors=None):
        if self._risk_builder.lower() == 'riskweighted':
            risk_list = self._risk_list
            risk_weight_list = self._weight_list

            if len(risk_list) > 0:
                ratio = self.weighted_ratio(factors=factors)
                rval = portfolio * ratio
            else:
                rval = portfolio.copy()
        else:
            raise NotImplementedError(
                'unknown leverageRiskBuilder method {0:s}'.format(
                    self._risk_builder))

        if self._risk_control:
            rval = self.constrained_leverage_portfolio(rval)

        return rval


class ExposureRisk(metaclass=abc.ABCMeta):

    def __init__(self, **kwargs):
        self._commission_rate = kwargs['commission_rate']
        self._portfolio_exposure = kwargs['portfolio_exposure']
        self._max_portfolio = kwargs['max_portfolio']
        self._product_exposure = kwargs['product_exposure']
        self._max_product = kwargs['max_product']
        self._turnover_winnratio_winsize = kwargs['turnover_winnratio_winsize']

    def portfolio_constraint_positions(self, portfolio, exposure=None):
        if exposure is None:
            exposure = self._max_portfolio
        rval = portfolio.copy()
        index = portfolio[portfolio.sum(axis=1).abs() > exposure].index
        rval = portfolio.copy()
        index = portfolio[portfolio.sum(axis=1).abs() > exposure].index
        for idx in index:
            x = portfolio.loc[idx]
            pos = x[x > 0].sum()
            neg = x[x < 0].sum()
            expo = pos + neg

            if expo > 0:
                to_pos = -neg + exposure
                multiplier = to_pos / pos
                x[x > 0] = x[x > 0] * multiplier
            elif expo < 0:
                to_neg = -pos - exposure
                multiplier = to_neg / neg
                x[x < 0] = x[x < 0] * multiplier

            rval.loc[idx] = x

        return rval

    def product_constraint_positions(self, portfolio, max_exposure=None):
        if max_exposure is None:
            max_exposure = self._max_product
        lower = (-max_exposure)
        upper = max_exposure

        return portfolio.clip(lower=lower, upper=upper)

    def turnover_winning_weighted_positions(self,
                                            portfolios,
                                            returns,
                                            winsize=None,
                                            commission_rate=None):
        if winsize is None:
            winsize = self._turnover_winnratio_winsize

        if commission_rate is None:
            commission_rate = self._commission_rate

        data = dict()
        for key, portfolio in portfolios.items():
            turnover = portfolio.diff(
                periods=1) - portfolio.shift(periods=1, freq=None) * returns
            turnover = turnover.abs()
            turnover = turnover.rolling(window=winsize).sum()
            return_net = calc_portfolio_net_return(
                portfolio, returns, commission_rate).sum(axis=1, skipna=True)
            return_net_sign = return_net
            return_net_sign[return_net > 0] = 1
            return_net_sign[return_net < 0] = -1
            winning_ratio = return_net_sign.rolling(window=winsize).mean()
            data[key] = turnover / (winning_ratio + 1e-16)
        data = pd.DataFrame(data)
        universe = pd.DataFrame(True, index=data.index, columns=data.columns)
        rank = cross_section_demean_rank(data, universe)

        rval = pd.DataFrame(0, index=returns.index, columns=returns.columns)
        for col in data.columns:
            rval += portfolios[col].mul(rank[col], axis=0)

        return rval

    def run(self, portfolio, returns=None):
        rval = portfolio.copy()
        if self._portfolio_exposure:
            rval = self.portfolio_constraint_positions(portfolio=portfolio)
        if self._product_exposure:
            rval = self.product_constraint_positions(portfolio=portfolio)
        if returns is not None:
            rval = self.turnover_winning_weighted_positions(portfolio, returns)
        return rval


class TurnoverRisk(object):

    def __init__(self, **kwargs):
        self._grade_step = kwargs['grade_step']

    def portfolio_positions(self, portfolio):
        rval = portfolio.copy()
        if self._grade_step > 0:
            rval = ts_grade(rval, self._grade_step)
        return rval

    def run(self, portfolio):
        return self.portfolio_positions(portfolio=portfolio)


class VolatilityRisk(object):

    def __init__(self, **kwargs):
        self._volatility_winsize = kwargs['volatility_winsize']
        self._volatility_base = kwargs['volatility_base']
        self._upper_limit = kwargs['upper_limit']
        self._lower_limit = kwargs['lower_limit']

    def return_vol_ratio(self, portfolio, returns, is_portfolio=True):
        data = portfolio.copy()
        product_return_gross = data.shift(periods=1) * returns
        portfolio_return_gross = product_return_gross.sum(
            axis=1, skipna=True) if is_portfolio else product_return_gross
        portfolio_return_std = ts_std_mean0(portfolio_return_gross,
                                            self._volatility_winsize)
        rval = 1 / portfolio_return_std / self._volatility_base
        rval.iloc[0:self._volatility_winsize] = 1
        rval[rval >= self._upper_limit] = self._upper_limit
        rval[rval <= self._lower_limit] = self._lower_limit

        return rval

    def run(self, portfolio, returns, method):
        rval = portfolio.copy()
        if method == 'portfolio':
            ratio = self.return_vol_ratio(portfolio=portfolio,
                                          returns=returns,
                                          is_portfolio=True)
            rval = rval.mul(ratio, axis=0)
        elif method == 'product':
            ratio = self.return_vol_ratio(portfolio=portfolio,
                                          returns=returns,
                                          is_portfolio=False)
            rval *= ratio
        return rval


#def inverse_average_ratio(close, high, low, average_winsize):
#    true_range = ts_true_range(c=close, h=high, l=low)
#    alpha = 1 / average_winsize
#    avg_true_range = BaseOperator.ts_wma(data=true_range, alpha=alpha)

#    numerator = 1 / (avg_true_range / low)
#    denominator = numerator.sum(axis=1, skipna=True)
#    rval = numerator.div(denominator, axis=0)
#    return rval
