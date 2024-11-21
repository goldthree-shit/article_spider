import os
import pymysql
from scrapy.crawler import CrawlerProcess
from article.spiders.main_crawl import MainCrawlSpider
from scrapy.utils.project import get_project_settings
import multiprocessing
import argparse
from datetime import datetime
from logger_config import controller_logger as logger
import traceback

parser = argparse.ArgumentParser(description='web crawl')
parser.add_argument('-web', nargs='*', type=str, help='A list of websites')
parser.add_argument('-m', choices=['add','full'], required=True)
args = parser.parse_args()

def crawl_website(param):
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(MainCrawlSpider, param=param)
    process.start()

if __name__ == '__main__':
    logger.info(f"启动对网站的爬取")
    full_mode = args.m == 'full'
    web_specific = args.web # 可选参数 指定个别web进行爬取 默认全部爬取
    folder_path = './spider_config'
    target_websites_dedicate = [file.split('.')[0] for file in os.listdir(folder_path)]
    if web_specific is None:
        params = [{'target_websites': website, 'full_mode': full_mode} 
                  for website in target_websites_dedicate]
    else:
        params = [{'target_websites': website, 'full_mode': full_mode} 
                  for website in target_websites_dedicate
                  if web_specific is not None and website in web_specific]

    with multiprocessing.Pool(processes=len(params)) as pool:
        pool.map(crawl_website, params)
    
    connection = pymysql.connect(
        host='10.176.56.233',
        port=3310,
        user='root',
        password='114514',
        database='intelligenceSource'
    )
    current_date = datetime.now().strftime('%Y-%m-%d')
    query = """
        SELECT * FROM source WHERE crawl_date = "{}" and source = "{}";
    """
    try:
        with connection.cursor() as cursor:
            for param in params:
                cursor.execute(query.format(current_date, param['target_websites']))
                result = cursor.fetchall()
                logger.info(f"本次对 {param['target_websites']} 爬取新增条目 {len(result)}")
    except Exception as e:
        logger.error(traceback.format_exc())
    finally:
        if connection:
            connection.close()
