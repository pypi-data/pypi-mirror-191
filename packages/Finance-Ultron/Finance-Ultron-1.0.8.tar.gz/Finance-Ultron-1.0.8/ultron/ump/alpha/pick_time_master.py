# -*- encoding:utf-8 -*-
"""
    择时并行多任务调度模块
"""
import pandas as pd
import numpy as np
from ultron.ump.core import env
from ultron.ump.core.process import EnvProcess
from ultron.kdutils.parallel import delayed, Parallel
from ultron.ump.market.market import split_k_market
from ultron.ump.trade import trade_execute
from ultron.ump.alpha.pick_time_execute import do_symbols_with_same_factors


class PickTimeMaster(object):
    """择时并行多任务调度类"""

    @classmethod
    def do_symbols_with_same_factors_process(
            cls,
            target_symbols,
            benchmark,
            buy_factors,
            sell_factors,
            capital,
            kl_pd_manager=None,
            n_process_kl=env.g_cpu_cnt *
        2 if env.g_is_mac_os else env.g_cpu_cnt,
            n_process_pick_time=env.g_cpu_cnt,
            show_progress=True):
        """
        将多个交易对象拆解为多份交易对象序列，多任务并行完成择时工作
        :param target_symbols: 多个择时交易对象序列
        :param benchmark: 交易基准对象，AbuBenchmark实例对象
        :param buy_factors: 买入因子序列
        :param sell_factors: 卖出因子序列
        :param capital: AbuCapital实例对象
        :param kl_pd_manager: 金融时间序列管理对象，AbuKLManager实例
        :param n_process_kl: 控制金融时间序列管理对象内部启动n_process_kl进程获取金融序列数据
        :param n_process_pick_time: 控制择时操作并行任务数量
        :param show_progress: 显示进度条，透传do_symbols_with_same_factors，默认True
        """

        if n_process_pick_time <= 0:
            # 因为下面要根据n_process_pick_time来split_k_market
            n_process_pick_time = env.g_cpu_cnt

        # 将target_symbols切割为n_process_pick_time个子序列，这样可以每个进程处理一个子序列
        process_symbols = split_k_market(n_process_pick_time,
                                         market_symbols=target_symbols)

        # 因为切割会有余数，所以将原始设置的进程数切换为分割好的个数, 即32 -> 33 16 -> 17
        n_process_pick_time = len(process_symbols)

        parallel = Parallel(
            1,  #n_process_pick_time,
            verbose=0,
            pre_dispatch='2*n_jobs')
        # 每个并行的进程通过do_symbols_with_same_factors及自己独立的子序列独立工作，注意kl_pd_manager装载了所有需要的数据
        p_env = EnvProcess()
        out = parallel(
            delayed(do_symbols_with_same_factors)(choice_symbols,
                                                  benchmark,
                                                  buy_factors,
                                                  sell_factors,
                                                  capital,
                                                  apply_capital=False,
                                                  kl_pd_manager=kl_pd_manager,
                                                  env=p_env,
                                                  show_progress=show_progress)
            for choice_symbols in process_symbols)
        orders_pd = None
        action_pd = None
        all_fit_symbols_cnt = 0
        for sub_out in out:
            # 将每个子序列进程的处理结果进行合并
            sub_orders_pd, sub_action_pd, sub_all_fit_symbols_cnt = sub_out
            orders_pd = sub_orders_pd if orders_pd is None else pd.concat(
                [orders_pd, sub_orders_pd])
            action_pd = sub_action_pd if action_pd is None else pd.concat(
                [action_pd, sub_action_pd])
            all_fit_symbols_cnt += sub_all_fit_symbols_cnt

        if orders_pd is not None and action_pd is not None:
            # 将合并后的结果按照时间及行为进行排序
            # noinspection PyUnresolvedReferences
            action_pd = action_pd.sort_values(['Date', 'action'])
            action_pd.index = np.arange(0, action_pd.shape[0])
            # noinspection PyUnresolvedReferences
            orders_pd = orders_pd.sort_values(['buy_date'])
            # 最后将所有的action作用在资金上，生成资金时序，及判断是否能买入
            trade_execute.apply_action_to_capital(capital,
                                                  action_pd,
                                                  kl_pd_manager,
                                                  show_progress=show_progress)

        return orders_pd, action_pd, all_fit_symbols_cnt