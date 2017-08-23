# encoding: utf-8
"""
规则： info表必须有code主键，但是可以有多个主键
"""

# thd
import pandas as pd
from sqlalchemy.sql import text
# app
from base import Base
from Utils import logger
from database import engine  # 导入本地数据库的相关参数


class BaseInfo(Base):
    tableName = ""

    # --------------------------------------------------------------------------
    @classmethod
    def selectDF(cls, code=None):
        """根据代码选择指定的时间序列，升序排列
        :param code: string
        :return: dataframe
        """

        df = None
        try:
            if code is None:
                df = pd.read_sql_table(table_name=cls.tableName, con=engine)
            elif type(code) is str:
                sqlQuery = "select " + cls.columnString + " from " + cls.tableName
                condition = " where code = %(code)s"
                params = {"code": code}
                df = pd.read_sql(sqlQuery + condition, engine, params=params)
            elif type(code) is list:
                sqlQuery = "select " + cls.columnString + " from " + cls.tableName
                condition = " where code in %(codeList)s"
                params = {"code": ",".join(code)}
                df = pd.read_sql(sqlQuery + condition, engine, params=params)
            return df
        except BaseException as e:
            logger.exception('selectDFByCode fails!{}'.format(e))
            return None

    # -------------------------------------------------------------------------------------
    @classmethod
    def selectAllCodesList(cls, distinct=True):
        """
        :return: list
        """
        try:
            s = text('SELECT ' + ('distinct' if distinct else '') + ' code FROM ' + cls.tableName)
            res = engine.execute(s)
            resData = res.fetchall()
            codeList = []
            if resData is not None and len(resData) > 0:
                for i in range(len(resData)):
                    codeList.append(resData[i][0])
                return codeList
            else:
                return None
        except BaseException as e:
            logger.exception('selectAllCodesList fails!{}'.format(e))
            return None

    # ----------------------------------------------------------------------------------------
    @classmethod
    def insertDF(cls, df):
        try:
            df.to_sql(cls.tableName, engine, flavor=None, if_exists='append', index=False)
            return True
        except BaseException as e:
            logger.exception('inset data fails!{}'.format(e))
            return False
