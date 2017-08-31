# encoding: utf-8
import pandas as pd
from factorEvent import *
import math
import numpy as np



def calculate_info_ratio(asset_series, factor_series, event_name, config, beginDate=None, endDate=None, period=1):
    """计算信息比率"""
    # 计算所以调仓时点
    adjust_time_spots = []
    for i in range(len(factor_series.index)-1):
        time_spot = asset_series.index[len(asset_series[asset_series.index <= factor_series.index[i + 1]])]
        adjust_time_spots.append(time_spot)
    return adjust_time_spots


def check_factor(asset_series, factor_series, event_name, config, beginDate=None, endDate=None, period=1):
    """
    因子校验器
    :param beginDate: 
    :param endDate: 
    :param period: 
    :param asset_series: 
    :param factor_series: 
    :param event_name: 
    :param config: 
    :return: 
    """
    # 先确定要调用的事件
    if event_name == "avg_break":
        event = avg_break
    else:
        print(u"该因子事件还没有收录到因子事件库中，请更新你的因子事件库再重新运行！")
        return None
    # 开始回溯
    pos_list = []  # 每个周期都产生的持仓信号，当period为1时，和period_pos_list是一样的
    event_value_list = []
    period_pos_list = []  # 每period个周期，产生一个持仓信号，期间都沿用上一个持仓信号
    ret_after_signal = []  # 记录信号发出后资产在period内的涨幅
    times = []
    asset_ret_series = asset_series.to_frame().pct_change()  # 转换成涨跌幅
    # 对回测时间进行筛选
    if beginDate is not None:
        asset_ret_series = asset_ret_series[(asset_ret_series.index >= beginDate)]
    elif endDate is not None:
        asset_ret_series = asset_ret_series[(asset_ret_series.index <= endDate)]
    asset_ret_series = asset_ret_series[1:]  # 去除首行NA
    signal_start_index = -1
    for i in range(len(asset_ret_series)):
        # 检查因子事件是否返回结果
        event_result, pos = event(factor_series, asset_series.index[i], config)
        if event_result is not None:  # 如果定义的起始时间并没有信号，那么起始时间自动延后
            times.append(asset_ret_series.index[i])
            # 记录事件值
            event_value_list.append(event_result)
            # 记录信号值,将正向事件和负向事件区别对待
            pos_list.append(0 if (config["postive"] ^ (pos == 0)) else 1)
            if signal_start_index == -1:
                # 记录产生信号的第一天的行数
                signal_start_index = i
            if (i - signal_start_index) % period == 0:  # 没多少个周期调整一次
                if event_result > 0:
                    ret_after_signal.append((asset_ret_series.iloc[i:period + i] + 1).cumprod().values[0] - 1)
                period_pos_list.append(0 if (config["postive"] ^ (pos == 0)) else 1)
            else:  # 如果没到更新点，则沿用上个周期的持仓
                period_pos_list.append(period_pos_list[-1])
        else:
            continue
    res = asset_ret_series.ix[signal_start_index:, [asset_series.name]]
    res.loc[:, "pos"] = pd.Series(period_pos_list, index=res.index)
    res.loc[:, "value"] = (res.loc[:, asset_series.name] * res.loc[:, "pos"] + 1).cumprod()
    res.loc[:, "base"] = (res.loc[:, asset_series.name] + 1).cumprod()
    report = dict()
    report["sp"] = sharpe_ratio(res["value"])
    report["excess_sp"] = - sharpe_ratio(res["base"]) + report["sp"]
    # 计算IR信息比率
    report["ir"] = np.average(ret_after_signal) / np.std(ret_after_signal)
    report["precious"] = np.sum(np.array(ret_after_signal) > 0) * 1.0 / len(ret_after_signal)
    report["ts"] = res.loc[:, ["value", "base", "pos"]]
    return report


