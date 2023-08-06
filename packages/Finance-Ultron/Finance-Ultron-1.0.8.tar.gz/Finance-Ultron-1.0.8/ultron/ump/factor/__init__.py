# -*- encoding:utf-8 -*-
from ultron.ump.factor.sell.atrn_stop import FactorAtrNStop
from ultron.ump.factor.sell.close_atrn_stop import FactorCloseAtrNStop
from ultron.ump.factor.sell.pre_atrn_stop import FactorPreAtrNStop
from ultron.ump.factor.sell.sell_nday import FactorSellNDay
from ultron.ump.factor.sell.sell_break import FactorSellBreak
from ultron.ump.factor.sell.sell_break import FactorSellXDBK
from ultron.ump.factor.buy.buy_break import FactorBuyBreak
from ultron.ump.factor.buy.buy_break import FactorBuyXDBK
from ultron.ump.factor.buy.buy_break import FactorBuyPutBreak
from ultron.ump.factor.buy.buy_break import FactorBuyPutXDBK
from ultron.ump.factor.buy.buy_demo import FactorSDBreak
from ultron.ump.factor.buy.buy_wd import FactorBuyXD

from ultron.ump.factor.buy.buy_demo import TwoDayBuy
from ultron.ump.factor.buy.buy_demo import WeekMonthBuy
from ultron.ump.factor.buy.buy_dm import DoubleMaBuy
from ultron.ump.factor.buy.buy_trend import UpDownTrend
from ultron.ump.factor.buy.buy_trend import DownUpTrend
from ultron.ump.factor.sell.sell_dm import DoubleMaSell

__all__ = [
    'FactorAtrNStop', 'FactorCloseAtrNStop', 'FactorPreAtrNStop',
    'FactorSellNDay', 'FactorSellBreak', 'FactorSellXDBK', 'FactorBuyBreak',
    'FactorBuyXDBK', 'FactorBuyPutBreak', 'FactorBuyPutXDBK', 'FactorSDBreak',
    'FactorBuyXD', 'TwoDayBuy', 'WeekMonthBuy', 'DoubleMaBuy', 'UpDownTrend',
    'DownUpTrend', 'DoubleMaSell'
]
