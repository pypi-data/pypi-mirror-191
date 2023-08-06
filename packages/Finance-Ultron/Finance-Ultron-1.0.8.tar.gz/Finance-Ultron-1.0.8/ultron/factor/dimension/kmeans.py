# -*- encoding:utf-8 -*-
"""
    KMEANS 聚类寻优
"""
import numpy as np
import pandas as pd
from six.moves import xrange
from sklearn import metrics
from sklearn.cluster import KMeans as KmeansImpl
from ultron.utilities.logger import kd_logger
from ultron.kdutils.progress import Progress


class KMeans(object):

    def __init__(self,
                 min=0,
                 max=0,
                 method='squares',
                 features=None,
                 thresh=1):
        if method == 'squares':
            self._k_rng = xrange(min, max) if min != 0 else xrange(
                1, len(features))
        else:
            self._k_rng = xrange(min, max) if min != 0 else xrange(
                2, len(features))
        self._method = method
        self._features = features
        self._thresh = thresh

    def _silhoette_score(self, factors_data, est_arr):
        score = []
        i = 0
        with Progress(len(est_arr), 0, 'evaluate silhoette') as pg:
            for e in est_arr:
                i += 1
                pg.show(i)
                score.append(
                    metrics.silhouette_score(factors_data,
                                             e.labels_,
                                             metric='euclidean'))
        score = pd.Series(score, name='silhouette')
        score = score.sort_values()
        return score

    def _calinski_harabasz_score(self, factors_data, est_arr):
        score = []
        i = 0
        with Progress(len(est_arr), 0, 'evaluate harabasz') as pg:
            for e in est_arr:
                i += 1
                pg.show(i)
                score.append(
                    metrics.calinski_harabasz_score(factors_data, e.labels_))
        score = pd.Series(score, name='harabasz')
        score = score.sort_values()
        return score

    def _squares_score(self, est_arr):
        sum_squares = []
        i = 0
        with Progress(len(est_arr), 0, 'evaluate squares') as pg:
            for e in est_arr:
                i += 1
                pg.show(i)
                sum_squares.append(e.inertia_)
        diff_squares = [squares / sum_squares[0] for squares in sum_squares]
        diff_squares_pd = pd.Series(diff_squares, name='squares')
        score = diff_squares_pd[diff_squares_pd < self._thresh]
        score = score.sort_values()
        return score

    def _kmean_evaluate(self, factors_data, est_arr, method):
        if method == 'silhoette':
            score = self._silhoette_score(factors_data=factors_data,
                                          est_arr=est_arr)
        elif method == 'harabasz':
            score = self._calinski_harabasz_score(factors_data=factors_data,
                                                  est_arr=est_arr)
        elif method == 'squares':
            score = self._squares_score(est_arr=est_arr)

        select_k = self._k_rng[score.index[0]]
        return select_k

    def fit_kmeans(self, factors_data):
        est_arr = []
        i = 0
        with Progress(len(self._k_rng), 0, 'fit kmeans') as pg:
            for k in self._k_rng:
                i += 1
                est_arr.append(KmeansImpl(n_clusters=k).fit(factors_data))
                pg.show(i)
        return est_arr

    def run(self, factors_data):
        diff_cols = [
            col for col in factors_data.columns if col not in self._features
        ]
        kd_logger.info("initialize kmeans range:{0}".format(self._k_rng))
        est_arr = self.fit_kmeans(factors_data[self._features])
        kd_logger.info("{} evaluate kmean best k".format(self._method))
        best_k = self._kmean_evaluate(
            factors_data=factors_data[self._features],
            est_arr=est_arr,
            method=self._method)

        kd_logger.info("kmean best {}".format(best_k))

        est = KmeansImpl(n_clusters=best_k).fit(factors_data[self._features])

        kmeans_clustering_labels = pd.DataFrame(est.labels_,
                                                columns=['cluster'])
        kmeans_data = pd.concat([
            factors_data[diff_cols + self._features], kmeans_clustering_labels
        ],
                                axis=1)
        return kmeans_data