def calculate_excess_sharp_ratio(asset_series, factor_series, event_name, config, beginDate=None, endDate=None, period=1):
    """
    对因子-因子事件进行回测，针对因子信号计算器夏普比率，主要评价因子信号的对称性特征。
    如果超额夏普比率大，说明因子-因子事件，无论是触发还是没被触发都可以作为一种做多或者做空的信号
    :param beginDate: 
    :param endDate: 
    :param period: 
    :param asset_series: 
    :param factor_series: 
    :param event_name: 
    :param config: 
    :return: 
    """
    # 先确定要调用的事件
    if event_name == "avg_break":
        event = avg_break
    else:
        print(u"该因子事件还没有收录到因子事件库中，请更新你的因子事件库再重新运行！")
        return None
    # 开始回溯
    pos_list = []  # 每个周期都产生的持仓信号，当period为1时，和period_pos_list是一样的
    event_value_list = []
    period_pos_list = []  # 每period个周期，产生一个持仓信号，期间都沿用上一个持仓信号
    ret_after_signal = []  # 记录信号发出后资产在period内的涨幅
    times = []
    asset_ret_series = asset_series.to_frame().pct_change()  # 转换成涨跌幅
    # 对回测时间进行筛选
    if beginDate is not None:
        asset_ret_series = asset_ret_series[(asset_ret_series.index >= beginDate)]
    elif endDate is not None:
        asset_ret_series = asset_ret_series[(asset_ret_series.index <= endDate)]
    asset_ret_series = asset_ret_series[1:]  # 去除首行NA
    signal_start_index = -1
    for i in range(len(asset_ret_series)):
        # 检查因子事件是否返回结果
        event_result, pos = event(factor_series, asset_series.index[i], config)
        if event_result is not None:  # 如果定义的起始时间并没有信号，那么起始时间自动延后
            times.append(asset_ret_series.index[i])
            # 记录事件值
            event_value_list.append(event_result)
            # 记录信号值,将正向事件和负向事件区别对待
            pos_list.append(0 if (config["postive"] ^ (pos == 0)) else 1)
            if signal_start_index == -1:
                # 记录产生信号的第一天的行数
                signal_start_index = i
            if (i - signal_start_index) % period == 0:  # 没多少个周期调整一次
                if event_result > 0:
                    ret_after_signal.append((asset_ret_series.iloc[i:period + i] + 1).cumprod().values[0] - 1)
                period_pos_list.append(0 if (config["postive"] ^ (pos == 0)) else 1)
            else:  # 如果没到更新点，则沿用上个周期的持仓
                period_pos_list.append(period_pos_list[-1])
        else:
            continue
    res = asset_ret_series.ix[signal_start_index:, [asset_series.name]]
    res.loc[:, "pos"] = pd.Series(period_pos_list, index=res.index)
    res.loc[:, "value"] = (res.loc[:, asset_series.name] * res.loc[:, "pos"] + 1).cumprod()
    res.loc[:, "base"] = (res.loc[:, asset_series.name] + 1).cumprod()
    report = dict()
    report["sp"] = sharpe_ratio(res["value"])
    report["excess_sp"] = - sharpe_ratio(res["base"]) + report["sp"]
    # 计算IR信息比率
    report["ir"] = np.average(ret_after_signal) / np.std(ret_after_signal)
    report["precious"] = np.sum(np.array(ret_after_signal) > 0) * 1.0 / len(ret_after_signal)
    report["ts"] = res.loc[:, ["value", "base", "pos"]]
    return report


def test():
    from windHelper import WindHelper
    from datetime import datetime
    beginDate = datetime(2012, 12, 1)
    endDate = datetime(2017, 8, 22)
    para = "close"
    df = WindHelper.getMultiTimeSeriesDataFrame(["060E.CS", "885009.WI"], beginDate=beginDate, endDate=endDate,
                                                para=para)
    df = df.dropna()
    df.loc[:, "cm"] = df.loc[:, "060e.cs_close"] / df.loc[:, "885009.wi_close"]
    result = check_factor(df["060e.cs_close"], df["cm"], "avg_break", {"his_count": 60}, period=5)
    print result


if __name__ == "__main__":
    test()
