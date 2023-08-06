import sys, os
from IPython.display import clear_output
from IPython.display import display
from ipywidgets import FloatProgress, Text, Box
from ultron.ump.core import env
from ultron.kdutils.decorator import warnings_filter, catch_error
"""多进程下进度条通信socket文件最终名字，这里子进程可以获取g_socket_fn是通过ABuEnvProcess拷贝了主进程全局信息"""
g_socket_fn = None
"""多进程下进度是否显示ui进度，只针对进程间通信类型的进度，有些太频繁的进度显示可以选择关闭"""
g_show_ui_progress = True
"""主进程下用来存贮子进程传递子进程pid为key，进度条对象UIProgress为value"""


def do_clear_output(wait=False):
    """
    模块方法，clear所有的输出，内部针对notebook和命令行输出做区分
    :param wait: 是否同步执行clear操作，透传给IPython.display.clear_output
    """
    if env.g_is_ipython:
        # notebook clear
        clear_output(wait=wait)
    else:
        # cmd clear
        #cmd = 'clear' if env.g_is_mac_os else 'cls'
        cmd = "clear" if True else "cls"
        os.system(cmd)
        # pass


class MulPidProgress(object):
    """多进程进度显示控制类"""

    def __init__(self, total, label, show_progress=True):
        """
        外部使用eg：
        with AbuMulPidProgress(len(self.choice_symbols), 'pick stocks complete') as progress:
            for epoch, target_symbol in enumerate(self.choice_symbols):
                progress.show(epoch + 1)

        :param total: 总任务数量
        :param label: 进度显示label
        """
        self._total = total
        self._label = label
        self.epoch = 0
        self.display_step = 1
        self.progress_widget = None
        self.text_widget = None
        self.progress_box = None
        self.show_progress = show_progress

    # 不管ui进度条有什么问题，也不能影响任务工作的进度执行，反正有文字进度会始终显示
    @catch_error(log=False)
    def init_ui_progress(self):
        """初始化ui进度条"""
        if not self.show_progress:
            return

        if not env.g_is_ipython or self._total < 2:
            return

        if env.g_main_pid == os.getpid():
            # 如果是在主进程下显示那就直接来
            self.progress_widget = FloatProgress(value=0, min=0, max=100)
            self.text_widget = Text('pid={} begin work'.format(os.getpid()))
            self.progress_box = Box([self.text_widget, self.progress_widget])
            display(self.progress_box)
        else:
            if g_show_ui_progress and g_socket_fn is not None:
                # 子进程下通过socket通信将pid给到主进程，主进程创建ui进度条
                ABuOsUtil.socket_send_msg(g_socket_fn,
                                          '{}|init'.format(os.getpid()))

    # 不管ui进度条有什么问题，也不能影响任务工作的进度执行，反正有文字进度会始终显示
    @catch_error(log=False)
    def update_ui_progress(self, ps, ps_text):
        """更新文字进度条"""
        if not self.show_progress:
            return

        if not env.g_is_ipython or self._total < 2:
            return

        if env.g_main_pid == os.getpid():
            # 如果是在主进程下显示那就直接来
            if self.progress_widget is not None:
                self.progress_widget.value = ps
            if self.text_widget is not None:
                self.text_widget.value = ps_text
        else:
            if g_show_ui_progress and g_socket_fn is not None:
                # 子进程下通过socket通信将pid给到主进程，主进程通过pid查找对应的进度条对象后更新进度
                ABuOsUtil.socket_send_msg(
                    g_socket_fn, '{}|{}|{}'.format(os.getpid(), ps, ps_text))

    # 不管ui进度条有什么问题，也不能影响任务工作的进度执行，反正有文字进度会始终显示
    @catch_error(log=False)
    def close_ui_progress(self):
        """关闭ui进度条显示"""
        if not self.show_progress:
            return

        if not env.g_is_ipython or self._total < 2:
            return

        if env.g_main_pid == os.getpid():
            # 如果是在主进程下显示那就直接来
            if self.progress_box is not None:
                self.progress_box.close()
        else:
            if g_show_ui_progress and g_socket_fn is not None:
                # 子进程下通过socket通信将pid给到主进程，主进程通过pid查找对应的进度条对象后关闭对象，且弹出
                ABuOsUtil.socket_send_msg(g_socket_fn,
                                          '{}|close'.format(os.getpid()))

    def __enter__(self):
        """
        以上下文管理器类方式实现__enter__，针对self._total分配self.display_step
        """
        if self.show_progress:
            self.display_step = 1
            if self._total >= 5000:
                self.display_step = 50
            elif self._total >= 3000:
                self.display_step = 30
            elif self._total >= 2000:
                self.display_step = 20
            elif self._total > 1000:
                self.display_step = 10
            elif self._total >= 600:
                self.display_step = 6
            elif self._total >= 300:
                self.display_step = 3
            elif self._total >= 100:
                self.display_step = 2
            elif self._total >= 20:
                self.display_step = 2
            self.epoch = 0
            self.init_ui_progress()
        return self

    def show(self, epoch=None, clear=True):
        """
        进行进度控制显示主方法
        :param epoch: 默认None, 即使用类内部计算的迭代次数进行进度显示
        :param clear: 默认True, 子进程显示新的进度前，先do_clear_output所有输出
        :return:
        """
        if not self.show_progress:
            return

        self.epoch = epoch if epoch is not None else self.epoch + 1
        if self.epoch % self.display_step == 0:
            ps = round(self.epoch / self._total * 100, 2)
            ps = 100 if ps > 100 else ps
            ps_text = "pid:{} {}:{}%".format(os.getpid(), self._label, ps)
            if not env.g_is_ipython or self._total < 2:
                if clear:
                    do_clear_output()
                    # clear_std_output()
                print(ps_text)

            self.update_ui_progress(ps, ps_text)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        以上下文管理器类方式实现__exit__，针对在子进城中的输出显示进度进行do_clear_output扫尾工作
        """
        if not self.show_progress:
            return

        clear = False
        if clear:
            # clear在mac上应该打开, 由于windows某些版本浏览器wait=True会有阻塞情况，如果wait＝False, 有clear之后的风险，
            do_clear_output(wait=True)  # wait 需要同步否则会延迟clear
        else:
            # print("pid:{} done!".format(os.getpid()))
            pass

        self.close_ui_progress()


class Progress(object):
    """单进程（主进程）进度显示控制类"""

    @warnings_filter
    def __init__(self, total, a_progress, label=None):
        """
        外部使用eg：
            progess = Progress(stock_df.shape[0], 0, 'merging {}'.format(m))
            for i, symbol in enumerate(stock_df['symbol']):
                progess.show(i + 1)
        :param total: 总任务数量
        :param a_progress: 初始进度
        :param label: 进度显示label
        """
        self._total = total
        self._progress = a_progress
        self._label = label
        self.f = sys.stdout
        self.progress_widget = None

    def __enter__(self):
        """创建子进程做进度显示"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.f.write('\r')
        if self.progress_widget is not None:
            self.progress_widget.close()

    @property
    def progress(self):
        """property获取self._progress"""
        return self._progress

    @progress.setter
    def progress(self, a_progress):
        """progress.setter设置progress"""
        if a_progress > self._total:
            self._progress = self._total
        elif a_progress < 0:
            self._progress = 0
        else:
            self._progress = a_progress

    def show(self, a_progress=None, ext='', p_format="{}:{}:{}%"):
        """
        进行进度控制显示主方法
        :param ext: 可以添加额外的显示文字，str，默认空字符串
        :param a_progress: 默认None, 即使用类内部计算的迭代次数进行进度显示
        :param p_format: 进度显示格式，默认{}: {}%，即'self._label:round(self._progress / self._total * 100, 2))%'
        """
        self.progress = a_progress if a_progress is not None else self.progress + 1
        ps = round(self._progress / self._total * 100, 2)

        if self._label is not None:
            # 如果初始化label没有就只显示ui进度
            self.f.write('\r')
            self.f.write(p_format.format(self._label, ext, ps))

        if 'IS_IPYTHON' in os.environ and os.environ['IS_IPYTHON']:
            if self.progress_widget is None:
                self.progress_widget = FloatProgress(value=0, min=0, max=100)
                display(self.progress_widget)
            self.progress_widget.value = ps

        # 这样会出现余数结束的情况，还是尽量使用上下文管理器控制结束
        if self._progress == self._total:
            self.f.write('\r')
            if self.progress_widget is not None:
                self.progress_widget.close()
