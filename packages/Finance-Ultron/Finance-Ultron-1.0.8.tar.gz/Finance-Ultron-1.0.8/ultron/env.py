# -*- encoding:utf-8 -*-
"""
    全局环境配置模块
"""
import os
from os import path
from enum import Enum
from urllib.request import urlretrieve
from ultron.utilities.logger import kd_logger
"""是否开启 example 环境，默认关闭False"""
_g_enable_example_env = False
"""当前用户路径"""
root_drive = path.expanduser('~')

g_project_root = path.join(root_drive, 'ultron')

g_base_path = os.path.join(g_project_root, 'base')

g_project_data = os.path.join(g_project_root, 'rom/sandbox')

default_sandbox_url = 'https://ultronsandbox.oss-cn-hangzhou.aliyuncs.com/sandbox.zip'
default_base_url = 'https://ultronsandbox.oss-cn-hangzhou.aliyuncs.com/base.zip'

g_sandbox_url = default_sandbox_url if 'ULTRON_DATA_URL' not in os.environ else os.environ[
    'ULTRON_DATA_URL']

g_base_url = default_base_url if 'ULTRON_BASE_URL' not in os.environ else os.environ[
    'ULTRON_BASE_URL']

if 'ULTRON_DATA' in os.environ:
    g_project_data = os.path.join(g_project_data, os.environ['ULTRON_DATA'])

g_plt_figsize = (14, 7)


# TODO 缩短 E_DATA_FETCH_NORMAL－>NORMAL
class EMarketDataFetchMode(Enum):
    """
        金融时间数据获取模式
    """
    """普通模式，尽量从本地获取数据，本地数据不满足的情况下进行网络请求"""
    E_DATA_FETCH_NORMAL = 0
    """强制从本地获取数据，本地数据不满足的情况下，返回None"""
    E_DATA_FETCH_FORCE_LOCAL = 1
    """强制从网络获取数据，不管本地数据是否满足"""
    E_DATA_FETCH_FORCE_NET = 2


def init_plot_set():
    """全局plot设置"""
    import seaborn as sns
    sns.set_context('notebook', rc={'figure.figsize': g_plt_figsize})
    sns.set_style("darkgrid")

    import matplotlib
    # conda 5.0后需要添加单独matplotlib的figure设置否则pandas的plot size不生效
    matplotlib.rcParams['figure.figsize'] = g_plt_figsize


def init_data():
    if not os.path.exists(g_base_path):
        data_base_zip = os.path.join(g_project_root, "base.zip")
        if not os.path.exists(g_project_root):
            os.mkdir(g_project_root)
        kd_logger.info("download base data")
        urlretrieve(g_base_url, data_base_zip)
        try:
            from zipfile import ZipFile
            zip_csv = ZipFile(data_base_zip, "r")
            unzip_dir = os.path.join(g_project_root, "./")
            for csv in zip_csv.namelist():
                zip_csv.extract(csv, unzip_dir)
            zip_csv.close()
        except Exception as e:
            # 解压测试数据zip失败，就不开启测试数据模式了
            kd_logger.error('data env failed! e={}'.format(e))
            return


def enable_example_env(show_log=True):
    if not os.path.exists(g_project_data):
        data_example_zip = os.path.join(g_project_root, "sandbox.zip")
        if not os.path.exists(g_project_root):
            os.mkdir(g_project_root)
        kd_logger.info("download sandbox data")
        urlretrieve(g_sandbox_url, data_example_zip)
        try:
            from zipfile import ZipFile
            zip_csv = ZipFile(data_example_zip, "r")
            unzip_dir = os.path.join(g_project_root, "rom/")
            for csv in zip_csv.namelist():
                zip_csv.extract(csv, unzip_dir)
            zip_csv.close()
        except Exception as e:
            # 解压测试数据zip失败，就不开启测试数据模式了
            kd_logger.error('example env failed! e={}'.format(e))
            return

    global _g_enable_example_env, g_data_fetch_mode
    _g_enable_example_env = True

    g_data_fetch_mode = EMarketDataFetchMode.E_DATA_FETCH_FORCE_LOCAL

    init_plot_set()
    if show_log:
        kd_logger.info(
            'enable example env will only read {0}'.format(g_project_data))
