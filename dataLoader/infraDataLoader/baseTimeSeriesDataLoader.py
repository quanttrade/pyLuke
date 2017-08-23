# encoding: utf-8
# thd
from datetime import *
from WindPy import w
# app
from Utils import logger, WindHelper


class BaseTimeSeriesDataLoader(object):
    """从wind导入的df数据默认index是没有名字的datetimeIndex，而字段都是wind自己定义的字段
        需要将wind的数据导入
    """

    def start(self):
        count = 0
        result = False
        for code in self.codeList:
            while count <= 5:
                count += 1
                result = self.loadByCode(code, self.freq)
                if result:
                    count = 0
                    break
            if not result:
                logger.info(u"第 {count} 次导入{code}失败".format(count=count, code=code))

    def loadByCode(self, code, freq="day"):
        try:
            w.start()
            # 确定开始时间和结束时间
            (beginDate, endDate) = self.getBeginAndEndDate(code)
            if freq == "day":
                if beginDate.date() <= endDate.date():
                    df = self.windProduct.__class__.getWindTimeSeriesDataFrame(code, beginDate, endDate,
                                                                               self.windParaList)
                    df = df[self.windParaList]  # 调整字段顺序
                    # df.columns = self.columnList[1:len(self.columnList)]
                    df.rename(columns=self.mapper, inplace=True)
                    df.index.name = self.columnList[0]
                    self.timeSeriesDAO.create()
                    self.timeSeriesDAO.insertDF(df)
                    print("The ts data of {code} from {beginDate} to {endDate} has been inserted.".
                          format(code=code, beginDate=beginDate, endDate=endDate))
            elif freq == "min":  # 需要分段导入，否则数据量太大
                tmpEndDate = min(beginDate + timedelta(days=100), endDate)
                while tmpEndDate <= endDate:
                    if beginDate.date() <= tmpEndDate.date():
                        df = self.windProduct.__class__.getWindMinTimeSeriesDataFrame(code, beginDate, tmpEndDate,
                                                                                      self.windParaList)
                        # 判断是否下载到空数据,如果下载到空数据，则说明数据本身不存在，直接跳过
                        if "outmessage" in df.columns:
                            return True
                        df.rename(columns=self.mapper, inplace=True)
                        df.index.name = self.columnList[0]
                        df["code"] = code
                    self.timeSeriesDAO.create()
                    self.timeSeriesDAO.insertDF(df)
                    print("The ts data of {code} from {beginDate} to {tmpEndDate} has been inserted.".
                          format(code=code, beginDate=beginDate, tmpEndDate=tmpEndDate))
                    if tmpEndDate.date() == endDate.date():
                        break
                    beginDate = tmpEndDate + timedelta(days=1)
                    tmpEndDate = min(tmpEndDate + timedelta(days=100), endDate)
            return True
        except BaseException as e:
            print(e.message)
            return False

    @classmethod
    def beginAndEndDate(cls, dbObject, column, target, ct=19):
        # 确定数据库中已经包含的最大日期
        maxDate = dbObject.selectMaxDate(target=target, column=column)
        if maxDate is None:
            beginDate = None
        else:
            beginDate = WindHelper.getOffsetDays(1, maxDate)
        # 确定结束时间
        formerTradeDate = WindHelper.getOffsetDays()
        if datetime.now().hour >= ct:  # 多少点之后把当天的时间也算进来
            endDate = formerTradeDate
        elif datetime.now().date() > formerTradeDate.date():  # 当天是休息日，最后交易日提前
            endDate = formerTradeDate
        else:
            endDate = WindHelper.getOffsetDays(-1)
        return beginDate, endDate


