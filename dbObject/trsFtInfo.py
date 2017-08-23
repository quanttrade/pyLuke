# encoding: utf-8
# std
# thd
# app
from baseInfo import BaseInfo


class TrsFtInfo(BaseInfo):
    """
      `code` varchar(45) NOT NULL COMMENT '交易日期',
      `ipo_date` datetime DEFAULT NULL COMMENT '上市时间',
      `last_trade_date` datetime DEFAULT NULL COMMENT '最后交易日',
      `ld_date` datetime DEFAULT NULL COMMENT '配对缴款日',
    """
    tablename = "fi_ttf_info"  # 表名
    columnList = ["code", "ipo_date", "last_trade_date", "ld_date"]
    columnString = ",".join(columnList)


def test():
    info = TrsFtInfo()
    df = info.selectDF()
    df = info.selectDFByCode("TF1503.CFE")
    print(df)
    codeList = info.selectAllCodesList()
    print(codeList)


if __name__ == "__main__":
    test()
