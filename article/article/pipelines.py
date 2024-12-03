# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
import json
import os
from pathlib import Path
import yaml
from scrapy import signals
from datetime import datetime
from logger_config import article_logger as logger
import pymysqlpool
from .signals import spider_stop_signal
from .signals import existed_signal

pool = pymysqlpool.ConnectionPool(host='10.176.56.233', port=3310,
                                  user='root', password='114514', database='intelligenceSource', size=3)


class ArticlePipeline:
    def process_item(self, item, spider=None):
        url = item['url']
        output_dir = item['output_dir']
        download_html = item['download_html']
        web_name = item['web_name']

        # 创建存储的文件夹
        with open('config.yaml', 'r') as file:
            data = yaml.safe_load(file)
            article_save_dir = data['paths']['web']
        crawl_date = datetime.now().strftime('%Y-%m-%d')
        save_dir = os.path.join(article_save_dir, output_dir, crawl_date)
        Path(save_dir).mkdir(parents=True, exist_ok=True)

        sha = hashlib.sha1(download_html.encode("utf-8")).hexdigest()
        if self.check_existed(url, sha, web_name):
            logger.info(f"[{web_name}] 爬取到重复的内容")
            spider_stop_signal.send_catch_log(existed_signal)
            return item
        else:
            self.insert_into_db_source(url, sha, web_name, crawl_date)
            logger.info(f"[{web_name}] saved".format(url))
            with open(f'{save_dir}/{sha}.html', 'w', encoding='utf-8') as f:
                f.write(download_html)
            return item

    # 检查是否已存在, sha暂时保留
    def check_existed(self, url, sha, web_name):
        is_exist = False
        connection = pool.get_connection()
        cursor = connection.cursor()
        sql_query = f"""
        SELECT * FROM source WHERE source = "{web_name}" and link = "{url}";
        """
        cursor.execute(sql_query)
        result = cursor.fetchall()
        if len(result) > 0:
            is_exist = True
        connection.close()
        return is_exist

    def insert_into_db_source(self, url, sha, web_name, crawl_date):
        connection = pool.get_connection()
        cursor = connection.cursor()
        sql_insert = f"""
        INSERT INTO source (source, link, hash_value, crawl_date)
        VALUES (%s, %s, %s, %s)
        """
        data = (web_name, url, sha, crawl_date)
        cursor.execute(sql_insert, data)
        connection.commit()
        connection.close()
