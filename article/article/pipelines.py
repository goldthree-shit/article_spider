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

from .signals import spider_stop_signal
from .signals import existed_signal

class ArticlePipeline:
    def process_item(self, item, spider=None):
        url = item['url']
        output_dir = item['output_dir']
        download_html = item['download_html']

        # 创建存储的文件夹
        with open('config.yaml', 'r') as file:
            data = yaml.safe_load(file)
            article_save_dir = data['paths']['web']
        crawl_date = datetime.now().strftime('%Y-%m-%d')
        save_dir = os.path.join(article_save_dir, output_dir, crawl_date)
        Path(save_dir).mkdir(parents=True, exist_ok=True)

        sha = hashlib.sha1(download_html.encode("utf-8")).hexdigest()
        if self.check_existed(url, save_dir, sha):
            spider_stop_signal.send_catch_log(existed_signal)

            return item
        logger.info("{} saved".format(url))

        with open(f'{save_dir}/{sha}.html', 'w', encoding='utf-8') as f:
            f.write(download_html)
        return item

    # 检查是否已存在, 如果不存在则更新
    def check_existed(self, url, output_dir, sha):
        record_file = f'{output_dir}/record.json'

        # 如果 record.json 文件不存在，创建文件并写入一个空字典
        if not os.path.exists(record_file):
            os.makedirs(output_dir, exist_ok=True)  # 确保输出目录存在
            with open(record_file, 'w') as f:
                json.dump({}, f)  # 默认写入空的 JSON 对象

        # 读取 record.json 文件的内容
        with open(record_file, 'r') as f:
            record = json.load(f)

        # 检查 URL 是否已经存在
        if url in record:
            logger.info(f"{url} existed")
            return True

        # 如果 URL 不存在，将其添加到记录中
        record[url] = sha

        # 将更新后的记录写回文件
        with open(record_file, 'w') as f:
            json.dump(record, f, indent=4)

        return False