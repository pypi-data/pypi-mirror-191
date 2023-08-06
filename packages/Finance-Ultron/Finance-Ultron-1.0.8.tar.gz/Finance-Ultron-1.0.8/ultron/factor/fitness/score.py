# -*- encoding:utf-8 -*-
import pdb
import numpy as np
import pandas as pd
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from ultron.factor.fitness.metrics import Metrics
from ultron.ump.core.fixes import six


class ScoreTuple(
        namedtuple('ScoreTuple', ('name', 'factors', 'returns', 'freq'))):
    __slots__ = ()

    def __repr__(self):
        return "name:{}\nfreq:{}\nfactors:{}\returns:{}".format(
            self.name, self.freq,
            self.factors.info() if self.factors is not None else 'zero order',
            self.returns.info() if self.returns is not None else 'zero order')


class BaseScorer(six.with_metaclass(ABCMeta, object)):

    def __init__(self, score_tuple_array, *arg, **kwargs):

        self.score_tuple_array = score_tuple_array
        self.score_dict = {}
        self.weights_cnt = -1

        self._init_self_begin(arg, *arg, **kwargs)

        if not hasattr(self, 'select_score_func'):
            raise RuntimeError('_init_self_begin must set select_score_func')
        if not hasattr(self, 'columns_name'):
            raise RuntimeError('_init_self_begin must set columns_name')

        # 如果有设置权重就分配权重否则等权重
        if 'weights' in kwargs and kwargs['weights'] is not None and len(
                kwargs['weights']) == self.weights_cnt:
            self.weights = kwargs['weights']
        else:
            self.weights = self.weights_cnt * [
                1. / self.weights_cnt,
            ]

        if 'metrics_class' in kwargs and kwargs['metrics_class'] is not None \
                and issubclass(kwargs['metrics_class'], Metrics):
            self.metrics_class = kwargs['metrics_class']
        else:
            self.metrics_class = Metrics

        for ind, score_tuple in enumerate(self.score_tuple_array):
            metrics = self.metrics_class(returns=score_tuple.returns,
                                         factors=score_tuple.factors)
            if metrics.valid:
                result = metrics.fit_metrics()
                self.score_dict["{0}_{1}_{2}".format(
                    score_tuple.name, result.long_evaluate.category,
                    result.long_evaluate.freq)] = self.select_score_func(
                        result.long_evaluate)

                self.score_dict["{0}_{1}_{2}".format(
                    score_tuple.name, result.short_evaluate.category,
                    result.short_evaluate.freq)] = self.select_score_func(
                        result.short_evaluate)

                self.score_dict["{0}_{1}_{2}".format(
                    score_tuple.name, result.both_evaluate.category,
                    result.both_evaluate.freq)] = self.select_score_func(
                        result.both_evaluate)

        # 将score_dict转换DataFrame并且转制
        self.score_pd = pd.DataFrame(self.score_dict).T
        # 设置度量指标名称
        self.score_pd.columns = self.columns_name

        self._init_self_end(arg, *arg, **kwargs)

        # 分数每一项都由0-1
        score_ls = np.linspace(0, 1, self.score_pd.shape[0])
        for cn in self.columns_name:
            # 每一项的结果rank后填入对应项
            score = score_ls[(self.score_pd[cn].fillna(0).rank().values -
                              1).astype(int)]
            self.score_pd['score_' + cn] = score

        scores = self.score_pd.filter(regex='score_*')
        # 根据权重计算最后的得分
        self.score_pd['score'] = scores.apply(lambda s:
                                              (s * self.weights).sum(),
                                              axis=1)

    @abstractmethod
    def _init_self_begin(self, *arg, **kwargs):
        """子类需要实现，设置度量项抽取函数select_score_func，度量名称columns_name，weights_cnt"""
        pass

    @abstractmethod
    def _init_self_end(self, *arg, **kwargs):
        """子类需要实现，一般的任务是将score_pd中需要反转的度量结果进行反转"""
        pass

    def fit_score(self):
        """对度量结果按照score排序，返回排序后的score列"""
        self.score_pd.sort_values(by='score', inplace=True)
        return self.score_pd['score']

    def __call__(self):
        """call self.fit_score"""
        return self.fit_score()


class DemoScorer(BaseScorer):

    def _init_self_begin(self, *arg, **kwargs):
        """胜率，策略收益，换手率组成select_score_func"""
        self.select_score_func = lambda metrics: [
            metrics.win_rate, metrics.returns_mean, metrics.turnover
        ]
        self.columns_name = ['win_rate', 'returns_mean', 'turnover']
        self.weights_cnt = len(self.columns_name)

    def _init_self_end(self, *arg, **kwargs):
        """
        _init_self_end这里一般的任务是将score_pd中需要反转的反转，默认是数据越大越好，有些是越小越好，
        类似make_scorer(xxx, greater_is_better=True)中的参数greater_is_better的作用：

                            sign = 1 if greater_is_better else -1
        """
        pass