# encoding: utf-8
# std
# thd
import pandas as pd
# app
from dbObject import TrsFtDayTimeSeries
from Utils import WindHelper, logger
from baseTimeSeriesDataLoader import BaseTimeSeriesDataLoader

pd.set_option('mode.chained_assignment', "warn")


class TrsFtDayTimeSeriesLoader(BaseTimeSeriesDataLoader):
    """重写了基类的方法，没有采用基类的原型"""

    def __init__(self):
        self.typeDict = {"TF": ["TF00.CFE", "TF01.CFE", "TF02.CFE"],
                         "T": ["T00.CFE", "T01.CFE", "T02.CFE"]}
        self.windParaList = ["trade_hiscode", "open", "high", "low", "close", "settle", "volume", "oi",
                             "lasttrade_date", "lastdelivery_date"]  # 从wind接口需要提取的数据
        self.trsFtDayTimeSeries = TrsFtDayTimeSeries()

    def start(self):
        self.loadByType("TF")
        self.loadByType("T")

    def loadByType(self, contractType):
        try:
            beginDate, endDate = self.beginAndEndDate(dbObject=TrsFtDayTimeSeries, column="type", target=contractType)
            if beginDate is None:
                if contractType == "TF":
                    beginDate = WindHelper.getInfoDataFrame("TF1312.CFE", ["ipo_date"]).ipo_date[0].to_pydatetime()
                elif contractType == "T":
                    beginDate = WindHelper.getInfoDataFrame("T1509.CFE", "ipo_date").ipo_date[0].to_pydatetime()
            if beginDate.date() <= endDate.date():
                for type_ in self.typeDict[contractType]:
                    df = WindHelper.getTimeSeriesDataFrame(type_, beginDate, endDate, self.windParaList)
                    df.loc[:, "type"] = type_
                    df.rename(columns={'trade_hiscode': 'code'}, inplace=True)
                    #TODO: 需要从TrsFtInfo里面得到信息
                    df["dtltd"] = 0
                    df["dtldd"] = 0
                    for i in range(len(df)):
                        df.ix[i, "dtltd"] = WindHelper.daysCount(df.index[i].to_pydatetime(),
                                                                 df["lasttrade_date"][i].to_pydatetime())
                        df.ix[i, "dtldd"] = WindHelper.daysCount(df.index[i].to_pydatetime(),
                                                                 df["lastdelivery_date"][i].to_pydatetime())
                    df = df[self.trsFtDayTimeSeries.columnList[1:]]
                    logger.info(df.head())
                    TrsFtDayTimeSeries.insertDF(df)
                    logger.info("TrsFtDayTimeSeriesLoader:The daily ts data of {type} "
                                "from {beginDate} to {endDate} has been inserted."
                                .format(type=type_, beginDate=beginDate, endDate=endDate))
        except BaseException as e:
            logger.info(
                "TrsFtDayTimeSeriesLoader:the daily ts data of {type} failed to be inserted, the error info is {info}".format(
                    type=contractType, info=e.message))
            raise


def main():
    loader = TrsFtDayTimeSeriesLoader()
    loader.start()


if __name__ == "__main__":
    # delete()
    main()
