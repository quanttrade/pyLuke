# encoding: utf-8
# 编写因子事件
import pandas as pd


def e000(factor_series, cur_date, config):
    """
    因子过去N个周期的总涨幅
    :param factor_series: 
    :param cur_date: 
    :param config: 
    :return: 
    """
    period = config["period"]
    type = config["type"]
    his_count = config["his_count"]
    threshold = config["threshold"]
    his_end_num = len(factor_series[factor_series.index <= cur_date]) - 1
    his_start_num = his_end_num - his_count + 1
    ret = factor_series.iloc[his_end_num] / factor_series.iloc[his_start_num] - 1
    event_value = ret - threshold
    return event_value


def e001(adjust_factor_series, cur_date, config):
    """
    均值缺口事件函数，只是提供事件函数，不判断方向，不判断未来函数，保持最小功能
    :param adjust_factor_series: series 因子的时间序列
    :param cur_date: (datetime,timestamp or string),cur_date不是买入日期，而是承受波动日期
    :param his_count: int 历史时间窗口大小
    :return: float 返回因子事件值,返回值应该标准化，正值表示应该做多，负值表示应该做空
    """
    # 拆解config字典
    his_count = config["his_count"]
    std_count = config["std_count"]
    # 找到当前日期或者与当前日期最相近的前一个日期
    his_end_num = len(adjust_factor_series[adjust_factor_series.index <= cur_date]) - 1
    # 开始计算信号值的大小
    his_start_num = his_end_num - his_count + 1
    if his_start_num < 0:
        return None
    avg = adjust_factor_series.iloc[his_start_num:his_end_num + 1].mean()
    std = adjust_factor_series.iloc[his_start_num:his_end_num + 1].std()
    # 返回信号值
    event_value = adjust_factor_series.iloc[his_end_num] - avg - std_count * std
    return event_value


def e002x1(factor_series, cur_date, config):
    """
    连续N个周期上涨
    :return: 
    """

    pass


def e003():
    """
    连续N个周期下跌
    :return: 
    """
    pass


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


def test():
    pass


if __name__ == "__main__":
    test()
