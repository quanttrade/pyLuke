# encoding: utf-8
import pandas as pd
from factorEvent import FactorEventCollect

config = {
    "039.CS": {
        "cm": {
            "move_avg_break_through":
                {
                    "mv_count": 30,
                    "forward_count": 1,
                    "lag": 1,
                    "period": 1,
                }
        }
    }

}


class ValidationResult(object):
    pass


def factor_event_validator(factor_dict, factor_event, asset_dict, config, begin_date, end_date):
    """
    第一版本：大类资产的beta因子检验
    可以同时有多个因子和资产，但是只能有一个因子事件
    该方法用于检验beta因子的有效性
    """
    # TODO 读取配置信息
    # 初始化因子事件管理类
    factor_event_collect = FactorEventCollect(factor_dict, config)
    for asset_name in asset_dict:
        print "The current asset is {name}.".format(name=asset_name)
        for factor_name in factor_dict:
            pass

    # 返回结果
    factor_event_info = {"sp": 1,
                         "excess_sp": 0.5,
                         "value_df": pd.DataFrame(),
                         "base_df": pd.DataFrame(),
                         "anual_excess": 0.1,
                         "ir": 0.6,
                         "count": 6}
    return factor_event_info


def alphaFactorValidator(factor_event):
    """
    :param factor_event: 因子事件 
    :return: 
    """
    # TODO
    factor_event_info = {"sp": 1,
                         "excess_sp": 0.5,
                         "value_df": pd.DataFrame(),
                         "base_df": pd.DataFrame(),
                         "anual_excess": 0.1,
                         "ir": 0.6,
                         "count": 6
                         }


def test():
    pass


if __name__ == "__main__":
    test()
