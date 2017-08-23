# encoding: utf-8
"""
BaseTimeSeries是所有时间序列表的基类，定义了一些基础的方法，
规定了时间序列表的特征：1. 必须包含code类型；
                      2. 必须包含trade_date； 
                      3.主键必须包含code, trade_date,可以有第三个主键
"""
# thd
import pandas as pd
from sqlalchemy.sql import text
# app
from Utils import logger
from database import engine  # 导入本地数据库的相关参数
from base import Base


class BaseTimeSeries(Base):

    # ----------------------------------------------------------------------------------------------------
    @classmethod
    def selectDFByCodeAndDateRange(cls, code=None, beginDate=None, endDate=None, columns=None):
        """提取时间选择区间，列名和产品代码提取DataFrame数据，包括开始时间和结束时间
        """
        try:
            conditionList = []
            params = {}
            if columns is None:
                sqlQuery = "select " + cls.columnString + " from " + cls.tableName
            else:
                columnString = " trade_date," + ",".join(columns)
                sqlQuery = "select " + columnString + " from " + cls.tableName
            if code is not None:
                conditionList.append(" code like " + "%(code)s")
                params["code"] = "%" + code + "%"
            if beginDate is not None and endDate is None:
                conditionList.append(" trade_date >= %(beginDate)s")
                params["beginDate"] = beginDate
            elif endDate is not None and beginDate is None:
                conditionList.append(" trade_date <= %(endDate)s")
                params["endDate"] = endDate
            elif beginDate is not None and endDate is not None:
                conditionList.append(" trade_date BETWEEN %(beginDate)s AND %(endDate)s")
                params["beginDate"] = beginDate
                params["endDate"] = endDate
            condition = ""
            if len(conditionList) != 0:
                condition = " where " + conditionList[0]
                for item in conditionList[1:len(conditionList)]:
                    condition += " and " + item
                condition += " order by trade_date asc"
            df = pd.read_sql(sqlQuery + condition, engine,
                             params=params,
                             index_col=['trade_date'])
            return df
        except BaseException as e:
            logger.info('selectDFByCodeAndDateRange fails!{}'.format(e))
            return None

    # -----------------------------------------------------------------------------------
    @classmethod
    def selectMaxDate(cls, target, column="code"):
        """返回datetime"""
        exp = "%" + target + "%"
        try:
            s = text('SELECT max(trade_date) FROM ' + cls.tableName + ' where ' + column + ' like :exp')
            s = s.bindparams(exp=exp)
            res = engine.execute(s)
            resData = res.fetchall()
            if resData is not None and len(resData) > 0:
                return resData[0][0]
            else:
                return None
        except BaseException as e:
            logger.info('selectMaxDate fails!{}'.format(e))
            raise

    # -----------------------------------------------------------------------------------
    @classmethod
    def insertDF(cls, df):
        try:
            df.to_sql(cls.tableName, engine, flavor=None, if_exists='append', index=True)
            return True
        except BaseException as e:
            logger.info('inset data fails!{}'.format(e))
            raise e

