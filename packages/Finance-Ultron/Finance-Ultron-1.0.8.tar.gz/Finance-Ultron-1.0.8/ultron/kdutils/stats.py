# -*- encoding:utf-8 -*-
"""
    统计相关工具模块
"""
import numpy as np
import pandas as pd
import functools, six
import scipy.stats as scs
from collections import namedtuple, Iterable
from sklearn.metrics.pairwise import euclidean_distances, manhattan_distances, cosine_distances
from ultron.kdutils.scaler import scaler_mm
from ultron.ump.core.helper import pd_rolling_mean


# noinspection PyClassHasNoInit
class MomentsTuple(
        namedtuple(
            'MomentsTuple',
            ('count', 'max', 'min', 'mean', 'std', 'skewness', 'kurtosis'))):
    __slots__ = ()

    def __repr__(self):
        return "count:{}\nmax:{}\nmin:{}\nmean:{}\nstd:{}\nskewness:{}\nkurtosis:{}".format(
            self.count, self.max, self.min, self.mean, self.std, self.skewness,
            self.kurtosis)


# noinspection PyUnresolvedReferences
def _distance_matrix(distance_func, df, scale_end=True, to_similar=False):
    """
    非两两distance计算，限制只有一个矩阵的输入，且输入必须为pd.DataFrame or np.array or 多层迭代序列[[],[]]
    :param distance_func: 计算距离的方法
    :param df: pd.DataFrame or np.array or 多层迭代序列[[],[]], 之所以叫df，是因为在内部会统一转换为pd.DataFrame
    :param scale_end: 对结果矩阵进行标准化处理
    :param to_similar: 是否进行后置输出转换similar值
    :return: distance_matrix，pd.DataFrame对象
    """

    if not callable(distance_func):
        raise TypeError('distance_func must callable!!!')

    if isinstance(df, np.ndarray):
        # 把np.ndarray转DataFrame，便统一处理
        df = pd.DataFrame(df)

    if not isinstance(df, pd.DataFrame):
        if all(isinstance(arr_item, Iterable) for arr_item in df):
            # 如果子序列的元素也都是可以迭代的，那么先转np.array，然后再DataFrame
            df = pd.DataFrame(np.array(df))
        else:
            raise TypeError('df must pd.DataFrame object!!!')
    # 做列的distance所以df.T
    distance = distance_func(df.T)

    if scale_end:
        # TODO 这里需要可以设置标准化使用的方法，暂时都使用scaler_mm
        distance = scaler_mm(distance)
        if to_similar:
            # 只有scale_end的情况下to_similar才会生效，否则没有意义
            distance = 1 - distance

    # 将计算结果的distance转换为pd.DataFrame对象，行和列索引都使用df.columns
    distance_df = pd.DataFrame(distance, index=df.columns, columns=df.columns)
    return distance_df


def arr_to_pandas(func):
    """
        函数装饰器：定参数装饰器，非通用，通用转换使用ABuDTUtil中的装饰器
        将被装饰函数中的arr序列转换为pd.DataFrame或者pd.Series
    """

    @functools.wraps(func)
    def wrapper(arr, *arg, **kwargs):

        # TODO Iterable和six.string_types的判断抽出来放在一个模块，做为Iterable的判断来使用
        if not isinstance(arr, Iterable) or isinstance(arr, six.string_types):
            # arr必须是可以迭代的对象
            raise TypeError('arr not isinstance of Iterable')

        if not isinstance(arr, pd.DataFrame) or isinstance(arr, pd.Series):
            if isinstance(
                    arr,
                    np.ndarray) and len(arr.shape) > 1 and arr.shape[1] > 1:
                # np.ndarray > 1列的转换为pd.DataFrame
                arr = pd.DataFrame(arr)
            elif isinstance(arr, dict):
                # 针对dict转换pd.DataFrame
                arr = pd.DataFrame(arr)
            elif all(isinstance(arr_item, Iterable) for arr_item in arr):
                # 如果子序列的元素也都是可以迭代的，那么先转np.array，然后再DataFrame
                arr = pd.DataFrame(np.array(arr))
            else:
                # 否则序列对象转换为pd.Series
                arr = pd.Series(arr)
        return func(arr, *arg, **kwargs)

    return wrapper


