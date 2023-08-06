# -*- encoding:utf-8 -*-
"""
    字符工具模块
"""


def digit_str(item):
    """
        从第一个字符开始删除，直到所有字符都是数字为止，或者item长度 < 2
        eg:
            input:  ABuStrUtil.digit_str('sh000001')
            output: 000001

            input:  ABuStrUtil.digit_str('shszsh000001')
            output: 000001
    :param item: 字符串对象
    :return: 过滤head字母的字符串对象
    """
    while True:
        if item.isdigit():
            break
        if len(item) < 2:
            break
        item = item[1:]
    return item