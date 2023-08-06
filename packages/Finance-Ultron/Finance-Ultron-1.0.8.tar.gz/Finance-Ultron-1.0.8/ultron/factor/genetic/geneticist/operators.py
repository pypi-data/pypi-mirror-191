# -*- coding: utf-8 -*-
import numpy as np
from ....utilities.singleton import Singleton
from ultron.sentry.Analysis.SecurityValueHolders import SecurityLatestValueHolder
from ultron.sentry.Analysis.SecurityValueHolders import SecurityCurrentValueHolder

##横截面变异
from ultron.sentry.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecurityAverageValueHolder
from ultron.sentry.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecurityDiffValueHolder
from ultron.sentry.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecuritySignValueHolder
from ultron.sentry.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecurityExpValueHolder
from ultron.sentry.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecurityLogValueHolder
from ultron.sentry.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecuritySqrtValueHolder
from ultron.sentry.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecurityAbsValueHolder
from ultron.sentry.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecurityAcosValueHolder
from ultron.sentry.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecurityAcoshValueHolder
from ultron.sentry.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecurityAsinValueHolder
from ultron.sentry.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecurityAsinhValueHolder
from ultron.sentry.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecurityNormInvValueHolder
from ultron.sentry.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecurityCeilValueHolder
from ultron.sentry.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecurityFloorValueHolder
from ultron.sentry.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecurityRoundValueHolder
from ultron.sentry.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecuritySigmoidValueHolder
from ultron.sentry.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecurityTanhValueHolder
from ultron.sentry.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecuritySimpleReturnValueHolder
from ultron.sentry.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecurityLogReturnValueHolder

##横截面交叉
from ultron.sentry.Analysis.SecurityValueHolders import SecurityAddedValueHolder
from ultron.sentry.Analysis.SecurityValueHolders import SecuritySubbedValueHolder
from ultron.sentry.Analysis.SecurityValueHolders import SecurityMultipliedValueHolder
from ultron.sentry.Analysis.SecurityValueHolders import SecurityDividedValueHolder
from ultron.sentry.Analysis.SecurityValueHolders import SecurityLtOperatorValueHolder
from ultron.sentry.Analysis.SecurityValueHolders import SecurityLeOperatorValueHolder
from ultron.sentry.Analysis.SecurityValueHolders import SecurityGtOperatorValueHolder
from ultron.sentry.Analysis.SecurityValueHolders import SecurityGeOperatorValueHolder
from ultron.sentry.Analysis.SecurityValueHolders import SecurityEqOperatorValueHolder
from ultron.sentry.Analysis.SecurityValueHolders import SecurityNeOperatorValueHolder
from ultron.sentry.Analysis.SecurityValueHolders import SecurityAndOperatorValueHolder
from ultron.sentry.Analysis.SecurityValueHolders import SecurityOrOperatorValueHolder
from ultron.sentry.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecurityMinimumValueHolder
from ultron.sentry.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecurityMaximumValueHolder

from ultron.sentry.Analysis.CrossSectionValueHolders import CSAverageSecurityValueHolder
from ultron.sentry.Analysis.CrossSectionValueHolders import CSAverageAdjustedSecurityValueHolder
from ultron.sentry.Analysis.CrossSectionValueHolders import CSResidueSecurityValueHolder
from ultron.sentry.Analysis.CrossSectionValueHolders import CSRankedSecurityValueHolder
from ultron.sentry.Analysis.CrossSectionValueHolders import CSPercentileSecurityValueHolder
from ultron.sentry.Analysis.CrossSectionValueHolders import CSZScoreSecurityValueHolder

## 横截面变异
#from ultron.sentry.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecurityPowValueHolder # 指定默认参数

## 时间序列变异
#from ultron.sentry.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecurityMACDValueHolder #双默认参数

