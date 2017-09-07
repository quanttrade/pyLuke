# encoding: utf-8
# thd
from WindPy import w
import pandas as pd
from datetime import timedelta, datetime


class WindHelper(object):
    """
    WindPy20170904更新
    在本次修改后, 下面函数结果中的时间Times将只包含日期date: 
    wsd, tdays, tdayscount, tdaysoffset, wset, weqs, wpd, htocode, edb
    常用字段：
    close
    settle
    volume
    """
    @staticmethod
    def getMultiTimeSeriesDataFrame(codeList, beginDate, endDate, para, period="",
                                    tradingCalendar="", priceAdj="", credibility=0):
        """
        para只能是一个参数
        get time series from windPy, each code represents one capture
         月度合约: trade_hiscode
           :param credibility: (int)
           :param codeList: (list)
           :param beginDate: (date or datetime)
           :param endDate: (date or datetime)
           :param para: (string)只能是一个字符参数
           :param period: (int) 频率
           :param tradingCalendar: (string)   交易日历，选择可以选择银行间:NIB,不选择，则默认交易所日历
           :param priceAdj: (string) 价格是否调整,F:前复权，B:后复权
           :return: (DataFrame)
        """
        try:
            w.start()
            codeListStr = ",".join(codeList)
            period = ("Period=" + period) if period == "W" else ""
            tradingCalendar = ("TradingCalendar=" + tradingCalendar) if tradingCalendar != "" else ""
            priceAdj = ("priceAdj=" + priceAdj) if priceAdj != "" else ""
            credibility = ("credibility=" + str(credibility)) if credibility != 0 else ""
            windData = w.wsd(codeListStr,
                             para,
                             beginDate.strftime("%Y-%m-%d"),
                             endDate.strftime("%Y-%m-%d"),
                             period,
                             tradingCalendar,
                             priceAdj, credibility)
            if len(windData.Data) == 0:
                raise BaseException
            if len(windData.Data[0]) == 0:
                raise BaseException
            dataDict = {}
            for i in range(len(windData.Data)):
                dataDict[windData.Codes[i].lower() + "_" + para] = windData.Data[i]
            df = pd.DataFrame(dataDict, index=windData.Times)
            df.index = pd.to_datetime(df.index)
            df.index.name = "trade_date"
            return df
        except BaseException as e:
            print(e.message)
            raise

    @staticmethod
    def getTimeSeriesDataFrame(code, beginDate, endDate, paraList, period="",
                                   tradingCalendar="", priceAdj="", credibility=0):
        """
        get time series from windPy, each code represents one capture
         月度合约: trade_hiscode
           :param credibility: (int)
           :param code: (string)
           :param beginDate: (date or datetime)
           :param endDate: (date or datetime)
           :param paraList: (list)
           :param period: (int) 频率
           :param tradingCalendar: (string)   交易日历，选择可以选择银行间:NIB,不选择，则默认交易所日历
           :param priceAdj: (string) 价格是否调整,F:前复权，B:后复权
           :return: (DataFrame)
        """
        try:
            w.start()
            para = ",".join(paraList)
            period = ("Period=" + period) if period == "W" else ""
            tradingCalendar = ("TradingCalendar=" + tradingCalendar) if tradingCalendar != "" else ""
            priceAdj = ("priceAdj=" + priceAdj) if priceAdj != "" else ""
            credibility = ("credibility=" + str(credibility)) if credibility != 0 else ""
            windData = w.wsd(code,
                             para,
                             beginDate.strftime("%Y-%m-%d"),
                             endDate.strftime("%Y-%m-%d"),
                             tradingCalendar,
                             priceAdj, credibility)
            if len(windData.Data) == 0:
                raise BaseException
            if len(windData.Data[0]) == 0:
                raise BaseException
            dataDict = {}
            for i in range(len(windData.Data)):
                dataDict[windData.Fields[i].lower()] = windData.Data[i]
            df = pd.DataFrame(dataDict, index=windData.Times)
            df.index = pd.to_datetime(df.index)
            df.index.name = "trade_date"
            return df
        except BaseException as e:
            print(e.message)
            raise

    @staticmethod
    def getMinTimeSeriesDataFrame(code, beginDate, endDate, paraList, bar_size=1):
        """
        获取分钟级别数据
        get time series from windPy, each code represents one capture
         月度合约: trade_hiscode
           :param bar_size: (int)  The frequency of the data
           :param code: string
           :param beginDate: date or datetime
           :param endDate: date or datetime
           :param paraList: list
           :return: DataFrame
        """
        try:
            w.start()
            para = ",".join(paraList)
            bar_size = "" + bar_size if bar_size is not None else ""
            windData = w.wsi(code,
                             para,
                             beginDate.strftime("%Y-%m-%d %H:%M:%S"),
                             endDate.strftime("%Y-%m-%d %H:%M:%S"), "")
            if len(windData.Data) == 0:
                raise BaseException
            if len(windData.Data[0]) == 0:
                raise BaseException
            dataDict = {}
            for i in range(len(windData.Data)):
                dataDict[windData.Fields[i].lower()] = windData.Data[i]
            df = pd.DataFrame(dataDict, index=windData.Times)
            if df.index[0].to_pydatetime().microsecond != 0:
                df.index -= timedelta(microseconds=df.index[0].to_pydatetime().microsecond)
            df.index.name = "trade_date"
            return df
        except BaseException as e:
            print(e.message)
            raise

    @staticmethod
    def getInfoDataFrame(code, paraList):
        """
        get info of one product by code
        :return: DataFrame
        :param code:
        :param paraList:
        :return:  DataFrame;
        """
        try:
            w.start()
            para = ",".join(paraList)
            windData = w.wss(code,
                             para)
            if len(windData.Data) == 0:
                return None
            if len(windData.Data[0]) == 0:
                return None
            dataDict = {}
            for i in range(len(windData.Data)):
                dataDict[windData.Fields[i].lower()] = windData.Data[i]
            df = pd.DataFrame(dataDict)
            df = df[paraList]
            return df
        except BaseException as e:
            print(e.message)
            raise

    @staticmethod
    def getEDBTimeSeriesDataFrame(codeList, beginDate, endDate, fillChoice="Previous"):
        """
        宏观数据提取
        get edb time series from windPy, each code represents one capture
        : Param fillChoice: (string) previous或者None，空值数据是否需要被前一日的数据取代
        """
        codeListStr = ",".join(codeList)
        try:
            w.start()
            if fillChoice == "Previous":
                windData = w.edb(codeListStr,
                                 beginDate.strftime("%Y-%m-%d"),
                                 endDate.strftime("%Y-%m-%d"),
                                 "Fill=" + fillChoice)
            else:
                windData = w.edb(codeListStr,
                                 beginDate.strftime("%Y-%m-%d"),
                                 endDate.strftime("%Y-%m-%d"))
            if len(windData.Data) == 0:
                return None
            if len(windData.Data[0]) == 0:
                return None
            dataDict = {}
            for i in range(len(windData.Data)):
                dataDict[windData.Codes[i]] = windData.Data[i]
            df = pd.DataFrame(dataDict, index=windData.Times)
            df.index = pd.to_datetime(df.index)
            df.index.name = "trade_date"
            return df
        except BaseException as e:
            print(e.message)
            raise

    @staticmethod
    def getOffsetDays(offset=0, curDate=datetime.now()):
        try:
            w.start()
            result = w.tdaysoffset(offset, curDate.strftime("%Y-%m-%d"), "").Data[0][0]
            return result
        except IndexError as e:
            print(e.message)
            raise

    @staticmethod
    def daysCount(firstDate, secondDate):
        w.start()
        result = w.tdayscount(firstDate.strftime("%Y-%m-%d"), secondDate.strftime("%Y-%m-%d"), "").Data[0][0]
        return result

    @staticmethod
    def getAllTrsFtCodes(beginDate, endDate):
        w.start()
        pass


def test():
    beginDate = datetime(2008, 12, 1)
    endDate = datetime(2017, 8, 30)
    # df = WindHelper.getEDBTimeSeriesDataFrame(["S0059749"], beginDate=beginDate, endDate=endDate)
    codeList = ["T1612.CFE", "T1703.CFE"]
    para = "settle"
    df = WindHelper.getMultiTimeSeriesDataFrame(codeList=codeList, beginDate=datetime(2016, 5, 1),
                                                endDate=datetime(2016, 12, 11), para=para)
    print(df)


if __name__ == "__main__":
    test()
