# encoding: utf-8
import logging

# 创建一个logger
logger = logging.getLogger(name='mylogger')
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='C:\\Users\\luke wang\\Doing-Projects\\workspace\\PyFixedIncome-rebuild\\pyFixedIncome.log',
                filemode='a')
# 创建一个handler,用于输出控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

logger.info("info message")
