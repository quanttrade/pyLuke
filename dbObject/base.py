# encoding: utf-8
# std
# thd
# app
import database


class Base(object):
    # 定义三个类属性，每一个数据处理对象都必须有这三个类属性，且必须被子类继承重写
    tablename = ""
    columnList = []
    columnString = ""
