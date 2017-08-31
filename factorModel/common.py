# encoding: utf-8
import math
import numpy as np


config = {
    "039.CS": {
        "cm": {
            "avg_break":
                {
                    "postive": True,
                    "his_count": 30,
                    "std_count": 0
                },
            "cont_up":
                {
                    "cont_count": 3
                }
        }
    }

}


def sharpe_ratio(series, risk_free_rate=0.03):
    """计算夏普比率
    :param series: 
    :param risk_free_rate: 
    :return: 
    """
    daily = series[1:].values / series[:-1] - 1
    sp = math.sqrt(250) * (np.average(daily) - risk_free_rate / 250.0) / np.std(daily)
    return sp

