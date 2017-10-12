# encoding: utf-8
from WindPy import w
import pandas as pd
from Utils import WindHelper


def getAllContracts(contractType, beginDate, endDate):
    """从wind获取所有的国债期货合约的信息"""
    w.start()
    nearCode = "TF00.CFE"
    farCode = "TF01.CFE"
    farfarCode = "TF02.CFE"
    if contractType == "TF" or contractType == "tf":
        nearCode = "TF00.CFE"
        farCode = "TF01.CFE"
        farfarCode = "TF02.CFE"
    elif contractType == "T" or contractType == "t":
        nearCode = "T00.CFE"
        farCode = "T01.CFE"
        farfarCode = "T02.CFE"
    # 国债期货当季列表
    # lastrade_date 最后交易日
    # trade_hiscode 月份合约
    # oi 持仓量
    # volume 成交量
    # settle 结算价
    para = ["trade_hiscode"]
    nearDF = WindHelper.getTimeSeriesDataFrame(nearCode, beginDate, endDate, para)
    # 国债期货下季列表
    farDF = WindHelper.getTimeSeriesDataFrame(farCode, beginDate, endDate, para)
    # 国债期货隔季合约
    farfarDF = WindHelper.getTimeSeriesDataFrame(farfarCode, beginDate, endDate, para)
    # 获取国债期货时间序列基础表：
    # 日期，当季合约，当季结算价，持仓量，下季合约，下季结算价，持仓量，隔季合约，隔季结算价，持仓量
    baseDF = pd.DataFrame(nearDF).append(farDF).append(farfarDF)
    contractCodeList = baseDF["trade_hiscode"].unique().tolist()
    return contractCodeList


class TrsFtInfoLoader(object):
    def __init__(self):
        pass


    def load(self):
        # 获取所有的未导入的新合约信息
        curDate = None
        getAllContracts(curDate)


def main():
    pass


if __name__ == "__main__":
    main()