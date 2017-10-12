# encoding: utf-8
# std
# thd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# app
"""
想搭建一个双engine的环境，来适应未来的生产环境
"""
# 本地数据库MySQL
engine = create_engine('mysql+mysqlconnector://root:12345678@localhost:3306/fixed_income_db?charset=utf8',
                       echo=True,
                       pool_size=20)  # pool size是什么
# keep the lifecycle of the session separate and external from functions and objects
# that access and manipulate database data. This will greatly help with achieving
# a predictable and consistent transactional scope
# Session = sessionmaker(bind=engine)
# session = Session()  # 数据库操作的抽象类，属于全局变量

# 生产环境下的远程数据库MySQL or Oracle
# engine2 = create_engine('mysql+mysqlconnector://root:12345678@localhost:3306/fixed_income_db?charset=utf8',
#                         echo=False,
#                         pool_size=20)
# Session2 = sessionmaker(bind=engine)
