from loguru import logger
import os


def setup_article_logger(log_file_folder: str, log_type: str, log_file_name: str):
    log_file_path = os.path.join(log_file_folder, log_type, log_file_name)
    os.makedirs(log_file_folder, exist_ok=True)
    
    # 创建默认配置的日志
    my_logger = logger.bind(name='Article')
    logger.add(
        log_file_path,
        rotation="1 day",
        format="{time:YYYY-MM-DD at HH:mm:ss} {level} {message}",
        level="DEBUG",
        mode='a',
        filter=lambda record: record["extra"].get("name") == "Article"
    )
    my_logger.level('HIGHLIGHT', no=38, color="<yellow>")
    return my_logger


article_logger = setup_article_logger('log', 'article', 'article_{time:YYYY-MM-DD}.log')

def setup_controller_logger(log_file_folder: str, log_file_name:str):
    log_file_path = os.path.join(log_file_folder, log_file_name)
    os.makedirs(log_file_folder, exist_ok=True)
    
    # 创建总日志
    my_logger = logger.bind(name='Controller')
    logger.add(log_file_path,
               format="{time:YYYY-MM-DD at HH:mm:ss} {level} {message}",
               level='DEBUG',
               mode='a',
               filter=lambda record: record["extra"].get("name") == "Controller"
               )
    return my_logger

controller_logger= setup_controller_logger('log', 'controller.log')
