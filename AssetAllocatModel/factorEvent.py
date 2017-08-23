# encoding: utf-8
# 编写因子事件
import pandas as pd


class FactorEventCollect(object):
    def __init__(self, factor_dict, factor_config):
        """
        factor_dict用于存储因子的时间序列，之所以用字典形式，是为了在多因子回测中可以存储所有的因子序列。
        :param factor_dict:因子时间序列字典{"factor_name":dataframe} 
        :param factor_config: 因子关于各个因子事件的配置信息
        """
        self.factor_dict = factor_dict
        self.factor_event_dict = {"move_avg_break_through": self.move_avg_break_through}

    def move_avg_break_through(self, cur_date, mv_count, forward_window=1, period=1, lag=1):
        """因子突破均值事件
        设置mv_count值作为均值计算用的时间窗口。
        forward_count设置未来k个周期的整体涨跌，默认1个周期
        lag表示滞后次数，默认是1个周期，具体而言当天收盘得到信号，明天才能买入，后天才能看到涨跌，CPI之类的可能两个周期。
        period为调整周期，即没多少时间调整一次。
        """
        event_value = 0
        return event_value