def arr_to_numpy(func):
    """
        函数装饰器：定参数装饰器，非通用，通用转换使用UltronDTUtil中的装饰器
        将被装饰函数中的arr序列转换为np.array
    """

    @functools.wraps(func)
    def wrapper(arr, *arg, **kwargs):
        # TODO Iterable和six.string_types的判断抽出来放在一个模块，做为Iterable的判断来使用
        if not isinstance(arr, Iterable) or isinstance(arr, six.string_types):
            # arr必须是可以迭代的对象
            raise TypeError('arr not isinstance of Iterable')

        if not isinstance(arr, np.ndarray):
            if isinstance(arr, pd.DataFrame) or isinstance(arr, pd.Series):
                # 如果是pandas直接拿values
                arr = arr.values
            elif isinstance(arr, dict):
                # 针对dict转换np.array
                arr = np.array(list(arr.values())).T
            else:
                arr = np.array(arr)
        return func(arr, *arg, **kwargs)

    return wrapper


@arr_to_numpy
def stats_namedtuple(arr):
    """
    通过序列构造arr的基础统计信息dict, 被arr_to_numpy装饰，统一输出，且这样使用arr.max(), arr.min()等不需要axis参数区别
    与stats_dict的区别只是返回namedtuple对象
    :param arr: pd.DataFrame or pd.Series or Iterable
    :return: MomentsTuple
                eg:
                    count:504
                    max:286.04
                    min:143.67
                    mean:228.48845238095237
                    std:25.538448192811927
                    skewness:-0.282635248604699
                    kurtosis:0.009313464006726946

    """
    count = arr.shape[0]
    if len(arr.shape) > 1 and arr.shape[1] > 1:
        count = arr.shape[0] * arr.shape[1]

    return MomentsTuple(count, arr.max(), arr.min(), arr.mean(), arr.std(),
                        scs.skew(arr), scs.kurtosis(arr))


