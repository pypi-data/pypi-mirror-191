# -*- encoding:utf-8 -*-
"""
    技术线对象，对外执行，输出模块
"""
import math, itertools
import numpy as np
import pandas as pd
from collections import Iterable
from ultron.kdutils.lazy import LazyFunc
from ultron.ump.core.base import FreezeAttrMixin
from ultron.kdutils.decorator import arr_to_numpy
from ultron.kdutils import regression
from ultron.kdutils import stats as stats_util
from ultron.utilities.logger import kd_logger
from ultron.ump.technical.exectue import *

pd.options.display.precision = 4
# numpy精度浮点数显示4位，不使用科学计数法
np.set_printoptions(precision=4, suppress=True)
"""step_x_to_step函数中序列步长的常数单元值"""
g_step_unit = 10
"""预备颜色序列集，超出序列数量应使用itertools.cycle循环绘制"""
K_PLT_MAP_STYLE = ['r', 'g', 'c', 'k', 'm', 'r', 'y']


class Line(FreezeAttrMixin):
    """技术线封装执行对外操作的对象类"""

    def __init__(self, line, line_name, **kwargs):
        """
        :param line: 技术线可迭代序列，内部会通过arr_to_numpy统一转换numpy
        :param line_name: 技术线名称，str对象
        :param kwargs mean: 外部可选择通过kwargs设置mean，如不设置line.mean()
        :param kwargs std: 外部可选择通过kwargs设置std，如不设置line.std()
        :param kwargs high: 外部可选择通过kwargs设置high，如不设置self.mean + self.std
        :param kwargs low: 外部可选择通过kwargs设置low，如不设置self.mean - self.std
        :param kwargs close: 外部可选择通过kwargs设置close，如不设置line[-1]
        """
        # 把序列的nan进行填充，实际上应该是外面根据数据逻辑把nan进行填充好了再传递进来，这里只能都使用bfill填了
        line = pd.Series(line).fillna(method='bfill')
        self.tl = arr_to_numpy(line)
        self.mean = kwargs.pop('mean', self.tl.mean())
        self.std = kwargs.pop('std', self.tl.std())
        self.high = kwargs.pop('high', self.mean + self.std)
        self.low = kwargs.pop('low', self.mean - self.std)
        self.close = kwargs.pop('close', self.tl[-1])

        self.x = np.arange(0, self.tl.shape[0])
        self.line_name = line_name

        for k, v in kwargs:
            # 需要设置什么都通过kwargs设置进来，不然_freeze后无法设置
            setattr(self, k, v)
        # 需要进行定稿，初始化好就不能动
        self._freeze()

    @LazyFunc
    def score(self):
        """
        被LazyFunc装饰：
        score代表当前技术线值在当前的位置， (self.close - self.low) / (self.high - self.low)
        eg：
            self.high ＝ 100， self.low＝0，self.close＝80
            －> (self.close - self.low) / (self.high - self.low) = 0.8
            即代表当前位置在整体的0.8位置上

        :return: 技术线当前score, 返回值在0-1之间
        """
        if self.high == self.low:
            score = 0.8 if self.close > self.low else 0.2
        else:
            score = (self.close - self.low) / (self.high - self.low)
        return score

    @LazyFunc
    def y_zoom(self):
        """
        被LazyFunc装饰：
        获取对象技术线tl被self.x缩放后的序列y_zoom
        :return: 放后的序列y_zoom
        """
        zoom_factor = self.x.max() / self.tl.max()
        y_zoom = zoom_factor * self.tl
        return y_zoom

    def step_x_to_step(self, step_x):
        """
        针对技术线的时间范围步长选择函数，在create_shift_distance，create_regress_trend_channel，
        show_skeleton_channel等涉及时间步长的函数中用来控制步长范围
        :param step_x: 时间步长控制参数，float
        :return: 最终输出被控制在2-len(self.tl), int
        """
        if step_x <= 0:
            # 不正常step_x规范到正常范围中
            #log_func(
            #    'input step_x={} is error, change to step_x=1'.format(step_x))
            step_x = 1
        # 如果需要调整更细的粒度，调整g_step_unit的值
        step = int(math.floor(len(self.tl) / g_step_unit / step_x))
        # 输出被控制在2-len(self.tl)
        step = len(self.tl) if step > len(self.tl) else step
        step = 2 if step < 2 else step
        return step

    def is_up_trend(self, up_deg_threshold=5):
        """
        判断走势是否符合上升走势：
        1. 判断走势是否可以使用一次拟合进行描述
        2. 如果可以使用1次拟合进行描述，计算一次拟合趋势角度
        3. 如果1次拟合趋势角度 >= up_deg_threshold判定上升
        :param up_deg_threshold: 判定一次拟合趋势角度为上升趋势的阀值角度，默认5
        :return: 是否上升趋势
        """
        valid = regression.valid_poly(self.tl, poly=1)
        if valid:
            deg = regression.calc_regress_deg(self.tl)
            if deg >= up_deg_threshold:
                return True
        return False

    def is_down_trend(self, down_deg_threshold=-5):
        """
        判断走势是否符合下降走势：
        1. 判断走势是否可以使用一次拟合进行描述
        2. 如果可以使用1次拟合进行描述，计算一次拟合趋势角度
        3. 如果1次拟合趋势角度 <= down_deg_threshold判定下降
        :param down_deg_threshold: 判定一次拟合趋势角度为下降趋势的阀值角度，默认－5
        :return: 是否下降趋势
        """
        valid = regression.valid_poly(self.tl, poly=1)
        if valid:
            deg = regression.calc_regress_deg(self.tl)
            if deg <= down_deg_threshold:
                return True
        return False

    def create_support_resistance_pos(self, best_poly=0):
        """
        可视化分析技术线阻力位和支撑位，通过sco.fmin_bfgs寻找阻力位支撑位，阻力位点也是通过sco.fmin_bfgs寻找，
        但是要求传递进来的序列已经是标准化后取反的序列
        eg：
            demean_y = ABuStatsUtil.demean(self.tl)： 首先通过demean将序列去均值
            resistance_y = demean_y * -1 ：阻力位序列要取反
            support_y = demean_y ：支持位序列不需要取反
        :param best_poly: 函数使用者可设置best_poly, 设置后就不使用ABuRegUtil.search_best_poly寻找了,
                          详细阅ABuTLExecute.support_resistance_pos
        :return: (技术线支撑位: support_pos, 技术线阻力位: resistance_pos)
        """
        # 首先通过demean将序列去均值
        demean_y = stats_util.demean(self.tl)
        # 阻力位序列要取反
        resistance_y = demean_y * -1
        # 支持位序列不需要取反
        support_y = demean_y

        # 分析技术线支撑位
        support_pos = support_resistance_pos(self.x,
                                             support_y,
                                             best_poly=best_poly,
                                             label='support pos')
        # 分析技术线阻力位
        resistance_pos = support_resistance_pos(self.x,
                                                resistance_y,
                                                best_poly=best_poly,
                                                label='resistance pos')
        return support_pos, resistance_pos

    def create_support_resistance_select_k(self, best_poly=0):
        """
        可视化分析技术线阻力位和支撑位序列从1-序列个数开始聚类，多个聚类器的方差值进行比较，
        通过方差阀值等方法找到最佳聚类个数，最终得到kmean最佳分类器对象
        :param best_poly: 传递show_support_resistance_pos，
                          函数使用者可设置best_poly, 设置后就不使用ABuRegUtil.search_best_poly寻找了
        :return: upport_est, resistance_est, support_pos, resistance_pos
        """
        # 可视化分析技术线阻力位或者支撑位
        support_pos, resistance_pos = self.create_support_resistance_pos(
            best_poly)

        support_pos = np.array(
            [support_pos, [self.tl[support] for support in support_pos]]).T

        resistance_pos = np.array([
            resistance_pos,
            [self.tl[resistance] for resistance in resistance_pos]
        ]).T

        support_est = None
        if len(support_pos) > 1:
            # 多个聚类器的方差值进行比较，通过方差阀值等方法找到最佳聚类个数，最终得到kmean最佳分类器对象
            # 注意这里的show直接False了
            support_est = select_k_support_resistance(support_pos)

        resistance_est = None
        if len(resistance_pos) > 1:
            # 注意这里的show直接False了
            resistance_est = select_k_support_resistance(resistance_pos)

        return support_est, resistance_est, support_pos, resistance_pos

    def create_support_trend(self, best_poly=0, only_last=False):
        """
        最终对技术线只对阻力位进行绘制

        套接：show_support_resistance_select_k－>support_resistance_predict
             ->ABuTLExecute.plot_support_resistance_trend
        :param best_poly: 传递show_support_resistance_pos，
                          函数使用者可设置best_poly, 设置后就不使用ABuRegUtil.search_best_poly寻找了
        :param only_last: 透传ABuTLExecute.plot_support_resistance_trend，控制只绘制时间序列中最后一个发现的阻力或支撑
        """
        support_est, _, support_pos, _ = self.create_support_resistance_select_k(
            best_poly)
        y_trend_dict = {}
        if support_est is not None:
            support_trend = support_resistance_predict(self.x,
                                                       self.tl,
                                                       support_est,
                                                       support_pos,
                                                       is_support=True)
            y_support_trend = create_support_resistance_trend(
                self.x,
                self.tl,
                support_trend,
                'support trend line',
                only_last=only_last)

            if y_support_trend is not None:
                y_trend_dict['support'] = y_support_trend
        return y_trend_dict

    def create_resistance_trend(self, best_poly=0, only_last=False):
        """
        最终对技术线只对支撑位进行绘制

        套接：show_support_resistance_select_k－>support_resistance_predict
             ->ABuTLExecute.plot_support_resistance_trend
        :param best_poly: 传递show_support_resistance_pos，
                          函数使用者可设置best_poly, 设置后就不使用ABuRegUtil.search_best_poly寻找了
        :param only_last: 透传ABuTLExecute.plot_support_resistance_trend，控制只绘制时间序列中最后一个发现的阻力或支撑
        :param plot_org: 透传ABuTLExecute.plot_support_resistance_trend，控制是否绘制线段还是直线，控制是否绘制线段还是直线，
                         plot_org＝True时绘制线段，否则通过LinearRegression进行
        """
        _, resistance_est, _, resistance_pos = self.create_support_resistance_select_k(
            best_poly)

        y_trend_dict = {}

        if resistance_est is not None:
            resistance_trend = support_resistance_predict(self.x,
                                                          self.tl,
                                                          resistance_est,
                                                          resistance_pos,
                                                          is_support=False)
            y_resistance_trend = create_support_resistance_trend(
                self.x,
                self.tl,
                resistance_trend,
                'resistance trend line',
                only_last=only_last)

            if y_resistance_trend is not None:
                y_trend_dict['resistance'] = y_resistance_trend
        return y_trend_dict

    def create_support_resistance_trend(self, best_poly=0, only_last=False):
        """
        套接：show_support_resistance_select_k－>support_resistance_predict
             ->ABuTLExecute.plot_support_resistance_trend
        最终对技术线阻力位和支撑位进行绘制，注意show参数控制的是中间流程中的可视化，不包括
        最终阻力位和支撑的可视化
        :param best_poly: 传递show_support_resistance_pos，
                          函数使用者可设置best_poly, 设置后就不使用ABuRegUtil.search_best_poly寻找了
        :param only_last: 透传ABuTLExecute.plot_support_resistance_trend，控制只绘制时间序列中最后一个发现的阻力或支撑
        """
        support_est, resistance_est, support_pos, resistance_pos = self.create_support_resistance_select_k(
            best_poly)

        y_trend_dict = {}
        if support_est is not None:
            # FIXME 针对极端没有找到足够绘制支撑阻力位的情况做处理
            support_trend = support_resistance_predict(self.x,
                                                       self.tl,
                                                       support_est,
                                                       support_pos,
                                                       is_support=True)

            y_support_trend = create_support_resistance_trend(
                self.x,
                self.tl,
                support_trend,
                'support trend line',
                only_last=only_last)
            if y_support_trend is not None:
                y_trend_dict['support'] = y_support_trend
        else:
            kd_logger.info('can\'t plot support !')

        if resistance_est is not None:
            resistance_trend = support_resistance_predict(self.x,
                                                          self.tl,
                                                          resistance_est,
                                                          resistance_pos,
                                                          is_support=False)
            y_resistance_trend = create_support_resistance_trend(
                self.x,
                self.tl,
                resistance_trend,
                'resistance trend line',
                only_last=only_last)
            if y_resistance_trend is not None:
                y_trend_dict['resistance'] = y_resistance_trend
        else:
            kd_logger.info('can\'t plot resistance !')
        return y_trend_dict

    def create_shift_distance(self,
                              how=EShiftDistanceHow.shift_distance_close,
                              step_x=1.0):
        """
        可视化技术线'路程位移比'，注意默认使用shift_distance_close对应标准路程点位值定义方法，其它方法对应的
        路程终点点位值使用的计算方法并非得到最准确的'路程位移比'，实现详ABuTLExecute.shift_distance
        :param how: EShiftDistanceHow对象或者callable即外部可自行设置方法，即计算算路程终点点位值使用的计算方法可自定义
        :param step_x: 时间步长控制参数，默认1.0，float
        :return 对每一个金融序列切片进行shift_distance的返回结果序列，即每一个序列中的元素为：
                    h_distance(三角底边距离), v_distance(三角垂直距离),
                    distance(斜边，路程), shift(位移), sd（位移路程比：shift / distance）
                所组成的tuple对象
        """
        # 这里使用了缩放后的y，因为确保路程位移比具有更好的适应性
        y = self.y_zoom
        step = self.step_x_to_step(step_x)

        shift_distance_list = []
        for slice_end, _ in zip(np.arange(step, len(y), step),
                                itertools.cycle(K_PLT_MAP_STYLE)):
            slice_start = slice_end - step
            shift_distance_list.append(
                shift_distance(y,
                               how,
                               slice_start=slice_start,
                               slice_end=slice_end))
        return shift_distance_list

    def create_least_valid_poly(self, zoom=False):
        """
        可视化技术线，检测至少poly次拟合曲线可以代表原始曲线y的走势，
        具体详情ABuRegUtil.least_valid_poly
        :param zoom: 透传least_valid_poly是否缩放x,y
        """
        least, rolling_window, y_fit, y_roll_mean, distance_fit, distance_mean = regression.least_valid_poly(
            self.tl, zoom=zoom)
        return least, rolling_window, y_fit, y_roll_mean, distance_fit, distance_mean

    def create_best_poly(self, zoom=False):
        """
        可视化技术线最优拟合次数，寻找poly（1－100）次多项式拟合回归的趋势曲线可以比较完美的代表原始曲线y的走势，
        具体详情ABuRegUtil.search_best_poly
        :param zoom: 透传search_best_poly是否缩放x,y
        """
        best, rolling_window, y_fit, y_roll_mean, distance_fit, distance_mean = regression.search_best_poly(
            self.tl, zoom=zoom, only_poly=False)
        return best, rolling_window, y_fit, y_roll_mean, distance_fit, distance_mean

    def create_regress_trend_channel(self, step_x=1.0):
        """
        可视化技术线拟合曲线及上下拟合通道曲线，返回三条拟合曲线，组成拟合通道
        :param step_x: 时间步长控制参数，默认1.0，float
        """
        channel_list = []
        y = self.tl
        step = self.step_x_to_step(step_x)
        for slice_end, _ in zip(np.arange(step, len(y), step),
                                itertools.cycle(K_PLT_MAP_STYLE)):
            slice_start = slice_end - step
            slice_arr = y[slice_start:slice_end]
            # 通过regress_trend_channel获取切片段的上中下三段拟合曲线值
            y_below, y_fit, y_above = regress_trend_channel(slice_arr)
            x = self.x[slice_start:slice_end]
            channel_list.append({
                'x': x,
                'y_below': y_below,
                'y_fit': y_fit,
                'y_above': y_above
            })
        return channel_list

    def golden_percents(self, percents=(0.1, 0.9)):
        """
        可视化技术线比例分割的区域
        :param percents: float值或者可迭代序列，默认使用(0.1, 0.9)
        :return:
        """
        if not isinstance(percents, Iterable):
            # 如果不是可迭代序列，添加到list中，便于统一处理
            percents = [percents]
        pts_dict = find_percent_point(percents, self.tl)
        return pts_dict

    def create_golden(self, both_golden=True):
        """
        技术线黄金分割
        :param both_golden: 代表同时可视化两种分割线的计算在一个画布上
        :return:
        """
        if both_golden:
            return self.golden_percents(percents=(0.382, 0.618))
        else:
            return {
                'ex': find_golden_point_ex(self.x, self.tl),
                'basic': find_golden_point(self.x, self.tl)
            }

    def create_skeleton(self, how=ESkeletonHow.skeleton_min, step_x=1.0):
        """
        可视化技术线骨架结构
        :param how: 计算数据序列骨架点位的方法，ESkeletonHow对象或者callable即外部可自行设置方法，
                    即计算数据序列骨架点位的方法可自定义
        :param step_x: 时间步长控制参数，默认1.0，float
        """
        step = self.step_x_to_step(step_x)
        # 每个单位都先画一个点，由两个点连成一条直线形成股价骨架图
        last_pos = None
        # 根据how映射计算数据序列骨架点位的方法
        how_func = skeleton_how(how)

        skeleton_res = []
        for slice_end, color in zip(np.arange(step, len(self.tl), step),
                                    itertools.cycle(K_PLT_MAP_STYLE)):
            slice_start = slice_end - step
            slice_arr = self.tl[slice_start:slice_end]
            if how == ESkeletonHow.skeleton_triangle:
                """
                    三角模式骨架点位：确定取最大值，最小值，第三个点位how_func提供
                    如果np.argmax(arr) > np.argmin(arr)即最大值位置在最小值前面，第三点取序列起点，否则取序列终点
                """
                max_pos = (np.argmax(slice_arr) + slice_start,
                           np.max(slice_arr))
                min_pos = (np.argmin(slice_arr) + slice_start,
                           np.min(slice_arr))
                draw_pos = how_func(slice_arr, slice_start)
                res = {
                    'slice_end': slice_end,
                    'max_pos': max_pos,
                    'min_pos': min_pos,
                    'draw_pos': draw_pos
                }

            else:
                # 其它骨架数据计算方法
                draw_pos = (slice_start, how_func(slice_arr))
                temp_pos = last_pos
                # 将这个步长单位内的最小值点赋予last_pos
                last_pos = draw_pos
                res = {
                    'slice_end': slice_end,
                    'last_pos': temp_pos,
                    'draw_pos': draw_pos
                }

            skeleton_res.append(res)
        return skeleton_res

    def create_skeleton_channel(self, step_x=1.0):
        """
        套接show_skeleton，可视化可视化技术线骨架通道，通道由：
        ESkeletonHow.skeleton_min：下通道，
        ESkeletonHow.skeleton_max：上通道，
        ESkeletonHow.skeleton_mean 中轨通道，组成

        :param with_mean: 是否绘制ESkeletonHow.skeleton_mean 中轨通道，默认True
        :param step_x: 时间步长控制参数，默认1.0，float
        """
        min_res = self.create_skeleton(how=ESkeletonHow.skeleton_min,
                                       step_x=step_x)
        max_res = self.create_skeleton(how=ESkeletonHow.skeleton_max,
                                       step_x=step_x)

        mean_res = self.create_skeleton(how=ESkeletonHow.skeleton_mean,
                                        step_x=step_x)

        return min_res, max_res, mean_res
