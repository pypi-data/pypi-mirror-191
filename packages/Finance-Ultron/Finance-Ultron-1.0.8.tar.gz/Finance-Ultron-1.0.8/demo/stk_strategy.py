# -*- coding: utf-8 -*-
import copy, pdb
import pandas as pd
import numpy as np
import ultron.factor.empyrical as empyrical
from ultron.utilities.logger import kd_logger
from ultron.strategy.executor.naive import NaiveExecutor
from ultron.factor.analysis.factor_analysis import er_portfolio_analysis
from ultron.factor.data.processing import factor_processing
from ultron.factor.data.standardize import standardize
from ultron.factor.data.winsorize import winsorize_normal
from ultron.optimize.model.linearmodel import ConstLinearModel
from ultron.optimize.constraints import LinearConstraints, \
    create_box_bounds, BoundaryType


class RunningSetting(object):

    def __init__(self,
                 lbound=None,
                 ubound=None,
                 weights_bandwidth=None,
                 rebalance_method='risk_neutral',
                 bounds=None,
                 neutralized_styles=None,
                 **kwargs):
        self.lbound = lbound
        self.ubound = ubound
        self.weights_bandwidth = weights_bandwidth
        self.rebalance_method = rebalance_method
        self.bounds = bounds
        self.neutralized_styles = neutralized_styles
        self.more_opts = kwargs

    '''
    def __repr__(self):
        str_bounds = ""
        for k, v in self.bounds.items():
            str_bounds += "\nname:{}:\nlower-direction:{},boundary:{},val:{}\nupper-direction:{},boundary:{},val:{}".format(
                k, v.lower.direction, v.lower.b_type, v.lower.val,
                v.upper.direction, v.upper.b_type, v.upper.val)

        return "lbound:{}\nubound:{}\nweights_bandwidth:{}\nrebalance_method:{}\nneutralized_styles:{}\nbounds:{}".format(
            self.lbound, self.ubound, self.weights_bandwidth,
            self.rebalance_method, self.neutralized_styles, str_bounds)
    '''


