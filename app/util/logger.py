# logger.py
import os
from util import constant
from datetime import datetime
import logging


log_file_prefix = 'log_'
# 获取当前日期，格式化为%Y%m%d
current_date = datetime.now().strftime('%Y%m%d')
# 日志文件名后缀
log_file_suffix = '.log'
# 完整的日志文件路径
log_file_path = os.path.join(constant.log_path, log_file_prefix + current_date + log_file_suffix)

# 检查日志目录是否存在，如果不存在则创建
if not os.path.exists(constant.log_path):
    os.makedirs(constant.log_path)

# 创建一个logger
logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)

# 创建一个handler，用于写入日志文件
fh = logging.FileHandler(log_file_path)
#fh.setLevel(logging.INFO)
fh.setLevel(logging.INFO)

# 创建一个handler，用于将日志输出到控制台
ch = logging.StreamHandler()
#ch.setLevel(logging.INFO)
ch.setLevel(logging.INFO)

# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(fh)
logger.addHandler(ch)
