# coding=utf-8
"""
    数据对外接口模块，其它模块需要数据都只应该使用SymbolPd, 不应涉及其它内部模块的使用
"""
from collections import Iterable
import pandas as pd
import numpy as np
from ultron.ump.core import env
from ultron.ump.core.fixes import six
from ultron.ump.market.market import split_k_market
from ultron.kdutils.date import week_of_date


def _benchmark(df, benchmark_pd):
    """
    在内部使用kline_pd获取金融时间序列pd.DataFrame后，如果参数中
    基准benchmark（pd.DataFrame对象）存在，使用基准benchmark的
    时间范围切割kline_pd返回的金融时间序列
    :param df: 金融时间序列pd.DataFrame对象
    :param benchmark: 资金回测时间标尺，AbuBenchmark实例对象
    :return: 使用基准的时间范围切割返回的金融时间序列
    """
    if len(df.index & benchmark_pd.index) <= 0:
        # 如果基准benchmark时间范围和输入的df没有交集，直接返回None
        return None

    df = df.reindex(benchmark_pd.index)
    kl_pd = df.loc[benchmark_pd.index]

    # 两个金融时间序列通过loc寻找交集
    kl_pd = df.loc[benchmark_pd.index]
    # nan的date个数即为不相交的个数
    nan_cnt = kl_pd['date'].isnull().value_counts()
    # 两个金融序列是否相同的结束日期
    same_end = df.index[-1] == benchmark_pd.index[-1]
    # 两个金融序列是否相同的开始日期
    same_head = df.index[0] == benchmark_pd.index[0]

    # 如果nan_cnt即不相交个数大于benchmark基准个数的1/3，放弃
    base_keep_div = 3
    if same_end or same_head:
        # 如果两个序列有相同的开始或者结束改为1/2，也就是如果数据头尾日起的标尺有一个对的上的话，放宽na数量
        base_keep_div = 2
    if same_end and same_head:
        # 如果两个序列同时有相同的开始和结束改为1，也就是如果数据头尾日起的标尺都对的上的话，na数量忽略不计
        base_keep_div = 1

    #if symbol.is_a_stock():
    #    # 如果是A股市场的目标，由于停盘频率和周期都会长与其它市场所以再放宽一些
    #    base_keep_div *= 0.7

    if nan_cnt.index.shape[0] > 0 and nan_cnt.index.tolist().count(True) > 0 \
            and nan_cnt.loc[True] > benchmark_pd.shape[0] / base_keep_div:
        # nan 个数 > 基准base_keep_div分之一放弃
        return None

    # 来到这里说明没有放弃，那么就填充nan
    # 首先nan的交易量是0
    kl_pd.volume.fillna(value=0, inplace=True)
    # nan的p_change是0
    kl_pd.p_change.fillna(value=0, inplace=True)
    # 先把close填充了，然后用close填充其它的
    kl_pd.close.fillna(method='pad', inplace=True)
    kl_pd.close.fillna(method='bfill', inplace=True)
    # 用close填充open
    kl_pd.open.fillna(value=kl_pd.close, inplace=True)
    # 用close填充high
    kl_pd.high.fillna(value=kl_pd.close, inplace=True)
    # 用close填充low
    kl_pd.low.fillna(value=kl_pd.close, inplace=True)
    # 用close填充pre_close
    kl_pd.pre_close.fillna(value=kl_pd.close, inplace=True)

    # 细节nan处理完成后，把剩下的nan都填充了
    kl_pd = kl_pd.fillna(method='pad')
    # bfill再来一遍只是为了填充最前面的nan
    kl_pd.fillna(method='bfill', inplace=True)

    # pad了数据所以，交易日期date的值需要根据time index重新来一遍
    kl_pd['date'] = [int(ts.date().strftime("%Y%m%d")) for ts in kl_pd.index]
    kl_pd['date_week'] = kl_pd['date'].apply(
        lambda x: week_of_date(str(x), '%Y%m%d'))

    return kl_pd