@arr_to_pandas
def demean(arr, rolling_window=0):
    """
        去均值化后处理demean, 如果输入的是np.array进行转换为pd.DataFrame处理，
        被arr_to_pandas装饰，统一输出，且这样使用arr.mean()不需要axis参数区别np.array轴向
        eg:
            cc.head()
                        tsla	bidu	noah	sfun	goog	vips	aapl
            2014-07-25	223.57	226.50	15.32	12.11	589.02	21.349	97.67
            2014-07-28	224.82	225.80	16.13	12.45	590.60	21.548	99.02
            2014-07-29	225.01	220.00	16.75	12.22	585.61	21.190	98.38
            2014-07-30	228.92	219.13	16.83	11.78	587.42	21.185	98.15
            2014-07-31	223.30	216.05	16.06	11.47	571.60	20.550	95.60

            ABuStatsUtil.demean(cc.head())

                        tsla	bidu	noah	sfun	goog	vips	aapl
            2014-07-25	-1.554	5.004	-0.898	0.104	4.17	0.1846	-0.094
            2014-07-28	-0.304	4.304	-0.088	0.444	5.75	0.3836	1.256
            2014-07-29	-0.114	-1.496	0.532	0.214	0.76	0.0256	0.616
            2014-07-30	3.796	-2.366	0.612	-0.226	2.57	0.0206	0.386
            2014-07-31	-1.824	-5.446	-0.158	-0.536	-13.25	-0.6144	-2.164

            ABuStatsUtil.demean(cc.head().values)

                0	1	2	3	4	5	6
            0	-1.554	5.004	-0.898	0.104	4.17	0.1846	-0.094
            1	-0.304	4.304	-0.088	0.444	5.75	0.3836	1.256
            2	-0.114	-1.496	0.532	0.214	0.76	0.0256	0.616
            3	3.796	-2.366	0.612	-0.226	2.57	0.0206	0.386
            4	-1.824	-5.446	-0.158	-0.536	-13.25	-0.6144	-2.164

            tsla.head()

            2014-07-25    223.57
            2014-07-28    224.82
            2014-07-29    225.01
            2014-07-30    228.92
            2014-07-31    223.30

            ABuStatsUtil.demean(tsla.head())

            2014-07-25   -1.554
            2014-07-28   -0.304
            2014-07-29   -0.114
            2014-07-30    3.796
            2014-07-31   -1.824

            ABuStatsUtil.demean(tsla.head().values)

                0
            0	-1.554
            1	-0.304
            2	-0.114
            3	3.796
            4	-1.824

    :param arr: pd.DataFrame or pd.Series or Iterable
    :param rolling_window: 默认＝0，即不使用移动平均做去均值，rolling_window > 0 生效，
                           注意如果rolling_window值过小将导致去均值后不连续，比如5日，10日的
                           结果只能类似close pct_change的结果，如果需求要钝化，最好是两个月以上
                           的交易日数量，user要根据需求，选择使用的参数，
    :param show: 是否可视化去均值后的结果，默认False
    :return:
    """

    if rolling_window > 0:
        # arr_to_pandas装饰器保证了进来的类型不是pd.DataFrame就是pd.Series
        arr_mean = pd_rolling_mean(arr, window=rolling_window, min_periods=1)
        # arr_mean.fillna(method='bfill', inplace=True)
    else:
        arr_mean = arr.mean()

    demean_v = arr - arr_mean
    return demean_v


def euclidean_distance_matrix(df, scale_end=True, to_similar=False):
    """
    欧式距离(L2范数): 与euclidean_distance_xy的区别主要是，非两两distance计算，只有一个矩阵的输入，
    且输入必须为pd.DataFrame or np.array or 多层迭代序列[[],[]], 注意需要理解数据的测距目的来分析
    是否需要进行scale_start，进行和不进行scale_start的结果将完全不一样，在功能需求及数据理解的情况下
    选择是否进行scale_start

            input:

                        tsla	bidu	noah	sfun	goog	vips	aapl
            2014-07-25	223.57	226.50	15.32	12.110	589.02	21.349	97.67
            2014-07-28	224.82	225.80	16.13	12.450	590.60	21.548	99.02
            2014-07-29	225.01	220.00	16.75	12.220	585.61	21.190	98.38
            ...	...	...	...	...	...	...	...
            2016-07-22	222.27	160.88	25.50	4.850	742.74	13.510	98.66
            2016-07-25	230.01	160.25	25.57	4.790	739.77	13.390	97.34
            2016-07-26	225.93	163.09	24.75	4.945	740.92	13.655	97.76

            ABuStatsUtil.euclidean_distance_matrix(cc, scale_start=True)

            output:

                    tsla	bidu	noah	sfun	goog	vips	aapl
            tsla	0.0000	0.4086	0.7539	0.7942	0.4810	0.7638	0.3713
            bidu	0.4086	0.0000	0.7732	0.7047	0.6185	0.6161	0.4184
            noah	0.7539	0.7732	0.0000	0.7790	0.7174	0.6957	0.7425
            sfun	0.7942	0.7047	0.7790	0.0000	0.9950	0.5422	0.9558
            goog	0.4810	0.6185	0.7174	0.9950	0.0000	1.0000	0.5379
            vips	0.7638	0.6161	0.6957	0.5422	1.0000	0.0000	0.7348
            aapl	0.3713	0.4184	0.7425	0.9558	0.5379	0.7348	0.0000


            ABuStatsUtil.euclidean_distance_matrix(cc, scale_start=False)

                    tsla	bidu	noah	sfun	goog	vips	aapl
            tsla	0.0000	0.0781	0.3314	0.3573	0.6527	0.3386	0.1933
            bidu	0.0781	0.0000	0.2764	0.3018	0.7112	0.2827	0.1392
            noah	0.3314	0.2764	0.0000	0.0284	0.9732	0.0140	0.1408
            sfun	0.3573	0.3018	0.0284	0.0000	1.0000	0.0203	0.1674
            goog	0.6527	0.7112	0.9732	1.0000	0.0000	0.9820	0.8369
            vips	0.3386	0.2827	0.0140	0.0203	0.9820	0.0000	0.1481
            aapl	0.1933	0.1392	0.1408	0.1674	0.8369	0.1481	0.0000

    :param df: pd.DataFrame or np.array or 多层迭代序列[[],[]], 之所以叫df，是因为在内部会统一转换为pd.DataFrame
    :param scale_end: 对结果矩阵进行标准化处理
    :param to_similar: 是否进行后置输出转换similar值
    :return: distance_df，pd.DataFrame对象
    """
    return _distance_matrix(euclidean_distances, df, scale_end, to_similar)


