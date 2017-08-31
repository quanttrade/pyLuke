# encoding: utf-8
import pandas as pd
import numpy as np
import scipy.optimize as sop
from math import sqrt


def onbar(data, i , cycle):
    opt_w = np.zeros(len(data.columns))
    expect = data.iloc[i - cycle:i, :].mean() * 250
    var = data.cov() * 250
    opt_w = optimize(expect, var)
    return opt_w


def minus_sharp_ratio(expect, var):
    """计算夏普比率,返回一个函数"""
    return lambda x: -np.dot(x, expect) / sqrt(np.dot(x, var).dot(x))


def optimize(expect, var):
    """传入期望收益率向量和协方差矩阵
       返回最优权重向量
    """
    x0 = np.ones(len(expect)) / float(len(expect))
    # fun = lambda x: -np.dot(x, expect) / sqrt(np.dot(x, var).dot(x))
    cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bnds = [(0, 1)] * len(expect)
    res = sop.minimize(minus_sharp_ratio(expect, var), x0, constraints=cons, bounds=bnds, tol=1e-6)
    return res.x


def main():
    # ---公共模块------
    data = pd.read_excel(u"..\\data\\index_ret.xlsx", sheetname=0)
    # data 预处理，去除可转债
    # data = data.iloc[:, [i for i in range(len(data.columns) - 1)]]
    base = pd.read_excel(u"..\\data\\index_ret.xlsx", sheetname=1)
    data.set_index(["date"], inplace=True)
    base.set_index(["date"], inplace=True)
    ret = pd.DataFrame(columns=[i for i in range(1, 21)], index=data.index)
    # -----------------
    for cycle in range(1, 40):
        for i in range(cycle):
            ret.ix[i, cycle] = base.iloc[i, 0]
            opt_w = []
        for i in range(cycle, len(data)):
            if i % cycle == 0:
                # 计算最近一个时间窗口的期望收益率和协方差
                expect = data.iloc[i - cycle:i, :].mean() * 250
                var = data.cov() * 250
                opt_w = optimize(expect, var)
            ret.ix[i, cycle] = np.dot(opt_w, data.ix[i, :].values)
    ret = ret.join(base)
    ret.to_excel("ret.xlsx")
    # 将ret转换为净值曲线
    ret = ret.astype(float)  # 必须加上这句话，否则就无法使用exp函数，原因暂时未知
    value = (np.exp(ret).cumprod())
    value.to_excel("value.xlsx")


if __name__ == "__main__":
    main()
