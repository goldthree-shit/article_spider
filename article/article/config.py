import logging
import logging.config
import time
import os

# 日志设置
def setup_logger(name='my_logger'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # 创建控制台处理器，并设置日志级别
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)

    # 设置日志
    log_file = 'logs/log-{}.log'.format(time.strftime("%Y%m%d-%H%M%S"))
    # 创建日志目录，如果不存在
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # 创建文件处理器，并设置日志级别
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)

    # 创建格式器，并添加到处理器
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # 将处理器添加到日志记录器
    if not logger.handlers:  # 避免重复添加处理器
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger

# 设置默认日志记录器
default_logger = setup_logger()
