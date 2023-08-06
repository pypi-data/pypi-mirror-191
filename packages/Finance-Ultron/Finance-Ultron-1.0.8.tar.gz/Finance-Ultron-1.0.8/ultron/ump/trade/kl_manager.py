# -*- encoding:utf-8 -*-
"""
    金融时间序列管理模块
"""
import pandas as pd


class KLManager(object):
    """金融时间序列管理类"""

    def __init__(self, benchmark, capital):
        """
        :param benchmark: 交易基准对象，AbuBenchmark实例对象
        :param capital: 资金类AbuCapital实例化对象
        """
        self.benchmark = benchmark
        self.capital = capital
        # 选股时间交易序列字典
        pick_stock_kl_pd_dict = dict()
        # 择时时间交易序列字典
        pick_time_kl_pd_dict = dict()
        # 类字典pick_kl_pd_dict将选股和择时字典包起来
        self.pick_kl_pd_dict = {
            'pick_stock': pick_stock_kl_pd_dict,
            'pick_time': pick_time_kl_pd_dict
        }

    def __str__(self):
        """打印对象显示：pick_stock + pick_time keys, 即所有symbol信息"""
        keys = set(self.pick_kl_pd_dict['pick_stock'].keys()) | set(
            self.pick_kl_pd_dict['pick_time'].keys())
        return 'pick_stock + pick_time keys :{}'.format(keys)

    __repr__ = __str__

    def __len__(self):
        """对象长度：选股字典长度 + 择时字典长度"""
        return len(self.pick_kl_pd_dict['pick_stock']) + len(
            self.pick_kl_pd_dict['pick_time'])

    def __contains__(self, item):
        """成员测试：在择时字典中或者在选股字典中"""
        return item in self.pick_kl_pd_dict[
            'pick_stock'] or item in self.pick_kl_pd_dict['pick_time']

    def __missing__(self, key):
        """对象缺失：需要根据key使用code_to_symbol进行fetch数据，暂未实现"""
        # TODO 需要根据key使用code_to_symbol进行fetch数据
        raise NotImplementedError('TODO AbuKLManager __missing__')

    def __getitem__(self, key):
        """索引获取：尝试分别从选股字典，择时字典中查询，返回两个字典的查询结果"""
        pick_stock_item = None
        if key in self.pick_kl_pd_dict['pick_stock']:
            pick_stock_item = self.pick_kl_pd_dict['pick_stock'][key]
        pick_time_item = None
        if key in self.pick_kl_pd_dict['pick_time']:
            pick_time_item = self.pick_kl_pd_dict['pick_time'][key]
        return pick_stock_item, pick_time_item

    def __setitem__(self, key, value):
        """索引设置：抛错误，即不准许外部设置"""
        raise AttributeError("AbuKLManager set value!!!")

    def set_pick_time(self, values):
        self.pick_kl_pd_dict['pick_time'] = values

    def set_pick_stock(self, values):
        self.pick_kl_pd_dict['pick_stock'] = values

    def get_pick_time_kl_pd(self, target_symbol):
        """对外获取择时时段金融时间序列，首先在内部择时字典中寻找，没找到使用_fetch_pick_time_kl_pd获取，且保存择时字典"""
        if target_symbol in self.pick_kl_pd_dict['pick_time']:
            kl_pd = self.pick_kl_pd_dict['pick_time'][target_symbol]
            if kl_pd is not None:
                # 因为在多进程的时候拷贝会丢失name信息
                kl_pd.name = target_symbol
            return kl_pd
        kl_pd = pd.DataFrame()
        kl_pd.name = target_symbol
        return kl_pd