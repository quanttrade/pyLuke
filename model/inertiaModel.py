# encoding: utf-8
import pandas as pd
import numpy as np
import scipy.optimize as spo
"""验证最优配置模型和遍历最优是否具有等价效应"""


def optimize(expect, var):
    """传入期望收益率向量和协方差矩阵
       返回最优权重向量
    """
    x0 = np.ones(len(expect)) / float(len(expect))
    fun = lambda x: -np.dot(x, expect) / sqrt(np.dot(x, var).doct(x))
    cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bnds = [(0, None)] * len(expect)
    res = spo.minimize(fun, x0, tol=1e-6)
    return res.x


def test():
    # encoding: utf-8
    import pandas as pd
    import numpy as np

    """验证最优配置模型和遍历最优是否具有等价效应"""
    # CAPM的方法
    data = pd.read_excel(u"..\\data\\index_ret.xlsx", sheetname=0)
    data.set_index(["date"], inplace=True)
    data = data.ix[0:20, ["038B.CS", "038C.CS"]]
    mean_ret = data.mean() * 250
    var = data.cov() * 250
    w = np.linalg.inv(var).dot(mean_ret)
    w = w / np.sum(w)
    var = w[0] ** 2 * var.iloc[0, 0] + w[1] ** 2 * var.iloc[1, 1] + 2 * w[0] * w[1] * var.iloc[1, 0]
    print w
    print "sharp ratio is {}".format(np.dot(w, mean_ret) / np.sqrt(var))
    # 遍历的方法
    i = 0
    j = 0
    maxsp = 0
    maxi = 0
    for k in range(5000):
        i = k / 100.0 - 5.0
        j = 1 - i
        new_data = data.iloc[:, 0] * i + data.iloc[:, 1] * j
        new_var = new_data.var() * 250
        new_mean = new_data.mean() * 250
        sp = new_mean / np.sqrt(new_var)
        if sp > maxsp:
            maxsp = sp
            maxi = i
    w2 = [maxi, 1 - maxi]
    print w2
    print "sharp_ ratio is {}".format(maxsp)
    # minimize方法
    w3 = optimize(mean_ret.values, var.values)
    print w3


if __name__ == "__main__":
    test()
