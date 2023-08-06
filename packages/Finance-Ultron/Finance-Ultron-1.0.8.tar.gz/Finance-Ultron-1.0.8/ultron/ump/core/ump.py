# -*- encoding:utf-8 -*-
from collections import namedtuple
from ultron.kdutils import date as date_utils
from ultron.ump.core import env
from ultron.utilities.logger import kd_logger
from ultron.ump.market.benchmark import Benchmark
from ultron.ump.trade.kl_manager import KLManager
from ultron.ump.trade.capital import Capital
from ultron.ump.alpha.pick_time_master import PickTimeMaster


# noinspection PyClassHasNoInit
class ResultTuple(
        namedtuple('AbuResultTuple',
                   ('orders_pd', 'action_pd', 'capital', 'benchmark'))):
    """
        使用abu.run_loop_back返回的nametuple对象：

        orders_pd：回测结果生成的交易订单构成的pd.DataFrame对象
        action_pd: 回测结果生成的交易行为构成的pd.DataFrame对象
        capital:   资金类AbuCapital实例化对象
        benchmark: 交易基准对象，AbuBenchmark实例对象
    """
    __slots__ = ()

    def __repr__(self):
        """打印对象显示：orders_pd.info, action_pd.info, capital, benchmark"""
        return "orders_pd:{}\naction_pd:{}\ncapital:{}\nbenchmark:{}".format(
            self.orders_pd.info(), self.action_pd.info(), self.capital,
            self.benchmark)


def run_loop_back(read_cash,
                  buy_factors,
                  sell_factors,
                  pick_kl_pd_dict,
                  choice_symbols=None,
                  commission_dict=None,
                  n_process_kl=None,
                  n_process_pick=None,
                  benchmark_kl_pd=None):
    """
    封装执行择时，选股回测。

    推荐在使用abu.run_loop_back()函数进行全市场回测前使用abu.run_kl_update()函数首先将数据进行更新，
    在run_kl_update()中它会首选强制使用网络数据进行更新，在更新完毕后，更改数据获取方式为本地缓存，
    使用abu.run_kl_update()的好处是将数据更新与策略回测分离，在运行效率及问题排查上都会带来正面的提升

    :param read_cash: 初始化资金额度，eg：1000000
    :param buy_factors: 回测使用的买入因子策略序列，
                    eg：
                        buy_factors = [{'xd': 60, 'class': AbuFactorBuyBreak},
                                       {'xd': 42, 'class': AbuFactorBuyBreak}]
    :param sell_factors: 回测使用的卖出因子序列，
                    eg:
                        sell_factors = [{'stop_loss_n': 0.5, 'stop_win_n': 3.0, 'class': AbuFactorAtrNStop},
                                        {'pre_atr_n': 1.0, 'class': AbuFactorPreAtrNStop},
                                        {'close_atr_n': 1.5, 'class': AbuFactorCloseAtrNStop},]
    :param stock_picks: 回测使用的选股因子序列：
                    eg:
                        stock_pickers = [{'class': AbuPickRegressAngMinMax,
                                          'threshold_ang_min': 0.0, 'reversed': False},
                                         {'class': AbuPickStockPriceMinMax,
                                          'threshold_price_min': 50.0,
                                          'reversed': False}]
    :param choice_symbols: 备选股票池, 默认为None，即使用abupy.env.g_market_target的市场类型进行全市场回测，
                           为None的情况下为symbol序列
                    eg:
                        choice_symbols = ['usNOAH', 'usSFUN', 'usBIDU', 'usAAPL', 'usGOOG',
                                          'usTSLA', 'usWUBA', 'usVIPS']
    :param n_folds: int, 回测n_folds年的历史数据
    :param start: 回测开始的时间, str对象, eg: '2013-07-10'
    :param end: 回测结束的时间, str对象 eg: '2016-07-26'
    :param commission_dict: 透传给Capital，自定义交易手续费的时候时候。
                    eg：
                        def free_commission(trade_cnt, price):
                            # 免手续费
                            return 0
                        commission_dict = {'buy_commission_func': free_commission,
                                         'sell_commission_func': free_commission}
                        Capital(read_cash, benchmark, user_commission_dict=commission_dict)

    :param n_process_kl: 金融时间序列数据收集启动并行的进程数，默认None, 内部根据cpu数量分配
    :param n_process_pick: 择时与选股操作启动并行的进程数，默认None, 内部根据cpu数量分配
    :return: (ResultTuple对象, KLManager对象)
    """
    #if start is not None and end is not None and date_utils.date_str_to_int(
    #        end) - date_utils.date_str_to_int(start) <= 0:
    #    kd_logger.info('end date <= start date!!')
    #    return None, None

    benchmark = Benchmark(benchmark_kl_pd=benchmark_kl_pd)

    capital = Capital(read_cash,
                      benchmark,
                      user_commission_dict=commission_dict)

    win_to_one = choice_symbols is not None and len(
        choice_symbols) < 20 and not env.g_is_mac_os and env.g_cpu_cnt <= 4

    if n_process_pick is None:
        # 择时，选股并行操作的进程等于cpu数量, win_to_one满足情况下1个
        n_process_pick = 1 if win_to_one else env.g_cpu_cnt
    if n_process_kl is None:
        # mac系统下金融时间序列数据收集启动两倍进程数, windows只是进程数量，win_to_one满足情况下1个
        n_process_kl = 1 if win_to_one else env.g_cpu_cnt * 2 if env.g_is_mac_os else env.g_cpu_cnt

    kl_pd_manager = KLManager(benchmark, capital)
    kl_pd_manager.set_pick_time(pick_kl_pd_dict)

    orders_pd, action_pd, all_fit_symbols_cnt = PickTimeMaster.do_symbols_with_same_factors_process(
        choice_symbols,
        benchmark,
        buy_factors,
        sell_factors,
        capital,
        kl_pd_manager=kl_pd_manager,
        n_process_kl=n_process_kl,
        n_process_pick_time=n_process_pick)

    result_tuple = ResultTuple(orders_pd, action_pd, capital, benchmark)

    return result_tuple, kl_pd_manager