from ultron.sentry.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecurityXAverageValueHolder
from ultron.sentry.Analysis.TechnicalAnalysis.StatefulTechnicalAnalysers import SecurityMovingAverage
from ultron.sentry.Analysis.TechnicalAnalysis.StatefulTechnicalAnalysers import SecurityMovingDecay
from ultron.sentry.Analysis.TechnicalAnalysis.StatefulTechnicalAnalysers import SecurityMovingMax
from ultron.sentry.Analysis.TechnicalAnalysis.StatefulTechnicalAnalysers import SecurityMovingArgMax
from ultron.sentry.Analysis.TechnicalAnalysis.StatefulTechnicalAnalysers import SecurityMovingMin
from ultron.sentry.Analysis.TechnicalAnalysis.StatefulTechnicalAnalysers import SecurityMovingArgMin
from ultron.sentry.Analysis.TechnicalAnalysis.StatefulTechnicalAnalysers import SecurityMovingRank
from ultron.sentry.Analysis.TechnicalAnalysis.StatefulTechnicalAnalysers import SecurityMovingQuantile
from ultron.sentry.Analysis.TechnicalAnalysis.StatefulTechnicalAnalysers import SecurityMovingAllTrue
from ultron.sentry.Analysis.TechnicalAnalysis.StatefulTechnicalAnalysers import SecurityMovingAnyTrue
from ultron.sentry.Analysis.TechnicalAnalysis.StatefulTechnicalAnalysers import SecurityMovingSum
from ultron.sentry.Analysis.TechnicalAnalysis.StatefulTechnicalAnalysers import SecurityMovingVariance
from ultron.sentry.Analysis.TechnicalAnalysis.StatefulTechnicalAnalysers import SecurityMovingStandardDeviation
from ultron.sentry.Analysis.TechnicalAnalysis.StatefulTechnicalAnalysers import SecurityMovingCountedPositive
from ultron.sentry.Analysis.TechnicalAnalysis.StatefulTechnicalAnalysers import SecurityMovingPositiveAverage
from ultron.sentry.Analysis.TechnicalAnalysis.StatefulTechnicalAnalysers import SecurityMovingPositiveDifferenceAverage
from ultron.sentry.Analysis.TechnicalAnalysis.StatefulTechnicalAnalysers import SecurityMovingNegativeDifferenceAverage
from ultron.sentry.Analysis.TechnicalAnalysis.StatefulTechnicalAnalysers import SecurityMovingRSI
from ultron.sentry.Analysis.TechnicalAnalysis.StatefulTechnicalAnalysers import SecurityMovingLogReturn

from ultron.sentry.Analysis.SecurityValueHolders import SecurityDeltaValueHolder
from ultron.sentry.Analysis.SecurityValueHolders import SecurityShiftedValueHolder

## 时间序列交叉
from ultron.sentry.Analysis.TechnicalAnalysis.StatefulTechnicalAnalysers import SecurityMovingCorrelation

from ultron.sentry.api import CSMean
from ultron.sentry.api import CSMeanAdjusted
from ultron.sentry.api import CSRes
from ultron.sentry.api import CSRank
from ultron.sentry.api import CSQuantiles
from ultron.sentry.api import CSZScore

from ultron.sentry.api import ADDED
from ultron.sentry.api import SUBBED
from ultron.sentry.api import MUL
from ultron.sentry.api import DIV
from ultron.sentry.api import MINIMUM
from ultron.sentry.api import MAXIMUM

from ultron.sentry.api import LAST
from ultron.sentry.api import CURRENT

from ultron.sentry.api import AVG
from ultron.sentry.api import DIFF
from ultron.sentry.api import SIGN
from ultron.sentry.api import EXP
from ultron.sentry.api import LOG
from ultron.sentry.api import SQRT
from ultron.sentry.api import ABS
from ultron.sentry.api import ACOS
from ultron.sentry.api import ACOSH
from ultron.sentry.api import ASIN
from ultron.sentry.api import ASINH
from ultron.sentry.api import NORMINV
from ultron.sentry.api import CEIL
from ultron.sentry.api import FLOOR
from ultron.sentry.api import ROUND
from ultron.sentry.api import SIGMOID
from ultron.sentry.api import TANH
from ultron.sentry.api import RETURNSimple
from ultron.sentry.api import RETURNLog

