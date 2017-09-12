# encoding: utf-8
"""
基于宏观因子布尔信号的大类资产配置模型,参考广发证券大类资产模型
"""
import pandas as pd
import numpy as np


def init(context):
    context.a1 = "039.CS"
    context.a2 = "885006.WI"
    context.assets = [context.a1, context.a2]

    context.TIME_PERIOD = 14


def handle_bar(context, bar_dict):
    pass
