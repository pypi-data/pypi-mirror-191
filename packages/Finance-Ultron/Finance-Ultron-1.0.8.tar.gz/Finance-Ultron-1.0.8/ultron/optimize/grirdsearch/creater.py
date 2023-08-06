# -*- encoding:utf-8 -*-
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import BaggingRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import SGDRegressor
from sklearn.linear_model import SGDClassifier

from sklearn.neighbors import KNeighborsClassifier
from sklearn.multiclass import OneVsOneClassifier, OneVsRestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from xgboost import XGBRegressor
from lightgbm import LGBMClassifier
from lightgbm import LGBMRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from ultron.ump.core.fixes import GMM

from ultron.optimize.grirdsearch import grid as MLGrid


class MLCreater(object):
    """
        默认使用线性回归初始化回归器:
            self.reg = self.linear_regression()
        默认使用带概率估计的svm初始化分类器:
            self.clf = self.svc(probability=True)

        默认无简单学习器：hmm，pca，keman全部初始None值
    """

    def __init__(self):
        self._regressor = self.linear_regression()
        self._classifier = self.svc(probability=True)

        # 无监督机器学习，pca，聚类，hmm, 默认不初始化
        self._hmm = None
        self._pca = None
        self._kmean = None

    def __str__(self):
        """打印对象显示：reg, clf, hmm, pca, kmean"""
        return "reg: {}\nclf: {}\nhmm: {}\npca: {}\nkmean: {}\n".format(
            self._regressor, self._classifier, self._hmm, self._pca,
            self._kmean)

    def linear_regression(self, assign=True, **kwargs):
        """
        有监督学习回归器，实例化LinearRegression，默认使用：
            LinearRegression()

        通过**kwargs即关键字参数透传LinearRegression，即:
            LinearRegression(**kwargs)

        :param assign: 是否保存实例后的LinearRegression对象，默认True，self.reg = reg
        :param kwargs: 有参数情况下初始化: LinearRegression(**kwargs)
                       无参数情况下初始化: LinearRegression()

        :return: 实例化的LinearRegression对象
        """
        if kwargs is not None and len(kwargs) > 0:
            regressor = LinearRegression(**kwargs)
        else:
            regressor = LinearRegression()
        if assign:
            self._regressor = regressor
        return regressor

    def svc(self, assign=True, **kwargs):
        """
        有监督学习分类器，实例化SVC，默认使用：
            SVC(kernel='rbf', probability=True)

        通过**kwargs即关键字参数透传SVC，即:
            SVC(**kwargs)

        :param assign: 是否保存实例后的RandomForestRegressor对象，默认True，self.clf = clf
        :param kwargs: 有参数情况下初始化: SVC(**kwargs)
                       无参数情况下初始化: SVC(kernel='rbf', probability=True)

        :return: 实例化的SVC对象
        """
        if kwargs is not None and len(kwargs) > 0:
            classifier = SVC(**kwargs)
        else:
            classifier = SVC(kernel='rbf', probability=True)
        if assign:
            self._classifier = classifier
        return classifier

    def pca_decomposition(self, assign=True, **kwargs):
        """
        无监督学习器，实例化PCA，默认使用pca = PCA(0.95)，通过**kwargs即
        关键字参数透传PCA，即PCA(**kwargs)

        :param assign: 是否保存实例后的PCA对象，默认True，self.pca = pca
        :param kwargs: 有参数情况下初始化: PCA(**kwargs)
                       无参数情况下初始化: pca = PCA(0.95)
        :return: 实例化的PCA对象
        """
        if kwargs is not None and len(kwargs) > 0:
            pca = PCA(**kwargs)
        else:
            # 没参数直接要保留95%
            pca = PCA(0.95)
        if assign:
            self._pca = pca

        return pca

    def kmean_cluster(self, assign=True, **kwargs):
        """
        无监督学习器，实例化KMeans，默认使用KMeans(n_clusters=2, random_state=0)，
        通过**kwargs即关键字参数透传KMeans，即KMeans(**kwargs)

        :param assign: 是否保存实例后的kmean对象，默认True，self.kmean = kmean
        :param kwargs: 有参数情况下初始化: KMeans(**kwargs)
                       无参数情况下初始化: KMeans(n_clusters=2, random_state=0)
        :return: 实例化的KMeans对象
        """
        if kwargs is not None and len(kwargs) > 0:
            kmean = KMeans(**kwargs)
        else:
            # 默认也只有两个n_clusters
            kmean = KMeans(n_clusters=2, random_state=0)
        if assign:
            self._kmean = kmean
        return kmean

    def hmm_gaussian(self, assign=True, **kwargs):
        """
        无监督学习器，实例化GMM，默认使用GMM(n_components=2)，通过**kwargs即
        关键字参数透传GMM，即GMM(**kwargs)

        导入模块使用
            try:
                from hmmlearn.hmm import GaussianHMM as GMM
            except ImportError:
                from ..CoreBu.u'l't'r'o'nFixes import GMM
        即优先选用hmmlearn中的GaussianHMM，没有安装的情况下使用sklearn中的GMM

        :param assign: 是否保存实例后的hmm对象，默认True，self.hmm = hmm
        :param kwargs: 有参数情况下初始化: GMM(**kwargs)
                       无参数情况下初始化: GMM(n_components=2)
        :return: 实例化的GMM对象
        """
        if kwargs is not None and len(kwargs) > 0:
            hmm = GMM(**kwargs)
        else:
            # 默认只有n_components=2, 两个分类
            hmm = GMM(n_components=2)
        if assign:
            self._hmm = hmm
        return hmm

    def _estimators_prarms_best(
            self,
            create_func,
            x,
            y,
            param_grid,
            assign,
            n_jobs,
            grid_callback=MLGrid.grid_search_init_n_estimators):
        """
        封装使用MLGrid寻找针对学习器的最优参数值，针对不同学习器，选择不同的
        关键字参数做最优搜索，将寻找到的最优参数做为**kwargs用来重新构造学习器

        :param create_func: callable, 学习器函数构造器，eg：self.adaboost_classifier
        :param x: 训练集x矩阵，numpy矩阵
        :param y: 训练集y序列，numpy序列
        :param param_grid: 最优字典关键字参数，使用grid_search_mul_init_kwargs寻找参数最优值：
                        eg: _, best_params = MLGrid.grid_search_mul_init_kwargs(estimator, x, y,
                                                       param_grid=param_grid, n_jobs=n_jobs)
        :param assign: 是否保存实例化后最优参数的学习器对象，默认True，透传create_func，用来根据最优参数重新构造学习器保存在类变量
                        eg: create_func(assign=assign, **best_params)
        :param grid_callback: 如果没有有传递最优字典关键字参数param_grid，使用学习器对应的grid_callback函数，搜索特定的最优参数
                              默认MLGrid.grid_search_init_n_estimators
        :return: 通过最优参数构造的学习器对象，eg: create_func(assign=assign, **best_params)
        """
        # 通过create_func创建一个示例学习器，assign=False
        estimator = create_func(assign=False)
        if param_grid is not None and isinstance(param_grid, dict):
            # 如果有传递最优字典关键字参数，使用grid_search_mul_init_kwargs寻找参数最优值
            grid, _, best_params = MLGrid.grid_search_mul_init_kwargs(
                estimator, x, y, param_grid=param_grid, n_jobs=n_jobs)
        else:
            # 如果没有有传递最优字典关键字参数，使用学习器对应的grid_callback函数，默认UltronMLGrid.grid_search_init_n_estimators
            grid, _, best_params = grid_callback(estimator, x, y)

        if best_params is not None:
            # 将寻找到的最优参数best_params，做为参数重新传递create_func(assign=assign, **best_params)
            self.grid = grid
            return create_func(assign=assign, **best_params)

    def bagging_classifier(self,
                           assign=True,
                           base_estimator=DecisionTreeClassifier(),
                           **kwargs):
        """
        有监督学习分类器，实例化BaggingClassifier，默认使用：
            BaggingClassifier(base_estimator=base_estimator, n_estimators=200,
                              bootstrap=True, oob_score=True, random_state=1)

        通过**kwargs即关键字参数透传BaggingClassifier，即:
            BaggingClassifier(**kwargs)

        :param base_estimator: 默认使用DecisionTreeClassifier()
        :param assign: 是否保存实例后的BaggingClassifier对象，默认True，self.clf = clf
        :param kwargs: 有参数情况下初始化: BaggingClassifier(**kwargs)
                       无参数情况下初始化: BaggingClassifier(base_estimator=base_estimator, n_estimators=200,
                                                           bootstrap=True, oob_score=True, random_state=1)
        :return: 实例化的BaggingClassifier对象
        """
        if kwargs is not None and len(kwargs) > 0:
            if 'base_estimator' not in kwargs:
                kwargs['base_estimator'] = base_estimator
            classifier = BaggingClassifier(**kwargs)
        else:
            classifier = BaggingClassifier(base_estimator=base_estimator,
                                           n_estimators=200,
                                           bootstrap=True,
                                           oob_score=True,
                                           random_state=1)
        if assign:
            self._classifier = classifier
        return classifier

    def bagging_classifier_best(self,
                                x,
                                y,
                                param_grid=None,
                                assign=True,
                                n_jobs=-1):
        """
        寻找BaggingClassifier构造器的最优参数
        上层中bagging_classifier_best函数，直接使用ML中的x，y数据调用
        :param x: 训练集x矩阵，numpy矩阵
        :param y: 训练集y序列，numpy序列
        :param param_grid: 最优字典关键字参数，
                        eg：param_grid = {'max_samples': np.arange(1, 5), 'n_estimators': np.arange(100, 300, 50)}
        :param assign: 是否保存实例化后最优参数的学习器对象，默认True
        :param n_jobs: 并行执行的进程任务数量，默认-1, 开启与cpu相同数量的进程数
        :return: 通过最优参数构造的BaggingClassifier对象
        """
        return self._estimators_prarms_best(self.bagging_classifier, x, y,
                                            param_grid, assign, n_jobs)

    def bagging_regressor(self,
                          assign=True,
                          base_estimator=DecisionTreeRegressor(),
                          **kwargs):
        """
        有监督学习回归器，实例化BaggingRegressor，默认使用：
            BaggingRegressor(base_estimator=base_estimator, n_estimators=200,
                             bootstrap=True, oob_score=True, random_state=1)

        通过**kwargs即关键字参数透传BaggingRegressor，即:
            BaggingRegressor(**kwargs)

        :param base_estimator: 默认使用DecisionTreeRegressor()
        :param assign: 是否保存实例后的BaggingRegressor对象，默认True，self.reg = reg
        :param kwargs: 有参数情况下初始化: BaggingRegressor(**kwargs)
                       无参数情况下初始化: BaggingRegressor(base_estimator=base_estimator, reg_core, n_estimators=200,
                                                          bootstrap=True, oob_score=True, random_state=1)
        :return: 实例化的BaggingRegressor对象
        """
        if kwargs is not None and len(kwargs) > 0:
            if 'base_estimator' not in kwargs:
                kwargs['base_estimator'] = base_estimator
            regressor = BaggingRegressor(**kwargs)
        else:
            regressor = BaggingRegressor(base_estimator=base_estimator,
                                         n_estimators=200,
                                         bootstrap=True,
                                         oob_score=True,
                                         random_state=1)

        if assign:
            self._regressor = regressor
        return regressor

    def bagging_regressor_best(self,
                               x,
                               y,
                               param_grid=None,
                               assign=True,
                               n_jobs=-1):
        """
        寻找BaggingRegressor构造器的最优参数
        上层UltronML中bagging_regressor_best函数，直接使用UltronML中的x，y数据调用
        
        :param x: 训练集x矩阵，numpy矩阵
        :param y: 训练集y序列，numpy序列
        :param param_grid: 最优字典关键字参数，
                        eg：param_grid = {'max_samples': np.arange(1, 5), 'n_estimators': np.arange(100, 300, 50)}
        :param assign: 是否保存实例化后最优参数的学习器对象，默认True
        :param n_jobs: 并行执行的进程任务数量，默认-1, 开启与cpu相同数量的进程数
        :return: 通过最优参数构造的BaggingRegressor对象
        """
        return self._estimators_prarms_best(self.bagging_regressor, x, y,
                                            param_grid, assign, n_jobs)

    def adaboost_regressor(self,
                           assign=True,
                           base_estimator=DecisionTreeRegressor(),
                           **kwargs):
        """
        有监督学习回归器，实例化AdaBoostRegressor，默认使用：
            AdaBoostRegressor(base_estimator=base_estimator, n_estimators=100, random_state=1)

        通过**kwargs即关键字参数透传AdaBoostRegressor，即:
            AdaBoostRegressor(**kwargs)

        :param base_estimator: 默认使用DecisionTreeRegressor()
        :param assign: 是否保存实例后的AdaBoostRegressor对象，默认True，self.reg = reg
        :param kwargs: 有参数情况下初始化: AdaBoostRegressor(**kwargs)
                       无参数情况下初始化: AdaBoostRegressor(n_estimators=100, random_state=1)

        :return: 实例化的AdaBoostRegressor对象
        """
        if kwargs is not None and len(kwargs) > 0:
            if 'base_estimator' not in kwargs:
                kwargs['base_estimator'] = base_estimator
            regressor = AdaBoostRegressor(**kwargs)
        else:
            regressor = AdaBoostRegressor(base_estimator=base_estimator,
                                          n_estimators=100,
                                          random_state=1)

        if assign:
            self._regressor = regressor

        return regressor

    def adaboost_regressor_best(self,
                                x,
                                y,
                                param_grid=None,
                                assign=True,
                                n_jobs=-1):
        """
        寻找AdaBoostRegressor构造器的最优参数

        上层UltronML中adaboost_regressor_best函数，直接使用UltronML中的x，y数据调用


        :param x: 训练集x矩阵，numpy矩阵
        :param y: 训练集y序列，numpy序列
        :param param_grid: 最优字典关键字参数，
                        eg：param_grid = {'learning_rate': np.arange(0.2, 1.2, 0.2),
                                         'n_estimators': np.arange(10, 100, 10)}
        :param assign: 是否保存实例化后最优参数的学习器对象，默认True
        :param n_jobs: 并行执行的进程任务数量，默认-1, 开启与cpu相同数量的进程数
        :return: 通过最优参数构造的AdaBoostRegressor对象
        """
        return self._estimators_prarms_best(self.adaboost_regressor, x, y,
                                            param_grid, assign, n_jobs)

    def adaboost_classifier(self,
                            assign=True,
                            base_estimator=DecisionTreeClassifier(),
                            **kwargs):
        """
        有监督学习分类器，实例化AdaBoostClassifier，默认使用：
            AdaBoostClassifier(base_estimator=base_estimator, n_estimators=100, random_state=1)

        通过**kwargs即关键字参数透传AdaBoostClassifier，即:
            AdaBoostClassifier(**kwargs)

        :param base_estimator: 默认使用DecisionTreeClassifier()
        :param assign: 是否保存实例后的AdaBoostClassifier对象，默认True，self.clf = clf
        :param kwargs: 有参数情况下初始化: AdaBoostClassifier(**kwargs)
                       无参数情况下初始化: AdaBoostClassifier(n_estimators=100, random_state=1)

        :return: 实例化的AdaBoostClassifier对象
        """
        if kwargs is not None and len(kwargs) > 0:
            if 'base_estimator' not in kwargs:
                kwargs['base_estimator'] = base_estimator
            classifier = AdaBoostClassifier(**kwargs)
        else:
            classifier = AdaBoostClassifier(base_estimator=base_estimator,
                                            n_estimators=100,
                                            random_state=1)
        if assign:
            self._classifier = classifier
        return classifier

    def adaboost_classifier_best(self,
                                 x,
                                 y,
                                 param_grid=None,
                                 assign=True,
                                 n_jobs=-1):
        """
        寻找AdaBoostClassifier构造器的最优参数

        上层UltronML中adaboost_classifier_best函数，直接使用UltronML中的x，y数据调用

        :param x: 训练集x矩阵，numpy矩阵
        :param y: 训练集y序列，numpy序列
        :param param_grid: 最优字典关键字参数，
                     eg：param_grid = {'learning_rate': np.arange(0.2, 1.2, 0.2),
                                       'n_estimators': np.arange(10, 100, 10)}
        :param assign: 是否保存实例化后最优参数的学习器对象，默认True
        :param n_jobs: 并行执行的进程任务数量，默认-1, 开启与cpu相同数量的进程数
        :return: 通过最优参数构造的AdaBoostClassifier对象
        """
        return self._estimators_prarms_best(self.adaboost_classifier, x, y,
                                            param_grid, assign, n_jobs)

    def gradient_boosting_regressor(self, assign=True, **kwargs):
        """
        有监督学习回归器，默认使用：
                        GradientBoostingRegressor(n_estimators=100)
        通过**kwargs即关键字参数透传GBR(**kwargs)，即:
                        GradientBoostingRegressor(**kwargs)

        :param assign: 是否保存实例后的回归器对象，默认True，self.reg = reg
        :param kwargs: 有参数情况下初始化: GBR(n_estimators=100)
                       无参数情况下初始化: GBR(**kwargs)

        :return: 实例化的GradientBoostingRegressor对象
        """
        if kwargs is not None and len(kwargs) > 0:
            regressor = GradientBoostingRegressor(**kwargs)
        else:
            regressor = GradientBoostingRegressor(n_estimators=100)
        if assign:
            self._regressor = regressor
        return regressor

    def gradient_boosting_regressor_best(self,
                                         x,
                                         y,
                                         param_grid=None,
                                         assign=True,
                                         n_jobs=-1):
        """
        寻找GradientBoostingRegressor构造器的最优参数

        上层UltronML中xgb_regressor_best函数，直接使用UltronML中的x，y数据调用

        :param x: 训练集x矩阵，numpy矩阵
        :param y: 训练集y序列，numpy序列
        :param param_grid: 最优字典关键字参数，
                     eg：param_grid = {'learning_rate': np.arange(0.1, 0.5, 0.05),
                                      'n_estimators': np.arange(10, 100, 10)}
        :param assign: 是否保存实例化后最优参数的学习器对象，默认True
        :param n_jobs: 并行执行的进程任务数量，默认-1, 开启与cpu相同数量的进程数
        :return: 通过最优参数构造的GradientBoostingRegressor对象
        """
        return self._estimators_prarms_best(self.gradient_boosting_regressor,
                                            x, y, param_grid, assign, n_jobs)

    def gradient_boosting_classifier(self, assign=True, **kwargs):
        """
        有监督学习分类器，默认使用：
                        GradientBoostingClassifier(n_estimators=100)

        通过**kwargs即关键字参数透传GradientBoostingClassifier(**kwargs)，即:
                        GradientBoostingClassifier(**kwargs)

        :param assign: 是否保存实例后的分类器对象，默认True，self.clf = clf
        :param kwargs: 有参数情况下初始化: GradientBoostingClassifier(n_estimators=100)
                       无参数情况下初始化: GradientBoostingClassifier(**kwargs)

        :return: 实例化的GradientBoostingClassifier对象
        """
        if kwargs is not None and len(kwargs) > 0:
            classifier = GradientBoostingClassifier(**kwargs)
        else:
            classifier = GradientBoostingClassifier(n_estimators=100)
        if assign:
            self._classifier = classifier
        return classifier

    def gradient_boosting_classifier_best(self,
                                          x,
                                          y,
                                          param_grid=None,
                                          assign=True,
                                          n_jobs=-1):
        """
        寻找GradientBoostingClassifier构造器的最优参数

        上层UltronML中xgb_classifier_best函数，直接使用UltronML中的x，y数据调用

        :param x: 训练集x矩阵，numpy矩阵
        :param y: 训练集y序列，numpy序列
        :param param_grid: 最优字典关键字参数，
                     eg：param_grid = {'learning_rate': np.arange(0.1, 0.5, 0.05),
                                      'n_estimators': np.arange(50, 200, 10)}
        :param assign: 是否保存实例化后最优参数的学习器对象，默认True
        :param n_jobs: 并行执行的进程任务数量，默认-1, 开启与cpu相同数量的进程数
        :return: 通过最优参数构造的GradientBoostingClassifier对象
        """
        return self._estimators_prarms_best(self.gradient_boosting_classifier,
                                            x, y, param_grid, assign, n_jobs)

    def xgboost_regressor(self, assign=True, **kwargs):
        """
        有监督学习回归器，实例化XGBRegressor，默认使用：
            XGBRegressor(n_estimators=100)

        通过**kwargs即关键字参数透传XGBRegressor，即:
            XGBRegressor(**kwargs)

        :param assign: 是否保存实例后的XGBRegressor对象，默认True，self.reg = reg
        :param kwargs: 有参数情况下初始化: XGBRegressor(**kwargs)
                       无参数情况下初始化: XGBRegressor(n_estimators=100)

        :return: 实例化的XGBRegressor 对象
        """
        if kwargs is not None and len(kwargs) > 0:
            regressor = XGBRegressor(**kwargs)
        else:
            regressor = XGBRegressor(n_estimators=100)
        if assign:
            self._regressor = regressor
        return regressor

    def xgboost_regressor_best(self,
                               x,
                               y,
                               param_grid=None,
                               assign=True,
                               n_jobs=-1):
        """
        寻找XGBRegressor构造器的最优参数

        上层UltronML中xgboost_regressor_best函数，直接使用UltronML中的x，y数据调用

        :param x: 训练集x矩阵，numpy矩阵
        :param y: 训练集y序列，numpy序列
        :param param_grid: 最优字典关键字参数，
                     eg：param_grid = {'learning_rate': np.arange(0.1, 0.5, 0.05),
                                      'n_estimators': np.arange(50, 200, 10)}
        :param assign: 是否保存实例化后最优参数的学习器对象，默认True
        :param n_jobs: 并行执行的进程任务数量，默认-1, 开启与cpu相同数量的进程数
        :return: 通过最优参数构造的XGBRegressor对象
        """
        return self._estimators_prarms_best(self.xgboost_regressor, x, y,
                                            param_grid, assign, n_jobs)

    def xgboost_classifier(self, assign=True, **kwargs):
        """
        有监督学习分类，实例化XGBClassifier，默认使用：
            XGBClassifier(n_estimators=100)

        通过**kwargs即关键字参数透传XGBClassifier，即:
            XGBClassifier(**kwargs)

        :param assign: 是否保存实例后的XGBClassifier对象，默认True，self.reg = reg
        :param kwargs: 有参数情况下初始化: XGBClassifier(**kwargs)
                       无参数情况下初始化: XGBClassifier(n_estimators=100)

        :return: 实例化的XGBClassifier 对象
        """
        if kwargs is not None and len(kwargs) > 0:
            regressor = XGBClassifier(**kwargs)
        else:
            regressor = XGBClassifier(n_estimators=100)
        if assign:
            self._regressor = regressor
        return regressor

    def xgboost_classifier_best(self,
                                x,
                                y,
                                param_grid=None,
                                assign=True,
                                n_jobs=-1):
        """
        寻找XGBRegressor构造器的最优参数

        上层UltronML中xgboost_classifier_best函数，直接使用UltronML中的x，y数据调用

        :param x: 训练集x矩阵，numpy矩阵
        :param y: 训练集y序列，numpy序列
        :param param_grid: 最优字典关键字参数，
                     eg：param_grid = {'learning_rate': np.arange(0.1, 0.5, 0.05),
                                      'n_estimators': np.arange(50, 200, 10)}
        :param assign: 是否保存实例化后最优参数的学习器对象，默认True
        :param n_jobs: 并行执行的进程任务数量，默认-1, 开启与cpu相同数量的进程数
        :return: 通过最优参数构造的XGBClassifier对象
        """
        return self._estimators_prarms_best(self.xgboost_classifier, x, y,
                                            param_grid, assign, n_jobs)

    def lgbm_regressor(self, assign=True, **kwargs):
        """
        有监督学习回归器，实例化LGBMRegressor，默认使用：
            LGBMRegressor(n_estimators=100)

        通过**kwargs即关键字参数透传XGBRegressor，即:
            LGBMRegressor(**kwargs)

        :param assign: 是否保存实例后的LGBMRegressor对象，默认True，self.reg = reg
        :param kwargs: 有参数情况下初始化: LGBMRegressor(**kwargs)
                       无参数情况下初始化: LGBMRegressor(n_estimators=100)

        :return: 实例化的LGBMRegressor 对象
        """
        if kwargs is not None and len(kwargs) > 0:
            regressor = LGBMRegressor(**kwargs)
        else:
            regressor = LGBMRegressor(n_estimators=100)
        if assign:
            self._regressor = regressor
        return regressor

    def lgbm_regressor_best(self,
                            x,
                            y,
                            param_grid=None,
                            assign=True,
                            n_jobs=-1):
        """
        寻找XGBRegressor构造器的最优参数

        上层UltronML中lgbm_regressor_best函数，直接使用UltronML中的x，y数据调用

        :param x: 训练集x矩阵，numpy矩阵
        :param y: 训练集y序列，numpy序列
        :param param_grid: 最优字典关键字参数，
                     eg：param_grid = {'learning_rate': np.arange(0.1, 0.5, 0.05),
                                      'n_estimators': np.arange(50, 200, 10)}
        :param assign: 是否保存实例化后最优参数的学习器对象，默认True
        :param n_jobs: 并行执行的进程任务数量，默认-1, 开启与cpu相同数量的进程数
        :return: 通过最优参数构造的GradientBoostingClassifier对象
        """
        return self._estimators_prarms_best(self.lgbm_regressor, x, y,
                                            param_grid, assign, n_jobs)

    def lgbm_classifier(self, assign=True, **kwargs):
        """
        有监督学习分类，实例化LGBMClassifier，默认使用：
            LGBMClassifier(n_estimators=100)

        通过**kwargs即关键字参数透传LGBMClassifier，即:
            LGBMClassifier(**kwargs)

        :param assign: 是否保存实例后的LGBMClassifier对象，默认True，self.reg = reg
        :param kwargs: 有参数情况下初始化: LGBMClassifier(**kwargs)
                       无参数情况下初始化: LGBMClassifier(n_estimators=100)

        :return: 实例化的LGBMClassifier 对象
        """
        if kwargs is not None and len(kwargs) > 0:
            regressor = LGBMClassifier(**kwargs)
        else:
            regressor = LGBMClassifier(n_estimators=100)
        if assign:
            self._regressor = regressor
        return regressor

    def lgbm_classifier_best(self,
                             x,
                             y,
                             param_grid=None,
                             assign=True,
                             n_jobs=-1):
        """
        寻找LGBMClassifier构造器的最优参数

        上层UltronML中xgb_classifier_best函数，直接使用UltronML中的x，y数据调用
        eg：
             xgb_boost_regressor_best无param_grid参数调用：

             from Ultronpy import UltronML, ml
             ttn_Ultron = UltronML.create_test_more_fiter()
             ttn_Ultron.xgb_classifier_best()

             xgb_classifier_best有param_grid参数调用：

             param_grid = {'learning_rate': np.arange(0.1, 0.5, 0.05), 'n_estimators': np.arange(50, 200, 10)}
             ttn_Ultron.xgb_classifier_best(param_grid=param_grid, n_jobs=-1)

             out: GradientBoostingClassifier(learning_rate=0.1, n_estimators=160)

        :param x: 训练集x矩阵，numpy矩阵
        :param y: 训练集y序列，numpy序列
        :param param_grid: 最优字典关键字参数，
                     eg：param_grid = {'learning_rate': np.arange(0.1, 0.5, 0.05),
                                      'n_estimators': np.arange(50, 200, 10)}
        :param assign: 是否保存实例化后最优参数的学习器对象，默认True
        :param n_jobs: 并行执行的进程任务数量，默认-1, 开启与cpu相同数量的进程数
        :return: 通过最优参数构造的GradientBoostingClassifier对象
        """
        return self._estimators_prarms_best(self.lgbm_classifier, x, y,
                                            param_grid, assign, n_jobs)

    def lasso_regressor(self, assign=True, **kwargs):
        """
        有监督学习回归器，实例化Lasso，默认使用：
            Lasso(n_estimators=100)

        通过**kwargs即关键字参数透传Lasso，即:
            Lasso(**kwargs)

        :param assign: 是否保存实例后的Lasso对象，默认True，self.reg = reg
        :param kwargs: 有参数情况下初始化: Lasso(**kwargs)
                       无参数情况下初始化: Lasso(fit_intercept=True)

        :return: 实例化的Lasso对象
        """
        if kwargs is not None and len(kwargs) > 0:
            regressor = Lasso(**kwargs)
        else:
            regressor = Lasso(fit_intercept=True)
        if assign:
            self._regressor = regressor
        return regressor

    def lasso_regressor_best(self,
                             x,
                             y,
                             param_grid=None,
                             assign=True,
                             n_jobs=-1):
        """
        寻找RLasso构造器的最优参数

        上层UltronML中lasso_regressor_best函数，直接使用UltronML中的x，y数据调用
        :param x: 训练集x矩阵，numpy矩阵
        :param y: 训练集y序列，numpy序列
        :param param_grid: 最优字典关键字参数，
                     eg：param_grid = {'max_features': ['sqrt', 'log2', ],
                                      'n_estimators': np.arange(10, 150, 15)}
        :param assign: 是否保存实例化后最优参数的学习器对象，默认True
        :param n_jobs: 并行执行的进程任务数量，默认-1, 开启与cpu相同数量的进程数
        :return: 通过最优参数构造的RandomForestRegressor对象
        """
        return self._estimators_prarms_best(self.lasso_regressor, x, y,
                                            param_grid, assign, n_jobs)

    def sgd_regressor(self, assign=True, **kwargs):
        """
        有监督学习回归器，实例化SGDRegressor，默认使用：
            SGDRegressor(n_estimators=100)

        通过**kwargs即关键字参数透传SGDRegressor，即:
            SGDRegressor(**kwargs)

        :param assign: 是否保存实例后的SGDRegressor对象，默认True，self.reg = reg
        :param kwargs: 有参数情况下初始化: SGDRegressor(**kwargs)
                       无参数情况下初始化: SGDRegressor(fit_intercept=True)

        :return: 实例化的SGDRegressor对象
        """
        if kwargs is not None and len(kwargs) > 0:
            regressor = SGDRegressor(**kwargs)
        else:
            regressor = SGDRegressor(fit_intercept=True)
        if assign:
            self._regressor = regressor
        return regressor

    def sgd_regressor_best(self,
                           x,
                           y,
                           param_grid=None,
                           assign=True,
                           n_jobs=-1):
        """
        寻找SGDRegressor构造器的最优参数

        上层UltronML中sgd_regressor_best函数，直接使用UltronML中的x，y数据调用

        :param x: 训练集x矩阵，numpy矩阵
        :param y: 训练集y序列，numpy序列
        :param param_grid: 最优字典关键字参数，
                     eg：param_grid = {'max_features': ['sqrt', 'log2', ],
                                      'n_estimators': np.arange(10, 150, 15)}
        :param assign: 是否保存实例化后最优参数的学习器对象，默认True
        :param n_jobs: 并行执行的进程任务数量，默认-1, 开启与cpu相同数量的进程数
        :return: 通过最优参数构造的SGDRegressor对象
        """
        return self._estimators_prarms_best(self.sgd_regressor, x, y,
                                            param_grid, assign, n_jobs)

    def sgd_classifier(self, assign=True, **kwargs):
        """
        有监督学习回归器，实例化SGDClassifier，默认使用：
            SGDClassifier(fit_intercept=True)

        通过**kwargs即关键字参数透传SGDClassifier，即:
            SGDClassifier(**kwargs)

        :param assign: 是否保存实例后的SGDClassifier对象，默认True，self.reg = reg
        :param kwargs: 有参数情况下初始化: SGDClassifier(**kwargs)
                       无参数情况下初始化: SGDClassifier(fit_intercept=True)

        :return: 实例化的SGDClassifier对象
        """
        if kwargs is not None and len(kwargs) > 0:
            classifier = SGDClassifier(**kwargs)
        else:
            classifier = SGDClassifier(fit_intercept=True)
        if assign:
            self._classifier = classifier
        return classifier

    def sgd_classifier_best(self,
                            x,
                            y,
                            param_grid=None,
                            assign=True,
                            n_jobs=-1):
        """
        寻找SGDClassifier构造器的最优参数

        :param x: 训练集x矩阵，numpy矩阵
        :param y: 训练集y序列，numpy序列
        :param param_grid: 最优字典关键字参数，
                     eg：param_grid = {'max_features': ['sqrt', 'log2', ],
                                      'n_estimators': np.arange(10, 150, 15)}
        :param assign: 是否保存实例化后最优参数的学习器对象，默认True
        :param n_jobs: 并行执行的进程任务数量，默认-1, 开启与cpu相同数量的进程数
        :return: 通过最优参数构造的SGDClassifier对象
        """
        return self._estimators_prarms_best(self.sgd_classifier, x, y,
                                            param_grid, assign, n_jobs)

    def random_forest_regressor(self, assign=True, **kwargs):
        """
        有监督学习回归器，实例化RandomForestRegressor，默认使用：
            RandomForestRegressor(n_estimators=100)

        通过**kwargs即关键字参数透传RandomForestRegressor，即:
            RandomForestRegressor(**kwargs)

        :param assign: 是否保存实例后的RandomForestRegressor对象，默认True，self.reg = reg
        :param kwargs: 有参数情况下初始化: RandomForestRegressor(**kwargs)
                       无参数情况下初始化: RandomForestRegressor(n_estimators=100)

        :return: 实例化的RandomForestRegressor对象
        """
        if kwargs is not None and len(kwargs) > 0:
            regressor = RandomForestRegressor(**kwargs)
        else:
            regressor = RandomForestRegressor(n_estimators=100)
        if assign:
            self._regressor = regressor
        return regressor

    def random_forest_regressor_best(self,
                                     x,
                                     y,
                                     param_grid=None,
                                     assign=True,
                                     n_jobs=-1):
        """
        寻找RandomForestRegressor构造器的最优参数

        上层UltronML中random_forest_regressor_best函数，直接使用UltronML中的x，y数据调用

        :param x: 训练集x矩阵，numpy矩阵
        :param y: 训练集y序列，numpy序列
        :param param_grid: 最优字典关键字参数，
                     eg：param_grid = {'max_features': ['sqrt', 'log2', ],
                                      'n_estimators': np.arange(10, 150, 15)}
        :param assign: 是否保存实例化后最优参数的学习器对象，默认True
        :param n_jobs: 并行执行的进程任务数量，默认-1, 开启与cpu相同数量的进程数
        :return: 通过最优参数构造的RandomForestRegressor对象
        """
        return self._estimators_prarms_best(self.random_forest_regressor, x, y,
                                            param_grid, assign, n_jobs)

    def random_forest_classifier(self, assign=True, **kwargs):
        """
        有监督学习分类器，实例化RandomForestClassifier，默认使用：
            RandomForestRegressor(n_estimators=100)

        通过**kwargs即关键字参数透传RandomForestRegressor，即:
            RandomForestRegressor(**kwargs)

        :param assign: 是否保存实例后的RandomForestRegressor对象，默认True，self.reg = reg
        :param kwargs: 有参数情况下初始化: RandomForestRegressor(**kwargs)
                       无参数情况下初始化: RandomForestRegressor(n_estimators=100)

        :return: 实例化的RandomForestRegressor对象
        """
        if kwargs is not None and len(kwargs) > 0:
            classifier = RandomForestClassifier(**kwargs)
        else:
            classifier = RandomForestClassifier(n_estimators=100)
        if assign:
            self._classifier = classifier
        return classifier

    def random_forest_classifier_best(self,
                                      x,
                                      y,
                                      param_grid=None,
                                      assign=True,
                                      n_jobs=-1):
        """
        寻找RandomForestClassifier构造器的最优参数

        上层UltronML中random_forest_classifier_best函数，直接使用UltronML中的x，y数据调用

        :param x: 训练集x矩阵，numpy矩阵
        :param y: 训练集y序列，numpy序列
        :param param_grid: 最优字典关键字参数，
                     eg：param_grid = {'max_features': ['sqrt', 'log2', ],
                                      'n_estimators': np.arange(50, 200, 20)}
        :param assign: 是否保存实例化后最优参数的学习器对象，默认True
        :param n_jobs: 并行执行的进程任务数量，默认-1, 开启与cpu相同数量的进程数
        :return: 通过最优参数构造的RandomForestClassifier对象
        """
        return self._estimators_prarms_best(self.random_forest_classifier, x,
                                            y, param_grid, assign, n_jobs)

    def extra_tree_regressor(self, assign=True, **kwargs):
        """
        有监督学习回归器，实例化ExtraTreesRegressor，默认使用：
            ExtraTreesRegressor(max_depth=2, random_state=1)

        通过**kwargs即关键字参数透传ExtraTreesRegressor，即:
            ExtraTreesRegressor(**kwargs)

        :param assign: 是否保存实例后的ExtraTreesRegressor对象，默认True，self.reg = reg
        :param kwargs: 有参数情况下初始化: ExtraTreesRegressor(**kwargs)
                       无参数情况下初始化: ExtraTreesRegressor(max_depth=2, random_state=1)

        :return: 实例化的ExtraTreesRegressor对象
        """
        if kwargs is not None and len(kwargs) > 0:
            regressor = ExtraTreesRegressor(**kwargs)
        else:
            regressor = ExtraTreesRegressor(max_depth=2, random_state=1)
        if assign:
            self._regressor = regressor
        return regressor

    def extra_tree_regressor_best(self,
                                  x,
                                  y,
                                  param_grid=None,
                                  assign=True,
                                  n_jobs=-1):
        """
        寻找ExtraTreesRegressor构造器的最优参数

        上层UltronML中extra_tree_regressor_best函数，直接使用UltronML中的x，y数据调用

        :param x: 训练集x矩阵，numpy矩阵
        :param y: 训练集y序列，numpy序列
        :param param_grid: 最优字典关键字参数，
                     eg：param_grid = {'max_features': ['sqrt', 'log2', ],
                                      'n_estimators': np.arange(50, 200, 20)}
        :param assign: 是否保存实例化后最优参数的学习器对象，默认True
        :param n_jobs: 并行执行的进程任务数量，默认-1, 开启与cpu相同数量的进程数
        :return: 通过最优参数构造的ExtraTreeRegressor对象
        """
        return self._estimators_prarms_best(
            self.extra_tree_regressor,
            x,
            y,
            param_grid,
            assign,
            n_jobs,
            grid_callback=MLGrid.grid_search_init_max_depth)

    def extra_tree_classifier(self, assign=True, **kwargs):
        """
        有监督学习回归器，实例化ExtraTreesClassifier，默认使用：
            ExtraTreesClassifier(max_depth=2)

        通过**kwargs即关键字参数透传ExtraTreesClassifier，即:
            ExtraTreesClassifier(**kwargs)

        :param assign: 是否保存实例后的ExtraTreesClassifier对象，默认True，self.reg = reg
        :param kwargs: 有参数情况下初始化: ExtraTreesClassifier(**kwargs)
                       无参数情况下初始化: ExtraTreesClassifier(max_depth=2)

        :return: 实例化的ExtraTreesClassifier对象
        """
        if kwargs is not None and len(kwargs) > 0:
            classifier = ExtraTreesClassifier(**kwargs)
        else:
            classifier = ExtraTreesClassifier(max_depth=2)
        if assign:
            self._classifier = classifier
        return classifier

    def extra_tree_classifier_best(self,
                                   x,
                                   y,
                                   param_grid=None,
                                   assign=True,
                                   n_jobs=-1):
        """
        寻找ExtraTreesClassifier构造器的最优参数

        上层UltronML中decision_tree_regressor_best函数，直接使用UltronML中的x，y数据调用


        :param x: 训练集x矩阵，numpy矩阵
        :param y: 训练集y序列，numpy序列
        :param param_grid: 最优字典关键字参数，
                     eg：param_grid = {'max_features': ['sqrt', 'log2', ],
                                      'n_estimators': np.arange(50, 200, 20)}
        :param assign: 是否保存实例化后最优参数的学习器对象，默认True
        :param n_jobs: 并行执行的进程任务数量，默认-1, 开启与cpu相同数量的进程数
        :return: 通过最优参数构造的ExtraTreesClassifier对象
        """
        return self._estimators_prarms_best(
            self.extra_tree_classifier,
            x,
            y,
            param_grid,
            assign,
            n_jobs,
            grid_callback=MLGrid.grid_search_init_max_depth)

    def decision_tree_regressor(self, assign=True, **kwargs):
        """
        有监督学习回归器，实例化DecisionTreeRegressor，默认使用：
            DecisionTreeRegressor(max_depth=2, random_state=1)

        通过**kwargs即关键字参数透传DecisionTreeRegressor，即:
            DecisionTreeRegressor(**kwargs)

        :param assign: 是否保存实例后的DecisionTreeRegressor对象，默认True，self.reg = reg
        :param kwargs: 有参数情况下初始化: DecisionTreeRegressor(**kwargs)
                       无参数情况下初始化: DecisionTreeRegressor(max_depth=2, random_state=1)

        :return: 实例化的DecisionTreeRegressor对象
        """

        if kwargs is not None and len(kwargs) > 0:
            regressor = DecisionTreeRegressor(**kwargs)
        else:
            regressor = DecisionTreeRegressor(max_depth=2, random_state=1)
        if assign:
            self._regressor = regressor
        return regressor

    def decision_tree_regressor_best(self,
                                     x,
                                     y,
                                     param_grid=None,
                                     assign=True,
                                     n_jobs=-1):
        """
        寻找DecisionTreeRegressor构造器的最优参数

        上层UltronML中decision_tree_regressor_best函数，直接使用UltronML中的x，y数据调用

        :param x: 训练集x矩阵，numpy矩阵
        :param y: 训练集y序列，numpy序列
        :param param_grid: 最优字典关键字参数，
                     eg：param_grid = {'max_features': ['sqrt', 'log2', ],
                                      'n_estimators': np.arange(50, 200, 20)}
        :param assign: 是否保存实例化后最优参数的学习器对象，默认True
        :param n_jobs: 并行执行的进程任务数量，默认-1, 开启与cpu相同数量的进程数
        :return: 通过最优参数构造的DecisionTreeRegressor对象
        """
        return self._estimators_prarms_best(
            self.decision_tree_regressor,
            x,
            y,
            param_grid,
            assign,
            n_jobs,
            grid_callback=MLGrid.grid_search_init_max_depth)

    def decision_tree_classifier(self, assign=True, **kwargs):
        """
        有监督学习分类器，实例化DecisionTreeClassifier，默认使用：
            DecisionTreeClassifier(max_depth=2, random_state=1)

        通过**kwargs即关键字参数透传DecisionTreeClassifier，即:
            DecisionTreeClassifier(**kwargs)

        :param assign: 是否保存实例后的DecisionTreeClassifier对象，默认True，self.clf = clf
        :param kwargs: 有参数情况下初始化: DecisionTreeClassifier(**kwargs)
                       无参数情况下初始化: DecisionTreeClassifier(max_depth=2, random_state=1)

        :return: 实例化的DecisionTreeClassifier对象
        """

        if kwargs is not None and len(kwargs) > 0:
            classifier = DecisionTreeClassifier(**kwargs)
        else:
            classifier = DecisionTreeClassifier(max_depth=2, random_state=1)
        if assign:
            self._classifier = classifier
        return classifier

    def decision_tree_classifier_best(self,
                                      x,
                                      y,
                                      param_grid=None,
                                      assign=True,
                                      n_jobs=-1):
        """
        寻找DecisionTreeClassifier构造器的最优参数

        上层UltronML中decision_tree_classifier_best函数，直接使用UltronML中的x，y数据调用

        :param x: 训练集x矩阵，numpy矩阵
        :param y: 训练集y序列，numpy序列
        :param param_grid: 最优字典关键字参数，
                     eg：param_grid = {'max_features': ['sqrt', 'log2', ],
                                      'n_estimators': np.arange(50, 200, 20)}
        :param assign: 是否保存实例化后最优参数的学习器对象，默认True
        :param n_jobs: 并行执行的进程任务数量，默认-1, 开启与cpu相同数量的进程数
        :return: 通过最优参数构造的DecisionTreeClassifier对象
        """
        return self._estimators_prarms_best(
            self.decision_tree_classifier,
            x,
            y,
            param_grid,
            assign,
            n_jobs,
            grid_callback=MLGrid.grid_search_init_max_depth)

    def knn_classifier(self, assign=True, **kwargs):
        """
        有监督学习分类器，实例化KNeighborsClassifier，默认使用：
            KNeighborsClassifier(n_neighbors=1)

        通过**kwargs即关键字参数透传KNeighborsClassifier，即:
            KNeighborsClassifier(**kwargs)

        :param assign: 是否保存实例后的KNeighborsClassifier对象，默认True，self.clf = clf
        :param kwargs: 有参数情况下初始化: KNeighborsClassifier(**kwargs)
                       无参数情况下初始化: KNeighborsClassifier(n_neighbors=1)

        :return: 实例化的KNeighborsClassifier对象
        """

        if kwargs is not None and len(kwargs) > 0:
            classifier = KNeighborsClassifier(**kwargs)
        else:
            classifier = KNeighborsClassifier(n_neighbors=1)
        if assign:
            self._classifier = classifier
        return classifier

    def knn_classifier_best(self,
                            x,
                            y,
                            param_grid=None,
                            assign=True,
                            n_jobs=-1):
        """
        寻找KNeighborsClassifier构造器的最优参数

        上层UltronML中knn_classifier_best函数，直接使用UltronML中的x，y数据调用
        :param x: 训练集x矩阵，numpy矩阵
        :param y: 训练集y序列，numpy序列
        :param param_grid: 最优字典关键字参数，
                   eg：param_grid = {'algorithm': ['ball_tree', 'kd_tree', 'brute'],
                                    'n_neighbors': np.arange(1, 26, 1)}
        :param assign: 是否保存实例化后最优参数的学习器对象，默认True
        :param n_jobs: 并行执行的进程任务数量，默认-1, 开启与cpu相同数量的进程数
        :return: 通过最优参数构造的KNeighborsClassifier对象
        """
        return self._estimators_prarms_best(
            self.knn_classifier,
            x,
            y,
            param_grid,
            assign,
            n_jobs,
            grid_callback=MLGrid.grid_search_init_n_neighbors)

    def logistic_classifier(self, assign=True, **kwargs):
        """
        有监督学习分类器，实例化LogisticRegression，默认使用：
            LogisticRegression(C=1.0, penalty='l1', tol=1e-6)

        通过**kwargs即关键字参数透传LogisticRegression，即:
            LogisticRegression(**kwargs)

        :param assign: 是否保存实例后的LogisticRegression对象，默认True，self.clf = clf
        :param kwargs: 有参数情况下初始化: LogisticRegression(**kwargs)
                       无参数情况下初始化: LogisticRegression(C=1.0, penalty='l1', tol=1e-6)

        :return: 实例化的LogisticRegression对象
        """
        if kwargs is not None and len(kwargs) > 0:
            regression = LogisticRegression(**kwargs)
        else:
            regression = LogisticRegression(C=1.0, penalty='l1', tol=1e-6)
        if assign:
            self._regressor = regression
        return regression

    def polynomial_regression(self, assign=True, degree=2, **kwargs):
        """
        有监督学习回归器，使用：
            make_pipeline(PolynomialFeatures(degree), LinearRegression(**kwargs))

        :param assign: 是否保存实例后的LinearRegression对象，默认True，self.reg = reg
        :param degree: 多项式拟合参数，默认2
        :param kwargs: 由make_pipeline(PolynomialFeatures(degree), LinearRegression(**kwargs))
                       即关键字参数**kwargs全部传递给LinearRegression做为构造参数

        :return: 实例化的回归对象
        """
        regression = make_pipeline(PolynomialFeatures(degree),
                                   LinearRegression(**kwargs))
        if assign:
            self._regressor = regression
        return regression

    def onevsone_classifier(self, assign=False, **kwargs):
        """
        封装有监督学习分类器，使用OneVsOneClassifier进行多label的
        分类器二次封装，即：
             OneVsOneClassifier(self.clf, **kwargs)

        :param assign: 是否保存实例后的二次封装分类器对象，与其它构造器不同，
                       默认False，即默认不保存在类中替换原始分类器
        :param kwargs: 透传OneVsOneClassifier做为构造关键字参数
        :return: OneVsOneClassifier对象
        """
        onevsone = OneVsOneClassifier(self._classifier, **kwargs)
        if assign:
            self._classifier = onevsone
        return onevsone

    def onevsreset_classifier(self, assign=False, **kwargs):
        """
        封装有监督学习分类器，使用OneVsRestClassifier进行多label的
        分类器二次封装，即：
             OneVsRestClassifier(self.clf, **kwargs)

        :param assign: 是否保存实例后的二次封装分类器对象，与其它构造器不同，
                       默认False，即默认不保存在类中替换原始分类器
        :param kwargs: 透传OneVsRestClassifier做为构造关键字参数
        :return: OneVsRestClassifier对象
        """
        onevsreset = OneVsRestClassifier(self._classifier, **kwargs)
        if assign:
            self._classifier = onevsreset
        return onevsreset