class Strategy(object):

    def __init__(self,
                 alpha_model,
                 features=None,
                 start_date=None,
                 end_date=None,
                 risk_model=None,
                 index_return=None,
                 total_data=None):

        self.start_date = start_date
        self.end_date = end_date
        self.index_return = index_return
        self.alpha_models = alpha_model
        self.risk_models = risk_model
        self.total_data = total_data
        self.featrues = features
        if self.total_data is not None:
            self.total_data['trade_date'] = pd.to_datetime(
                self.total_data['trade_date'])

    @staticmethod
    def _create_lu_bounds(running_setting, codes, benchmark_w):

        codes = np.array(codes)

        if running_setting.weights_bandwidth:
            lbound = np.maximum(
                0., benchmark_w - running_setting.weights_bandwidth)
            ubound = running_setting.weights_bandwidth + benchmark_w

        lb = running_setting.lbound
        ub = running_setting.ubound

        if lb or ub:
            if not isinstance(lb, dict):
                lbound = np.ones_like(benchmark_w) * lb
            else:
                lbound = np.zeros_like(benchmark_w)
                for c in lb:
                    lbound[codes == c] = lb[c]

                if 'other' in lb:
                    for i, c in enumerate(codes):
                        if c not in lb:
                            lbound[i] = lb['other']
            if not isinstance(ub, dict):
                ubound = np.ones_like(benchmark_w) * ub
            else:
                ubound = np.ones_like(benchmark_w)
                for c in ub:
                    ubound[codes == c] = ub[c]

                if 'other' in ub:
                    for i, c in enumerate(codes):
                        if c not in ub:
                            ubound[i] = ub['other']
        return lbound, ubound

    def prepare_backtest_models(self, features, weights=None):
        models = {}
        weights = dict(zip(
            features, [(1 / len(features))
                       for i in features])) if weights is None else weights
        total_data_groups = self.total_data.groupby('trade_date')
        alpha_model = ConstLinearModel(features=features, weights=weights)
        for ref_date, _ in total_data_groups:
            models[ref_date] = alpha_model
        self.alpha_models = models
        kd_logger.info("alpha models training finished ...")

    def _calculate_pos(self,
                       running_setting,
                       er,
                       data,
                       constraints,
                       benchmark_w,
                       lbound,
                       ubound,
                       risk_model,
                       current_position,
                       is_benchmark=0):
        more_opts = running_setting.more_opts
        try:
            target_pos, _ = er_portfolio_analysis(
                er=er,
                industry=data.industry_code.values,
                dx_return=None,
                constraints=constraints,
                detail_analysis=False,
                benchmark=benchmark_w,
                method=running_setting.rebalance_method,
                lbound=lbound,
                ubound=ubound,
                current_position=current_position,
                target_vol=more_opts.get('target_vol'),
                turn_over_target=more_opts.get('turn_over_target'),
                risk_model=risk_model)
        except Exception as e:
            kd_logger.error('{0} rebalance error. {1}'.format(
                data.trade_date.values[0], str(e)))
            target_pos = current_position if not is_benchmark else benchmark_w
            target_pos = pd.DataFrame(target_pos, columns=['weight'])
            target_pos['industry'] = data.industry_code.values
            target_pos['er'] = er
        return target_pos

    def _build_setting(self, neutralized_styles, effective_industry,
                       invalid_industry, riskstyle, setting_params):
        _boundary = {
            'absolute': BoundaryType.ABSOLUTE,
            'relative': BoundaryType.RELATIVE
        }
        constraint_risk = neutralized_styles + riskstyle
        b_type = []
        l_val = []
        u_val = []
        total_risk_names = constraint_risk + ['benchmark', 'total']
        for name in total_risk_names:
            if name == 'benchmark':
                b_type.append(
                    _boundary[setting_params['benchmark']['boundary']])
                l_val.append(setting_params['benchmark']['lower'])
                u_val.append(setting_params['benchmark']['upper'])
            elif name == 'total':
                b_type.append(_boundary[setting_params['total']['boundary']])
                l_val.append(setting_params['total']['lower'])
                u_val.append(setting_params['total']['upper'])
            elif name in effective_industry:
                b_type.append(_boundary[setting_params['effective_industry']
                                        ['boundary']])
                l_val.append(setting_params['effective_industry']['lower'])
                u_val.append(setting_params['effective_industry']['upper'])
            elif name in invalid_industry:
                b_type.append(
                    _boundary[setting_params['invalid_industry']['boundary']])
                l_val.append(setting_params['invalid_industry']['lower'])
                u_val.append(setting_params['invalid_industry']['upper'])
            else:
                b_type.append(_boundary[setting_params['other']['boundary']])
                l_val.append(setting_params['other']['lower'])
                u_val.append(setting_params['other']['upper'])
        bounds = create_box_bounds(total_risk_names, b_type, l_val, u_val)
        return RunningSetting(
            neutralized_styles=setting_params['neutralized_styles'],
            bounds=bounds,
            lbound=setting_params['lbound'],
            ubound=setting_params['ubound'],
            weights_bandwidth=setting_params['weights_bandwidth'],
            rebalance_method=setting_params['method'],
            cov_winodws=setting_params['cov_windows'],
            cov_method=setting_params['cov_method'],
            target_vol=setting_params['target_vol'],
            is_benchmark=setting_params['is_benchmark'],
            turn_over_target=setting_params['turn_over_target'])

    def create_positions(self, params, total_data):
        kd_logger.info("starting re-balance ...")
        is_in_benchmark = (total_data.weight >
                           0.).astype(float).values.reshape((-1, 1))
        total_data.loc[:, 'benchmark'] = is_in_benchmark
        total_data.loc[:, 'total'] = np.ones_like(is_in_benchmark)
        total_data_groups = total_data.groupby('trade_date')
        previous_pos = pd.DataFrame()
        positions = pd.DataFrame()

        running_setting = self._build_setting(
            neutralized_styles=params['industry']['effective'] +
            params['industry']['invalid'],
            effective_industry=params['industry']['effective'],
            invalid_industry=params['industry']['invalid'],
            riskstyle=params['riskstyle'],
            setting_params=params['setting_params'])
        kd_logger.info("running setting finished ...")

        if self.alpha_models is None:
            self.prepare_backtest_models(features=self.featrues)

        for ref_date, this_data in total_data_groups:
            if ref_date < self.start_date:
                continue
            new_model = self.alpha_models[ref_date]
            risk_model = self.risk_models[
                ref_date] if self.risk_models is not None else None
            codes = this_data.code.values.tolist()

            if previous_pos.empty:
                current_position = None
            else:
                previous_pos.set_index('code', inplace=True)
                remained_pos = previous_pos.reindex(codes)
                remained_pos.fillna(0., inplace=True)
                current_position = remained_pos.weight.values

            benchmark_w = this_data.weight.values
            constraints = LinearConstraints(running_setting.bounds, this_data,
                                            benchmark_w)
            lbound, ubound = self._create_lu_bounds(running_setting, codes,
                                                    benchmark_w)
            this_data.fillna(0, inplace=True)
            new_factors = factor_processing(
                this_data[new_model.features].values,
                pre_process=[winsorize_normal, standardize],
                risk_factors=this_data[
                    running_setting.neutralized_styles].values.astype(float)
                if running_setting.neutralized_styles else None,
                post_process=[standardize])

            new_factors = pd.DataFrame(new_factors,
                                       columns=new_model.features,
                                       index=codes)
            er = new_model.predict(new_factors).astype(float)

            kd_logger.info('{0} re-balance: {1} codes'.format(
                ref_date, len(er)))
            target_pos = self._calculate_pos(
                running_setting,
                er,
                this_data,
                constraints,
                benchmark_w,
                lbound,
                ubound,
                risk_model=risk_model.get_risk_profile(codes)
                if risk_model is not None else None,
                current_position=current_position)

            target_pos['code'] = codes
            target_pos['trade_date'] = ref_date
            target_pos['benchmark'] = benchmark_w
            positions = positions.append(target_pos)
            previous_pos = target_pos
        return positions

    def rebalance_positions(self, params):
        factors_data = copy.deepcopy(self.total_data)
        positions = self.create_positions(params=params,
                                          total_data=factors_data)

        return positions

    def backtest(self, positions, yields, rate):
        kd_logger.info("starting backting ...")
        executor = NaiveExecutor()
        total_data = positions.merge(yields[['trade_date', 'code',
                                             'nxt1_ret']],
                                     on=['trade_date', 'code'])
        total_data_groups = total_data.groupby('trade_date')
        rets = []
        b_rets = []
        turn_overs = []
        leverags = []
        for ref_date, this_data in total_data_groups:
            turn_over, executed_pos = executor.execute(this_data)
            leverage = executed_pos.weight.abs().sum()
            ret = executed_pos.weight.values @ (
                np.exp(this_data.nxt1_ret.values) - 1.) - len(
                    this_data.code) * rate * turn_over
            b_ret = executed_pos.benchmark.values @ (
                np.exp(this_data.nxt1_ret.values) - 1.) - len(
                    this_data.code) * rate * turn_over
            rets.append(np.log(1. + ret))
            b_rets.append(np.log(1. + b_ret))
            executor.set_current(executed_pos)
            turn_overs.append(turn_over)
            leverags.append(leverage)
            kd_logger.info('{0}: turn over {1}, returns {2}'.format(
                ref_date, round(turn_over, 4), round(ret, 4)))

        trade_dates = positions.trade_date.unique()
        ret_df = pd.DataFrame(
            {
                'returns': rets,
                'turn_over': turn_overs,
                'leverage': leverags,
                'benchmark_returns': b_rets
            },
            index=trade_dates)
        ret_df['benchmark_returns'] = self.index_return[
            'returns'].values if self.index_return is not None else ret_df[
                'benchmark_returns'].values
        ret_df['excess_return'] = ret_df[
            'returns'] - ret_df['benchmark_returns'] * ret_df['leverage']
        return ret_df

    def empyrical(self, ret_df):
        rets = []

        def metrics(returns, turnover=0, period=empyrical.DAILY):
            returns = returns.astype('float').dropna()
            annual_return = empyrical.annual_return(returns=returns,
                                                    period=period)
            annual_volatility = empyrical.annual_volatility(returns=returns,
                                                            period=period)
            cagr = empyrical.cagr(returns=returns, period=period)
            sharpe_ratio = empyrical.sharpe_ratio(returns=returns,
                                                  period=period)
            downside_risk = empyrical.downside_risk(returns=returns,
                                                    period=period)
            max_drawdown = empyrical.max_drawdown(returns=returns)
            results = {
                'annual_return': annual_return,
                'annual_volatility': annual_volatility,
                'cagr': cagr,
                'sharpe_ratio': sharpe_ratio,
                'downside_risk': downside_risk,
                'max_drawdown': max_drawdown,
                'calmar_ratio': -annual_return / max_drawdown
            }
            if turnover > 0.: results['turnover'] = turnover
            return results

        for r in ['returns', 'benchmark_returns', 'excess_return']:
            turnover = ret_df['turn_over'].mean() if r == 'returns' else 0
            mat = metrics(ret_df[r], turnover=turnover)
            mat['name'] = r
            rets.append(mat)
        return rets

    def run(self, params, rate=0.0):
        yields = self.total_data[['trade_date', 'code', 'nxt1_ret']]
        positions = self.rebalance_positions(params=params)
        returns = self.backtest(positions, yields, rate)
        metrics = self.empyrical(returns)
        return metrics, returns, positions
