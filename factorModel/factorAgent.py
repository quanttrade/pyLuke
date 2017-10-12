# encoding: utf-8
from common import *


class DigitFactorAgent(object):
    """
    有一个人告诉FacotorAgent，你好，请告诉这个因子在A事件cur_date时间上产生的结果，
    FactorAgent说，好的，我会返回你一个因子在这个事件上的结果
    数字事件和模拟事件需要分开来研究，不要杂糅一团，但是两者最后又公共抽象部分。
    因子的叠加只适用于布尔事件值
    所有事件都是反映因子强弱一种方式
    A + B = C: A强B强，则C强
    A - B = C: A强B强，则C强
    C + D = E：C强D强，则E强
    A|B = C: B强后A强则C强
    A|(-B) = C: B弱后A强则C强
    (A+C)|(-B) = D: B弱后A和C都强则D强
    """

    def __init__(self, event_name, factor_series, factor_config):
        """
        :param event_name: (str) 因子名称
        :param factor_series:（series）因子时间序列 
        :param factor_config: (dict)因子关于各个因子事件的配置信息
        """
        self.config = factor_config
        self.factor_series = factor_series
        # 因子有效event合集
        self.event = event_dict[event_name]

    def get_event_value(self, cur_date):
        if cur_date in self.factor_series.index:
            return self.event(self.factor_series, cur_date, self.config)
        else:
            raise Exception(u"""The series in the factor agent 
            does not contain cur_date""")
