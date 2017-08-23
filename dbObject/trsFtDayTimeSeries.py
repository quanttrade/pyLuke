# encoding: utf-8
# thd
from sqlalchemy import Float, text
import pandas as pd
# app
from Utils import logger
from baseTimeSeries import (BaseTimeSeries, engine)


class TrsFtDayTimeSeries(BaseTimeSeries):
    """
    国债期货时间序列表对象
    字段信息：
      `trade_date` DATETIME NOT NULL COMMENT '交易日期',
      `code` VARCHAR(45) NOT NULL COMMENT '合约代码',
      `type` VARCHAR(45) NULL COMMENT 'T00,T01 or T02',
      `open` DOUBLE(20,5) NULL COMMENT '开盘价',
      `high` DOUBLE(20,5) NULL COMMENT '最高价',
      `low` DOUBLE(20,5) NULL COMMENT '最低价',
      `close` DOUBLE(20,5) NULL COMMENT '收盘价',
      `settle` DOUBLE(20,5) NULL, COMMENT '结算价',
      `volume` DOUBLE(20,5) NULL COMMENT '成交价',
      `oi` DOUBLE(20,5) NULL COMMENT 'open interest 持仓量',
      `dtltd` INTEGER NULL COMMENT '距离最后交易日日期',
      `dtldd` INTEGER NULL COMMENT '距离配对缴款日日期',
    """
    tableName = 'fi_ttf_day_ts'
    columnList = ["trade_date", "code", "type", "open", "high", "low", "close", "settle", "volume", "oi", "dtltd",
                  "dtldd"]
    columnString = ",".join(columnList)

    # ----------------------------------------------------------------------------------------------------
    @classmethod
    def selectMaxDateByType(cls, simpleContractType):
        """返回datetime"""
        exp = "%" + simpleContractType + "0%"
        try:
            s = text('SELECT max(trade_date) FROM ' + cls.tableName + ' where type like :exp')
            s = s.bindparams(exp=exp)
            conn = engine.connect()
            res = conn.execute(s)
            resData = res.fetchall()
            if resData is not None and len(resData) > 0 and resData[0] is not None:
                return resData[0][0]
            else:
                return None
        except BaseException as e:
            logger.info('selectMaxDate fails!{}'.format(e))
            return None

    # ----------------------------------------------------------------------------------------------------
    @classmethod
    def selectDFByType(cls, contractType, beginDate=None, endDate=None):
        """根据合约类型进行数据提取，TF01.CFE, TF02.CFE, TF00.CFE etc.
            日期默认升序排列
            beginDate 和 endDate都包括
        """
        try:
            sqlQuery = "select " + cls.columnString + " from " + cls.tableName

            if beginDate is not None and endDate is None:
                condition = " where type = %(type)s" + " where trade_date >= %(beginDate)s"
                params = {"type": contractType, "beginDate": beginDate}
            elif endDate is not None and beginDate is None:
                condition = " where type = %(type)s" + " where trade_date <= %(endDate)s"
                params = {"type": contractType, "endDate": endDate}
            elif beginDate is not None and endDate is not None:
                condition = " where type = %(type)s" + " where trade_date BETWEEN %(beginDate)s AND %(endDate)s"
                params = {"type": contractType, "beginDate": beginDate, "endDate": endDate}
            else:
                condition = " where type = %(type)s"
                params = {"type": contractType}
            df = pd.read_sql(sqlQuery + condition, engine,
                             params=params,
                             index_col=['trade_date'])
            return df
        except BaseException as e:
            logger.info('selectDFByType fails!{}'.format(e))
            return None


def test():
    df = TrsFtDayTimeSeries.selectDFByCodeAndDateRange(code="T1703.CFE", columns=["settle"])
    # logger.info(df)


if __name__ == "__main__":
    test()
