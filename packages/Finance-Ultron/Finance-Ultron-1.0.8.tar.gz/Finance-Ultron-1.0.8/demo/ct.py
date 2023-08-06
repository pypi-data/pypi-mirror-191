import pickle, pdb
import os, copy, sys, datetime

os.environ['ULTRON_DATA'] = 'keim'
os.environ['IGNORE_WARNINGS'] = '0'
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath('../'))

from ultron.env import *
from ultron.ump.core import env
from ultron.ump.indicator.atr import atr14, atr21
from ultron.ump.market.symbol_pd import _benchmark
from ultron.ump.factor import FactorPreAtrNStop, FactorAtrNStop, FactorCloseAtrNStop, \
    FactorBuyBreak, FactorBuyPutBreak
from ultron.ump.metrics import grid_helper as GridHelper
from ultron.ump.metrics.grid_search import GridSearch
from ultron.ump.metrics.metrics_base import MetricsBase
from ultron.ump.metrics.score import WrsmScorer, BaseScorer
from ultron.ump.metrics.base import MetricsDemo
from matplotlib import pyplot as plt
import seaborn as sns

score_tuple_array = pickle.load(open('score_tuple_array.kpl', 'rb'))


class DemoScorer(BaseScorer):

    def _init_self_begin(self, *arg, **kwargs):
        """胜率，策略收益，alpha组成select_score_func"""
        pdb.set_trace()
        self.select_score_func = lambda metrics: [
            metrics.win_rate, metrics.algorithm_period_returns, metrics.alpha
        ]
        self.columns_name = ['win_rate', 'returns', 'alpha']
        self.weights_cnt = len(self.columns_name)

    def _init_self_end(self, *arg, **kwargs):
        """
        _init_self_end这里一般的任务是将score_pd中需要反转的反转，默认是数据越大越好，有些是越小越好，
        类似make_scorer(xxx, greater_is_better=True)中的参数greater_is_better的作用：

                            sign = 1 if greater_is_better else -1
        """
        self.score_pd['alpha'] = -self.score_pd['alpha']  ## 此处为假设条件


scorer = DemoScorer(score_tuple_array, metrics_class=MetricsDemo)
# 返回按照评分排序后的队列
scorer_returns_max = scorer.fit_score()
scorer.score_pd.sort_values(by='alpha').tail()
