# encoding: utf-8
# 编写因子事件
import pandas as pd


def avg_break(factor_series, cur_date, config):
    """
    均值缺口事件
    :param factor_series: series 因子的时间序列
    :param cur_date: (datetime,timestamp or string),cur_date不是买入日期，而是承受波动日期
    :param his_count: int 历史时间窗口大小
    :return: float 返回因子事件值,返回值应该标准化，正值表示应该做多，负值表示应该做空
    """
    # 拆解config字典
    his_count = config["his_count"]
    std_count = config["std_count"]
    postive = config["postive"]
    # 找到当前日期或者与当前日期最相近的前一个日期
    his_end_num = len(factor_series[factor_series.index < cur_date]) - 1
    # 开始计算信号值的大小
    his_start_num = his_end_num - his_count + 1
    if his_start_num < 0:
        return None, None
    avg = factor_series.iloc[his_start_num:his_end_num + 1].mean()
    std = factor_series.iloc[his_start_num:his_end_num + 1].std()
    # 返回信号值
    gap = factor_series.iloc[his_end_num] - avg - std_count * std
    if postive:
        pos = 1 if gap > 0 else 0  # 做多信号或者无信号
    else:
        pos = -1 if gap > 0 else 0  # 做空信号或者无信号
    return gap, pos


def rank_limit(factor_series, cur_date, up_rank, period=1):
    """
    排名阈值事件
    :param factor_series: 
    :param cur_date: 
    :param up_rank: 
    :return: 
    """
    # 找到当前日期
    # 找到当前日期或者与当前日期最相近的前一个日期
    his_end_num = len(factor_series[factor_series.index < cur_date]) - 1
    # 开始计算信号的大小
    gap = up_rank - factor_series.iloc[his_end_num]
    return gap


class FactorAgent(object):
    """
    有一个人告诉FacotorAgent，你好，请告诉这个因子在A事件上有效性，
    FactorAgent说，好的，我会返回你一个因子在这个事件上的结果
    """

    def __init__(self, name, factor_df, factor_config):
        """
        :param name: (str) 因子名称
        :param factor_df:（dataFrame）因子时间序列 
        :param factor_config: (dict)因子关于各个因子事件的配置信息
        """
        self.name = name
        self.config = factor_config
        self.factor_df = factor_df
        # 因子有效event合集
        self.factor_event_dict = {"move_avg_break_through": self.move_avg_break_through}

    def move_avg_break_through(self, cur_date, hist_count, forward_count=1):
        """
        因子突破均值事件
        :param cur_date: 
        :param hist_count: (int)值作为均值计算用的时间窗口。
        :param forward_count: (int)设置未来k个周期的整体涨跌，默认1个周期
        :return: 
        """
        event_value = 0
        self.factor_df[cur_date]
        return event_value


def test():
    pass


if __name__ == "__main__":
    test()