from ultron.sentry.api import EMA
from ultron.sentry.api import MA
from ultron.sentry.api import MADecay
from ultron.sentry.api import MMAX
from ultron.sentry.api import MARGMAX
from ultron.sentry.api import MMIN
from ultron.sentry.api import MARGMIN
from ultron.sentry.api import MRANK
from ultron.sentry.api import MQUANTILE
from ultron.sentry.api import MALLTRUE
from ultron.sentry.api import MANYTRUE
from ultron.sentry.api import MSUM
from ultron.sentry.api import MVARIANCE
from ultron.sentry.api import MSTD
from ultron.sentry.api import MNPOSITIVE
from ultron.sentry.api import MAPOSITIVE
from ultron.sentry.api import RSI
from ultron.sentry.api import MARETURNLog

from ultron.sentry.api import DELTA
from ultron.sentry.api import SHIFT

from ultron.sentry.api import MCORR
from ultron.sentry.api import MRes
from ultron.sentry.api import MSharp
from ultron.sentry.api import MSortino

import six
from enum import Enum, unique


@unique
class FunctionType(Enum):
    cross_section = 1
    time_series = 2


class Function(object):

    def __init__(self, function, arity, ftype, default_value=0):
        self.function = function
        self.arity = arity
        self.name = function.__name__
        self.ftype = ftype
        self.default_value = default_value


@six.add_metaclass(Singleton)
class Operators(object):

    def __init__(self):

        # 时间序列默认周期列表
        self._ts_period = [i for i in range(1, 22) if (i % 2) == 0]

        self._init_cs()
        self._init_ts()

        self._cs_mutation_function_list = [
            Function(f, 1, FunctionType.cross_section)
            for f in self._cross_section_mutation_list
        ]
        self._cs_crossover_function_list = [
            Function(f, 2, FunctionType.cross_section)
            for f in self._cross_section_crossover_list
        ]
        #支持全部参数
        self._ts_mutation_function_list = []
        self._ts_crossover_function_list = []
        for period in self._ts_period:
            self._ts_mutation_function_list += [
                Function(f, 1, FunctionType.time_series, period)
                for f in self._time_series_mutation_list
            ]
            self._ts_crossover_function_list += [
                Function(f, 2, FunctionType.time_series, period)
                for f in self._time_series_crossover_list
            ]

        self._mutation_sets = self._cs_mutation_function_list + self._ts_mutation_function_list
        self._crossover_sets = self._cs_crossover_function_list + self._ts_crossover_function_list

    def _init_cs(self):
        self._cross_section_mutation_list = [
            AVG, DIFF, TANH, SIGN, EXP, LOG, SQRT, ABS, ACOS, ASIN, ASINH,
            ACOSH, NORMINV, CEIL, FLOOR, ROUND, RETURNSimple, RETURNLog,
            SIGMOID, CSRank, CSZScore, CSQuantiles, CSMean, CSMeanAdjusted
        ]

        self._cross_section_crossover_list = [
            CSRes, ADDED, SUBBED, MUL, DIV, MINIMUM, MAXIMUM
        ]

    def _init_ts(self):
        self._time_series_mutation_list = [
            EMA, MA, MADecay, MMAX, MARGMAX, MMIN, MARGMIN, MRANK, MQUANTILE,
            MALLTRUE, MANYTRUE, MSUM, MVARIANCE, MSTD, MNPOSITIVE, MAPOSITIVE,
            RSI, MARETURNLog, DELTA, SHIFT
        ]

        self._time_series_crossover_list = [MCORR, MRes, MSharp, MSortino]

    def custom_transformer(self, formula_sets):
        operators_sets = self._crossover_sets + self._mutation_sets

        return [
            operator for operator in operators_sets
            if operator.name in formula_sets
        ]

    def calc_factor(self,
                    expression,
                    total_data,
                    indexs,
                    key,
                    name='transformed',
                    dropna=False):
        return eval(expression).transform(total_data.set_index(indexs),
                                          category_field=key,
                                          name=name,
                                          dropna=dropna)

    def expression_params(self, expression):
        return eval(expression)._dependency

    def fetch_mutation_sets(self):
        return self._mutation_sets

    def fetch_crossover_sets(self):
        return self._crossover_sets


mutation_sets = Operators().fetch_mutation_sets()
crossover_sets = Operators().fetch_crossover_sets()
operators_sets = mutation_sets + crossover_sets
calc_factor = Operators().calc_factor
custom_transformer = Operators().custom_transformer
expression_params = Operators().expression_params
