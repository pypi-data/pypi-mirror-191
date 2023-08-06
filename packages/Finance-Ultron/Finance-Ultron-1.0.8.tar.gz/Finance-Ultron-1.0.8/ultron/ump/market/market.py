# -*- encoding:utf-8 -*-
"""
    市场相关切割，选股，等操作模块
"""
import pandas as pd
from ultron.kdutils.lazy import LazyFunc
from ultron.ump.core.env import EMarketTargetType
from ultron.ump.market.symbol import Symbol, code_to_symbol
from ultron.ump.market.stock import SymbolCN
from ultron.ump.market.futures import FuturesCn


class MarketMixin(object):
    """
        市场信息混入类，被混入类需要设置self.symbol_name，
        通过code_to_symbol将symbol转换为Symbol对象, 通过Symbol对象
        查询market和sub_market
    """

    @LazyFunc
    def _symbol(self):
        """通过code_to_symbol将symbol转换为Symbol对象 LazyFunc"""
        if not hasattr(self, 'symbol_name'):
            # 被混入类需要设置self.symbol_name
            raise NameError('must name symbol_name!!')
        # 通过code_to_symbol将symbol转换为Symbol对象
        return code_to_symbol(self.symbol_name)

    @LazyFunc
    def symbol_market(self):
        """查询self.symbol_name的市场类型 LazyFunc"""
        return self._symbol.market

    @LazyFunc
    def symbol_sub_market(self):
        """查询self.symbol_name的子市场类型，即交易所信息 LazyFunc"""
        return self._symbol.sub_market


def _all_tc_symbol():
    """
    获取币类symbol，注意这里只取比特币与莱特币，可自行扩展其它币种
    :return:
    """
    return ['btc', 'ltc']


def _all_futures_cn():
    """
    AbuFuturesCn().symbol获取国内期货symbol代码，注意这里只取连续合约代码
    :return:
    """
    return FuturesCn().symbol


def _all_cn_symbol(index=False):
    """
    通过AbuSymbolCN().all_symbol获取A股全市场股票代码
    :param index: 是否包含指数
    :return:
    """
    # noinspection PyProtectedMember
    #if ABuEnv._g_enable_example_env_ipython:
    #    return K_SAND_BOX_CN
    return SymbolCN().all_symbol(index=index)


def split_k_market(k_split, market_symbols=None, market=None):
    """
    将market_symbols序列切分成k_split个序列
    :param k_split: 切分成子序列个数int
    :param market_symbols: 待切割的原始symbols序列，如果none, 将取market参数中指定的市场所有symbol
    :param market: 默认None，如None则服从ABuEnv.g_market_target市场设置
    :return: list序列，序列中的每一个元素都是切割好的子symbol序列
    """
    if market_symbols is None:
        # 取market参数中指定的市场所有symbol
        market_symbols = all_symbol(market=market)
    if len(market_symbols) < k_split:
        # 特殊情况，eg：k_split＝100，但是len(market_symbols)＝50，就不切割了，直接返回
        return [[symbol] for symbol in market_symbols]

    # 计算每一个子序列的承载的symbol个数，即eg：100 ／ 5 ＝ 20
    sub_symbols_cnt = int(len(market_symbols) / k_split)
    group_adjacent = lambda a, k: zip(*([iter(a)] * k))
    # 使用lambda函数group_adjacent将market_symbols切割子序列，每个子系列sub_symbols_cnt个
    symbols = list(group_adjacent(market_symbols, sub_symbols_cnt))
    # 将不能整除的余数symbol个再放进去
    residue_ind = -(len(market_symbols) %
                    sub_symbols_cnt) if sub_symbols_cnt > 0 else 0
    if residue_ind < 0:
        # 所以如果不能除尽，最终切割的子序列数量为k_split+1, 外部如果需要进行多认为并行，可根据最终切割好的数量重分配任务数
        symbols.append(market_symbols[residue_ind:])
    return symbols


def all_symbol(market=None, ss=False, index=False, value=True):
    """
    根据传入的市场获取全市场代码
    :param market: 默认None，如None则服从ABuEnv.g_market_target市场设置
    :param ss: 是否将返回序列使用pd.Series包装
    :param index: 是否包含指数大盘symbol
    :param value: 返回字符串值，即如果序列中的元素是Symbol对象，Symbol转换字符串
    :return:
    """
    if market is None:
        raise
        # None则服从ABuEnv.g_market_target市场设置
        #market = ABuEnv.g_market_target

    if market == EMarketTargetType.E_MARKET_TARGET_CN:
        symbols = _all_cn_symbol(index)
    elif market == EMarketTargetType.E_MARKET_TARGET_FUTURES_CN:
        symbols = _all_futures_cn()
    elif market == EMarketTargetType.E_MARKET_TARGET_TC:
        symbols = _all_tc_symbol()
    else:
        raise TypeError('JUST SUPPORT EMarketTargetType!')

    # 在出口统一确保唯一性, 在每一个内部_all_xx_symbol中也要尽量保证唯一
    symbols = list(set(symbols))

    if value:
        """
            如果是Symbol类型的还原成字符串，尽量在上面返回的symbols序列是字符串类型
            不要在上面构造symbol，浪费效率，统一会在之后的逻辑中通过code_to_symbol
            进行转换
        """
        symbols = [
            sb.value if isinstance(sb, Symbol) else sb for sb in symbols
        ]
    # 根据参数ss是否将返回序列使用pd.Series包装
    return pd.Series(symbols) if ss else symbols