def manhattan_distance_matrix(df, scale_end=True, to_similar=False):
    """
    曼哈顿距离(L1范数): 与manhattan_distances_xy的区别主要是，非两两distance计算，只有一个矩阵的输入，
    且输入必须为pd.DataFrame or np.array or 多层迭代序列[[],[]]，注意需要理解数据的测距目的来分析
    是否需要进行scale_start，进行和不进行scale_start的结果将完全不一样，在功能需求及数据理解的情况下
    选择是否进行scale_start

        eg:
            input:

                        tsla	bidu	noah	sfun	goog	vips	aapl
            2014-07-25	223.57	226.50	15.32	12.110	589.02	21.349	97.67
            2014-07-28	224.82	225.80	16.13	12.450	590.60	21.548	99.02
            2014-07-29	225.01	220.00	16.75	12.220	585.61	21.190	98.38
            ...	...	...	...	...	...	...	...
            2016-07-22	222.27	160.88	25.50	4.850	742.74	13.510	98.66
            2016-07-25	230.01	160.25	25.57	4.790	739.77	13.390	97.34
            2016-07-26	225.93	163.09	24.75	4.945	740.92	13.655	97.76

            ABuStatsUtil.manhattan_distance_matrix(cc, scale_start=True)

            output:

                    tsla	bidu	noah	sfun	goog	vips	aapl
            tsla	0.0000	0.3698	0.6452	0.7917	0.4670	0.7426	0.3198
            bidu	0.3698	0.0000	0.5969	0.7056	0.6495	0.5822	0.4000
            noah	0.6452	0.5969	0.0000	0.7422	0.7441	0.6913	0.6896
            sfun	0.7917	0.7056	0.7422	0.0000	0.9236	0.4489	1.0000
            goog	0.4670	0.6495	0.7441	0.9236	0.0000	0.8925	0.5134
            vips	0.7426	0.5822	0.6913	0.4489	0.8925	0.0000	0.7038
            aapl	0.3198	0.4000	0.6896	1.0000	0.5134	0.7038	0.0000


            ABuStatsUtil.manhattan_distance_matrix(cc, scale_start=False)

            output:

                    tsla	bidu	noah	sfun	goog	vips	aapl
            tsla	0.0000	0.0640	0.3318	0.3585	0.6415	0.3395	0.1906
            bidu	0.0640	0.0000	0.2750	0.3018	0.6982	0.2827	0.1338
            noah	0.3318	0.2750	0.0000	0.0267	0.9733	0.0124	0.1412
            sfun	0.3585	0.3018	0.0267	0.0000	1.0000	0.0191	0.1680
            goog	0.6415	0.6982	0.9733	1.0000	0.0000	0.9809	0.8320
            vips	0.3395	0.2827	0.0124	0.0191	0.9809	0.0000	0.1489
            aapl	0.1906	0.1338	0.1412	0.1680	0.8320	0.1489	0.000

    :param df: pd.DataFrame or np.array or 多层迭代序列[[],[]], 之所以叫df，是因为在内部会统一转换为pd.DataFrame
    :param scale_end: 对结果矩阵进行标准化处理
    :param to_similar: 是否进行后置输出转换similar值
    :return: distance_df，pd.DataFrame对象
    """
    return _distance_matrix(manhattan_distances, df, scale_end, to_similar)


