# encoding: utf-8
"""
获取因子时间序列
"""
from Utils import WindHelper


def get_ip_ts(begin_date, end_date):
    """
    获取IP的月度同比数据
    注意：1月，2月数据用累计同步，3月到12月数据用当月同比
    :return: 
    """
    codeList = ["M0000545", "M0000011"]  # 当月同比， 累计同比
    df = WindHelper.getEDBTimeSeriesDataFrame(codeList=codeList,
                                              beginDate=begin_date,
                                              endDate=end_date)
    df.loc[:, "ip"] = df.iloc[:, 0]
    for i in range(len(df) - 1):
        if df.index[i].month == 1:
            df.ix[i, "ip"] = df.iloc[i+1, 1]
        elif df.index[i].month == 2:
            df.ix[i, "ip"] = df.iloc[i, 1]
        else:
            continue
    return df[["ip"]]


def test():
    from datetime import *
    begin_date = datetime(2007, 1, 1)
    end_date = datetime(2017, 8, 7)
    df = get_ip_ts(begin_date=begin_date, end_date=end_date)
    print(df)


if __name__ == "__main__":
    test()
