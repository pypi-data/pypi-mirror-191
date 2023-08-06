# -*- encoding:utf-8 -*-
"""
    全局环境配置模块
"""

from enum import Enum
import os
"""主进程pid，使用并行时由于EnvProcess会拷贝主进程注册了的模块信息，所以可以用g_main_pid来判断是否在主进程"""
g_main_pid = os.getpid()
g_is_ipython = True

g_is_mac_os = False
try:
    # noinspection PyUnresolvedReferences
    __IPYTHON__
except NameError:
    g_is_ipython = False


# TODO 缩短 E_MARKET_TARGET_US－>US
class EMarketTargetType(Enum):
    """
        交易品种类型，即市场类型，
        eg. 美股市场, A股市场, 港股市场, 国内期货市场,
            美股期权市场, TC币市场（比特币等
    """
    """美股市场"""
    E_MARKET_TARGET_US = 'us'
    """A股市场"""
    E_MARKET_TARGET_CN = 'hs'
    """港股市场"""
    E_MARKET_TARGET_HK = 'hk'
    """国内期货市场"""
    E_MARKET_TARGET_FUTURES_CN = 'futures_cn'
    """国际期货市场"""
    E_MARKET_TARGET_FUTURES_GLOBAL = 'futures_global'
    """美股期权市场"""
    E_MARKET_TARGET_OPTIONS_US = 'options_us'
    """TC币市场（比特币等）"""
    E_MARKET_TARGET_TC = 'tc'


g_market_trade_year = 250


# TODO 缩短 E_DATA_FETCH_NORMAL－>NORMAL
class EMarketDataFetchMode(Enum):
    """
        金融时间数据获取模式
    """
    """普通模式，尽量从本地获取数据，本地数据不满足的情况下进行网络请求"""
    E_DATA_FETCH_NORMAL = 0
    """强制从本地获取数据，本地数据不满足的情况下，返回None"""
    E_DATA_FETCH_FORCE_LOCAL = 1
    """强制从网络获取数据，不管本地数据是否满足"""
    E_DATA_FETCH_FORCE_NET = 2


class EDataCacheType(Enum):
    """
        金融时间序列数据缓存类型
    """
    """读取及写入最快 但非固态硬盘写入慢，存贮空间需要大"""
    E_DATA_CACHE_HDF5 = 0
    """读取及写入最慢 但非固态硬盘写速度还可以，存贮空间需要小"""
    E_DATA_CACHE_CSV = 1
    """适合分布式扩展，存贮空间需要大"""
    E_DATA_CACHE_MONGODB = 2


# TODO EMarketDataSplitMode移动到市场请求相关对应的模块中
class EMarketDataSplitMode(Enum):
    """
        ABuSymbolPd中请求参数，关于是否需要与基准数据对齐切割
    """
    """直接取出所有data，不切割，即外部需要切割"""
    E_DATA_SPLIT_UNDO = 0
    """内部根据start，end取切割data"""
    E_DATA_SPLIT_SE = 1


class EMarketSubType(Enum):
    """
        子市场（交易所）类型定义
    """
    """美股纽交所NYSE"""
    US_N = 'NYSE'
    """美股纳斯达克NASDAQ"""
    US_OQ = 'NASDAQ'
    """美股粉单市场"""
    US_PINK = 'PINK'
    """美股OTCMKTS"""
    US_OTC = 'OTCMKTS'
    """美国证券交易所"""
    US_AMEX = 'AMEX'
    """未上市"""
    US_PREIPO = 'PREIPO'
    """港股hk"""
    HK = 'hk'
    """上证交易所sh"""
    SH = 'sh'
    """深圳交易所sz"""
    SZ = 'sz'
    """大连商品交易所DCE'"""
    DCE = 'DCE'
    """郑州商品交易所ZZCE'"""
    ZZCE = 'ZZCE'
    """上海期货交易所SHFE'"""
    SHFE = 'SHFE'
    """伦敦金属交易所"""
    LME = 'LME'
    """芝加哥商品交易所"""
    CBOT = 'CBOT'
    """纽约商品交易所"""
    NYMEX = 'NYMEX'
    """币类子市场COIN'"""
    COIN = 'COIN'


"""切换目标操作市场，美股，A股，港股，期货，比特币等，默认美股市场"""
g_market_target = EMarketTargetType.E_MARKET_TARGET_US

try:
    # noinspection PyUnresolvedReferences
    import psutil
    """有psutil，使用psutil.cpu_count计算cpu个数"""
    g_cpu_cnt = psutil.cpu_count(logical=True) * 1
except ImportError:
    if True:
        # noinspection PyUnresolvedReferences
        g_cpu_cnt = os.cpu_count()
    else:
        import multiprocessing as mp

        g_cpu_cnt = mp.cpu_count()
except:
    # 获取cpu个数失败，默认4个
    g_cpu_cnt = 4

# ＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊主裁 start ＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊
# TODO 内置ump的设置move到UltronUmpManager中
"""是否开启裁判拦截机制: 主裁deg，默认关闭False"""
g_enable_ump_main_deg_block = False
"""是否开启裁判拦截机制: 主裁jump，默认关闭False"""
g_enable_ump_main_jump_block = False
"""是否开启裁判拦截机制: 主裁price，默认关闭False"""
g_enable_ump_main_price_block = False
"""是否开启裁判拦截机制: 主裁wave，默认关闭False"""
g_enable_ump_main_wave_block = False
"""是否开启裁判拦截机制: 边裁deg，默认关闭False"""
g_enable_ump_edge_deg_block = False
"""是否开启裁判拦截机制: 边裁price，默认关闭False"""
g_enable_ump_edge_price_block = False
"""是否开启裁判拦截机制: 边裁wave，默认关闭False"""
g_enable_ump_edge_wave_block = False
"""是否开启裁判拦截机制: 边裁full，默认关闭False"""
g_enable_ump_edge_full_block = False
"""是否开启机器学习特征收集, 开启后速度会慢，默认关闭False"""
g_enable_ml_feature = False
"""是否启用外部用户使用append_user_ump添加的ump对交易进行拦截决策"""
g_enable_user_ump = False