def cosine_distance_matrix(df, scale_end=True, to_similar=False):
    """
    余弦距离: 与cosine_distances_xy的区别主要是，非两两distance计算，只有一个矩阵的输入，
    且输入必须为pd.DataFrame or np.array or 多层迭代序列[[],[]]，注意需要理解数据的测距目的来分析
    是否需要进行scale_start，进行和不进行scale_start的结果将完全不一样，在功能需求及数据理解的情况下
    选择是否进行scale_start

        eg:
            input:

                        tsla	bidu	noah	sfun	goog	vips	aapl
            2014-07-25	223.57	226.50	15.32	12.110	589.02	21.349	97.67
            2014-07-28	224.82	225.80	16.13	12.450	590.60	21.548	99.02
            2014-07-29	225.01	220.00	16.75	12.220	585.61	21.190	98.38
            ...	...	...	...	...	...	...	...
            2016-07-22	222.27	160.88	25.50	4.850	742.74	13.510	98.66
            2016-07-25	230.01	160.25	25.57	4.790	739.77	13.390	97.34
            2016-07-26	225.93	163.09	24.75	4.945	740.92	13.655	97.76


            ABuStatsUtil.cosine_distance_matrix(cc, scale_start=True)

            output:

                    tsla	bidu	noah	sfun	goog	vips	aapl
            tsla	0.0000	0.1743	0.4434	0.2945	0.2394	0.4763	0.1266
            bidu	0.1743	0.0000	0.5808	0.2385	0.3986	0.3034	0.1470
            noah	0.4434	0.5808	0.0000	1.0000	0.3411	0.7626	0.2632
            sfun	0.2945	0.2385	1.0000	0.0000	0.7494	0.4448	0.4590
            goog	0.2394	0.3986	0.3411	0.7494	0.0000	0.9717	0.2806
            vips	0.4763	0.3034	0.7626	0.4448	0.9717	0.0000	0.2669
            aapl	0.1266	0.1470	0.2632	0.4590	0.2806	0.2669	0.0000


            ABuStatsUtil.cosine_distance_matrix(cc, scale_start=False)

            output:

                    tsla	bidu	noah	sfun	goog	vips	aapl
            tsla	0.0000	0.1743	0.4434	0.2945	0.2394	0.4763	0.1266
            bidu	0.1743	0.0000	0.5808	0.2385	0.3986	0.3034	0.1470
            noah	0.4434	0.5808	0.0000	1.0000	0.3411	0.7626	0.2632
            sfun	0.2945	0.2385	1.0000	0.0000	0.7494	0.4448	0.4590
            goog	0.2394	0.3986	0.3411	0.7494	0.0000	0.9717	0.2806
            vips	0.4763	0.3034	0.7626	0.4448	0.9717	0.0000	0.2669
            aapl	0.1266	0.1470	0.2632	0.4590	0.2806	0.2669	0.0000

    :param df: pd.DataFrame or np.array or 多层迭代序列[[],[]], 之所以叫df，是因为在内部会统一转换为pd.DataFrame
    :param scale_end: 对结果矩阵进行标准化处理
    :param to_similar: 是否进行后置输出转换similar值
    :return: distance_df，pd.DataFrame对象
    """
    return _distance_matrix(cosine_distances, df, scale_end, to_similar)