# noinspection PyDeprecation
def make_kl_df(symbol,
               data_mode=env.EMarketDataSplitMode.E_DATA_SPLIT_SE,
               n_folds=2,
               start=None,
               end=None,
               benchmark=None,
               show_progress=True,
               parallel=False,
               parallel_save=True):
    """
    外部获取金融时间序列接口
    eg: n_fold=2, start=None, end=None ，从今天起往前数两年
        n_fold=2, start='2015-02-14', end=None， 从2015-02-14到现在，n_fold无效
        n_fold=2, start=None, end='2016-02-14'，从2016-02-14起往前数两年
        n_fold=2, start='2015-02-14', end='2016-02-14'，从start到end

    :param data_mode: EMarketDataSplitMode对象
    :param symbol: list or Series or str or Symbol
                    e.g :['TSLA','SFUN'] or 'TSLA' or Symbol(MType.US,'TSLA')
    :param n_folds: 请求几年的历史回测数据int
    :param start: 请求的开始日期 str对象
    :param end: 请求的结束日期 str对象
    :param benchmark: 资金回测时间标尺，AbuBenchmark实例对象
    :param show_progress: 是否显示进度条
    :param parallel: 是否并行获取
    :param parallel_save: 是否并行后进行统一批量保存
    """

    if isinstance(symbol, (list, tuple, pd.Series, pd.Index)):
        # 如果symbol是可迭代的序列对象，最终返回三维面板数据pd.Panel
        panel = dict()
        if parallel:
            # 如果并行获取
            if env.g_data_fetch_mode != env.EMarketDataFetchMode.E_DATA_FETCH_FORCE_NET \
                    and env.g_data_cache_type == env.EDataCacheType.E_DATA_CACHE_HDF5:
                # 只能针对非hdf5存贮形式下或者针对force_net，因为hdf5多线程读容易卡死
                raise RuntimeError(
                    'make_kl_df just suit force net or not hdf5 store!')

            df_dicts = kl_df_dict_parallel(symbol,
                                           data_mode=data_mode,
                                           n_folds=n_folds,
                                           start=start,
                                           end=end,
                                           benchmark=benchmark,
                                           save=parallel_save,
                                           how='thread')
            for df_dict in df_dicts:
                for key_tuple, df in df_dict.values():
                    if df is None or df.shape[0] == 0:
                        continue
                    # 即丢弃原始df_dict保存金融时间序列时使用的save_kl_key，只保留df，赋予panel
                    panel[key_tuple[0].value] = df
        else:

            def _batch_make_kl_df():
                with AbuMulPidProgress(len(symbol),
                                       '_make_kl_df complete') as progress:
                    for pos, _symbol in enumerate(symbol):
                        _df, _ = _make_kl_df(_symbol,
                                             data_mode=data_mode,
                                             n_folds=n_folds,
                                             start=start,
                                             end=end,
                                             benchmark=benchmark,
                                             save=True)
                        if show_progress:
                            progress.show()
                        # TODO 做pd.Panel数据应该保证每一个元素的行数和列数都相等，不是简单的有数据就行
                        if _df is None or _df.shape[0] == 0:
                            continue

                        panel[symbol[pos]] = _df

            _batch_make_kl_df()
        # TODO pd.Panel过时
        return pd.Panel(panel)

    elif isinstance(symbol, Symbol) or isinstance(symbol, six.string_types):
        # 对单个symbol进行数据获取
        df, _ = _make_kl_df(symbol,
                            data_mode=data_mode,
                            n_folds=n_folds,
                            start=start,
                            end=end,
                            benchmark=benchmark,
                            save=True)
        return df
    else:
        raise TypeError('symbol type is error')


def kl_df_dict_parallel(symbols,
                        data_mode=env.EMarketDataSplitMode.E_DATA_SPLIT_SE,
                        n_folds=2,
                        start=None,
                        end=None,
                        benchmark=None,
                        n_jobs=16,
                        how='thread'):
    """
    多进程或者多线程对外执行函数，多任务批量获取时间序列数据
    :param symbols: symbol序列
    :param data_mode: EMarketDataSplitMode enum对象
    :param n_folds: 请求几年的历史回测数据int
    :param start: 请求的开始日期 str对象
    :param end: 请求的结束日期 str对象
    :param benchmark: 资金回测时间标尺，AbuBenchmark实例对象
    :param n_jobs: 并行的任务数，对于进程代表进程数，线程代表线程数
    :param save: 是否统一进行批量保存，即在批量获取金融时间序列后，统一进行批量保存，默认True
    :param how: process：多进程，thread：多线程，main：单进程单线程
    """

    # TODO Iterable和six.string_types的判断抽出来放在一个模块，做为Iterable的判断来使用
    if not isinstance(symbols, Iterable) or isinstance(symbols,
                                                       six.string_types):
        # symbols必须是可迭代的序列对象
        raise TypeError('symbols must a Iterable obj!')
    # 可迭代的symbols序列分成n_jobs个子序列
    parallel_symbols = split_k_market(n_jobs, market_symbols=symbols)
    # 使用partial对并行函数_kl_df_dict_parallel进行委托
    parallel_func = partial(_kl_df_dict_parallel,
                            data_mode=data_mode,
                            n_folds=n_folds,
                            start=start,
                            end=end,
                            benchmark=benchmark)
    # 因为切割会有余数，所以将原始设置的进程数切换为分割好的个数, 即32 -> 33 16 -> 17
    n_jobs = len(parallel_symbols)
    if how == 'process':
        """
            mac os 10.9 以后的并行加上numpy不是crash就是进程卡死，不要用，用thread
        """
        if ABuEnv.g_is_mac_os:
            logging.info('mac os 10.9 parallel with numpy crash or dead!!')

        parallel = Parallel(n_jobs=n_jobs, verbose=0, pre_dispatch='2*n_jobs')
        df_dicts = parallel(
            delayed(parallel_func)(choice_symbols)
            for choice_symbols in parallel_symbols)
    elif how == 'thread':
        # 通过ThreadPoolExecutor进行线程并行任务
        with ThreadPoolExecutor(max_workers=n_jobs) as pool:
            k_use_map = True
            if k_use_map:
                df_dicts = list(pool.map(parallel_func, parallel_symbols))
            else:
                futures = [
                    pool.submit(parallel_func, symbols)
                    for symbols in parallel_symbols
                ]
                df_dicts = [
                    future.result() for future in futures
                    if future.exception() is None
                ]
    elif how == 'main':
        # 单进程单线程
        df_dicts = [parallel_func(symbols) for symbols in parallel_symbols]
    else:
        raise TypeError('ONLY process OR thread!')
    return df_dicts