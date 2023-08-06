# -*- encoding:utf-8 -*-
"""
    黄金分割及比例分割示例模块
"""
from collections import namedtuple
import matplotlib.pyplot as plt
from ultron.ump.technical import exectue as tl_exectue


def create_golden(kl_pd):
    """
    只针对金融时间序列的收盘价格close序列，进行黄金分割及比例分割
    数值结果分析以及可视化
    :param kl_pd: 金融时间序列，pd.DataFrame对象
    :param show: 是否可视化黄金分割及比例分割结果
    :return: 黄金分割及比例分割结果组成的namedtuple数值对象
    """
    kl_close = kl_pd.close
    if not hasattr(kl_pd, 'name'):
        # 金融时间序列中如果有异常的没有name信息的补上一个unknown
        kl_pd.name = 'unknown'
    # 计算视觉黄金分割
    gd_382, gd_500, gd_618 = tl_exectue.find_golden_point(
        kl_pd.index, kl_close)
    # 计算统计黄金分割
    gex_382, gex_500, gex_618 = tl_exectue.find_golden_point_ex(
        kl_pd.index, kl_close)

    # below above 382, 618确定，即382，618上下底
    below618, above618 = tl_exectue.below_above_gen(gd_618, gex_618)
    below382, above382 = tl_exectue.below_above_gen(gd_382, gex_382)

    # 再次通过比例序列percents和find_percent_point寻找对应比例的位置字典pts_dict
    percents = [0.20, 0.25, 0.30, 0.70, 0.80, 0.90, 0.95]
    pts_dict = tl_exectue.find_percent_point(percents, kl_close)

    # 0.20, 0.25, 0.30只找最低的，即底部只要最低的
    below200, _ = tl_exectue.below_above_gen(*pts_dict[0.20])
    below250, _ = tl_exectue.below_above_gen(*pts_dict[0.25])
    below300, _ = tl_exectue.below_above_gen(*pts_dict[0.30])

    # 0.70, 0.80, 0.90, 0.95只找最高的，即顶部只要最高的
    _, above700 = tl_exectue.below_above_gen(*pts_dict[0.70])
    _, above800 = tl_exectue.below_above_gen(*pts_dict[0.80])
    _, above900 = tl_exectue.below_above_gen(*pts_dict[0.90])
    _, above950 = tl_exectue.below_above_gen(*pts_dict[0.95])

    return namedtuple('golden', [
        'g382', 'gex382', 'g500', 'gex500', 'g618', 'gex618', 'above618',
        'below618', 'above382', 'below382', 'above950', 'above900', 'above800',
        'above700', 'below300', 'below250', 'below200'
    ])(gd_382, gex_382, gd_500, gex_500, gd_618, gex_618, above618, below618,
       above382, below382, above950, above900, above800, above700, below300,
       below250, below200)
