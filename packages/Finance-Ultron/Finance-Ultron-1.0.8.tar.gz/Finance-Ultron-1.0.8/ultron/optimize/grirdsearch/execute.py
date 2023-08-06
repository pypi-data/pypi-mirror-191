# -*- encoding:utf-8 -*-
"""封装常用的分析方式及流程模块"""

import numpy as np
from scipy import interp
from sklearn import metrics
from sklearn import tree
from sklearn.base import ClusterMixin, clone
from sklearn.metrics import roc_curve, auc
from ultron.ump.core.fixes import KFold

__all__ = [
    'run_silhouette_cv_estimator', 'run_prob_cv_estimator', 'run_cv_estimator',
    'plot_learning_curve', 'plot_decision_boundary', 'plot_confusion_matrices',
    'plot_roc_estimator', 'graphviz_tree', 'visualize_tree'
]


# noinspection PyUnresolvedReferences
def run_silhouette_cv_estimator(estimator, x, n_folds=10):
    """
    只针对kmean的cv验证，使用silhouette_score对聚类后的结果labels_
    进行度量使用silhouette_score，kmean的cv验证只是简单的通过np.random.choice
    进行随机筛选x数据进行聚类的silhouette_score度量，并不涉及训练集测试集
    :param estimator: keman或者支持estimator.labels_, 只通过if not isinstance(estimator, ClusterMixin)进行过滤
    :param x: x特征矩阵
    :param n_folds: int，透传KFold参数，切割训练集测试集参数，默认10
    :return: eg: array([ 0.693 ,  0.652 ,  0.6845,  0.6696,  0.6732,  0.6874,  0.668 ,
                         0.6743,  0.6748,  0.671 ])
    """

    if not isinstance(estimator, ClusterMixin):
        print('estimator must be ClusterMixin')
        return

    silhouette_list = list()
    # eg: n_folds = 10, len(x) = 150 -> 150 * 0.9 = 135
    choice_cnt = int(len(x) * ((n_folds - 1) / n_folds))
    choice_source = np.arange(0, x.shape[0])

    # 所有执行fit的操作使用clone一个新的
    estimator = clone(estimator)
    for _ in np.arange(0, n_folds):
        # 只是简单的通过np.random.choice进行随机筛选x数据
        choice_index = np.random.choice(choice_source, choice_cnt)
        x_choice = x[choice_index]
        estimator.fit(x_choice)
        # 进行聚类的silhouette_score度量
        silhouette_score = metrics.silhouette_score(x_choice,
                                                    estimator.labels_,
                                                    metric='euclidean')
        silhouette_list.append(silhouette_score)
    return silhouette_list


def run_prob_cv_estimator(estimator, x, y, n_folds=10):
    """
    通过KFold和参数n_folds拆分训练集和测试集，使用
    np.zeros((len(y), len(np.unique(y))))初始化prob矩阵，
    通过训练estimator.fit(x_train, y_train)后的分类器使用
    predict_proba将y_prob中的对应填数据

    :param estimator: 支持predict_proba的有监督学习, 只通过hasattr(estimator, 'predict_proba')进行过滤
    :param x: 训练集x矩阵，numpy矩阵
    :param y: 训练集y序列，numpy序列
    :param n_folds: int，透传KFold参数，切割训练集测试集参数，默认10
    :return: eg: y_prob
                array([[ 0.8726,  0.1274],
                       [ 0.0925,  0.9075],
                       [ 0.2485,  0.7515],
                       ...,
                       [ 0.3881,  0.6119],
                       [ 0.7472,  0.2528],
                       [ 0.8555,  0.1445]])

    """
    if not hasattr(estimator, 'predict_proba'):
        print('estimator must has predict_proba')
        return

    # 所有执行fit的操作使用clone一个新的
    estimator = clone(estimator)
    kf = KFold(len(y), n_folds=n_folds, shuffle=True)
    y_prob = np.zeros((len(y), len(np.unique(y))))
    """
        根据y序列的数量以及y的label数量构造全是0的矩阵
        eg: y_prob
        array([[ 0.,  0.,  0.],
               [ 0.,  0.,  0.],
               [ 0.,  0.,  0.],
                ..............
               [ 0.,  0.,  0.],
               [ 0.,  0.,  0.],
               [ 0.,  0.,  0.],
    """

    for train_index, test_index in kf:
        x_train, x_test = x[train_index], x[test_index]
        y_train = y[train_index]

        # clf = clone(estimator)
        estimator.fit(x_train, y_train)
        # 使用predict_proba将y_prob中的对应填数据
        y_prob[test_index] = estimator.predict_proba(x_test)

    return y_prob


def run_cv_estimator(estimator, x, y, n_folds=10):
    """
    通过KFold和参数n_folds拆分训练集和测试集，使用
    y.copy()初始化y_pred矩阵，迭代切割好的训练集与测试集，
    不断通过 estimator.predict(x_test)将y_pred中的值逐步替换

    :param estimator: 有监督学习器对象
    :param x: 训练集x矩阵，numpy矩阵
    :param y: 训练集y序列，numpy序列
    :param n_folds: int，透传KFold参数，切割训练集测试集参数，默认10
    :return: y_pred序列
    """
    if not hasattr(estimator, 'predict'):
        print('estimator must has predict')
        return

    # 所有执行fit的操作使用clone一个新的
    estimator = clone(estimator)
    kf = KFold(len(y), n_folds=n_folds, shuffle=True)
    # 首先copy一个一摸一样的y
    y_pred = y.copy()
    """
        eg: y_pred
        array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
               1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
               1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
               2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
               2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
    """

    for train_index, test_index in kf:
        x_train, x_test = x[train_index], x[test_index]
        y_train = y[train_index]
        estimator.fit(x_train, y_train)
        # 通过 estimator.predict(x_test)将y_pred中的值逐步替换
        y_pred[test_index] = estimator.predict(x_test)
    return y_pred
