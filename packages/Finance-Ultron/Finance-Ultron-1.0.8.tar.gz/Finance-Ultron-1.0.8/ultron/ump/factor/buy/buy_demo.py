# -*- encoding:utf-8 -*-
"""
    示例买入择时因子
"""
from ultron.ump.factor.buy.base import FactorBuyBase, FactorBuyXD, FactorBuyTD, BuyCallMixin
from ultron.ump.factor.buy.buy_break import FactorBuyBreak
from ultron.ump.factor.buy.buy_wrap import LeastPolyWrap
from ultron.ump.technical.line import Line


class FactorSDBreak(FactorBuyXD, BuyCallMixin):
    """示例买入因子： 在FactorBuyBreak基础上进行降低交易频率，提高系统的稳定性处理"""

    def _init_self(self, **kwargs):
        """
        :param kwargs: kwargs可选参数poly值，poly在fit_month中和每一个月大盘计算的poly比较，
        若是大盘的poly大于poly认为走势震荡，poly默认为2
        """
        super(FactorSDBreak, self)._init_self(**kwargs)
        # poly阀值，self.poly在fit_month中和每一个月大盘计算的poly比较，若是大盘的poly大于poly认为走势震荡
        self.poly = kwargs.pop('poly', 2)
        # 是否封锁买入策略进行择时交易
        self.lock = False

    def fit_month(self, today):
        # fit_month即在回测策略中每一个月执行一次的方法
        # 策略中拥有self.benchmark，即交易基准对象，Benchmark实例对象，benchmark.kl_pd即对应的市场大盘走势
        benchmark_df = self.benchmark.kl_pd
        # 拿出大盘的今天
        benchmark_today = benchmark_df[benchmark_df.date == today.date]
        if benchmark_today.empty:
            return 0
        # 要拿大盘最近一个月的走势，准备切片的start，end
        end_key = int(benchmark_today.iloc[0].key)
        start_key = end_key - 20
        if start_key < 0:
            return False
        # 使用切片切出从今天开始向前20天的数据
        benchmark_month = benchmark_df.set_index('key').loc[start_key:end_key +
                                                            1].reset_index()

        # 通过大盘最近一个月的收盘价格做为参数构造TLine对象
        benchmark_month_line = Line(benchmark_month.close,
                                    'benchmark month line')
        # 计算这个月最少需要几次拟合才能代表走势曲线

        least, _, _, _, _, _ = benchmark_month_line.create_least_valid_poly()

        if least >= self.poly:
            # 如果最少的拟合次数大于阀值self.poly，说明走势成立，大盘非震荡走势，解锁交易
            self.lock = False
        else:
            # 如果最少的拟合次数小于阀值self.poly，说明大盘处于震荡走势，封锁策略进行交易
            self.lock = True

    def fit_day(self, today):
        if self.lock:
            # 如果封锁策略进行交易的情况下，策略不进行择时
            return None

        # 今天的收盘价格达到xd天内最高价格则符合买入条件
        if today.close == self.xd_kl.close.max():
            return self.buy_tomorrow()


@LeastPolyWrap()
class TwoDayBuy(FactorBuyTD, BuyCallMixin):
    """示例LeastPolyWrap，混入BuyCallMixin，即向上突破触发买入event"""

    def _init_self(self, **kwargs):
        """简单示例什么都不编写了"""
        pass

    def fit_day(self, today):
        """
        针对每一个交易日拟合买入交易策略，今天涨，昨天涨就买
        :param today: 当前驱动的交易日金融时间序列数据
        :return:
        """
        # 今天的涨幅
        td_change = today.p_change
        # 昨天的涨幅
        yd_change = self.yesterday.p_change

        if td_change > 0 and 0 < yd_change < td_change:
            # 连续涨两天, 且今天的涨幅比昨天还高 －>买入, 用到了今天的涨幅，只能明天买
            return self.buy_tomorrow()
        return None


class WeekMonthBuy(FactorBuyBase, BuyCallMixin):
    """策略示例每周买入一次或者每一个月买入一次"""

    def _init_self(self, **kwargs):
        """kwargs可选参数：is_buy_month，bool默认True一个月买入一次, False一周买入一次"""
        self.is_buy_month = kwargs.pop('is_buy_month', True)

    def fit_day(self, today):
        """
        :param today: 当前驱动的交易日金融时间序列数据
        """
        if self.is_buy_month and today.exec_month or not self.is_buy_month and today.exec_week:
            # 没有用到今天的任何数据，直接今天买入
            return self.buy_today()
