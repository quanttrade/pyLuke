# encoding: utf-8
import pandas as pd
import numpy as np





def test():
    # 读取数据文件
    # value_data = pd.read_excel(u"..\\data\\中债指数资产.xlsx",0, header=0, skiprows=[0,1,3,4])
    # tmp_columns = value_data.columns.values
    # tmp_columns[0] = "date"
    # value_data.columns = tmp_columns
    data = pd.read_excel(u"..\\data\\中债指数资产.xlsx",0, header=0, skiprows=[0,1,3,4])
    tmp_columns = data.columns.values
    tmp_columns[0] = "date"
    data.columns = tmp_columns
    data.set_index('date', inplace=True)
    print data.index
    # 参数设定及计算
    equalReturn = data.mean()*250   # 年华均衡收益
    covMat = data.cov()*250  # 年化协方差矩阵
    delta = 2
    tau = 0.03
    # 输入观点
    P = []




if __name__ == "__main__":
    test()