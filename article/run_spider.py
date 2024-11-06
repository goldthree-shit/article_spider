import os

from scrapy.crawler import CrawlerProcess
from article.spiders.main_crawl import MainCrawlSpider
from scrapy.utils.project import get_project_settings
import multiprocessing
import sys

def crawl_website(param):
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(MainCrawlSpider, param=param)
    process.start()

if __name__ == '__main__':
    full_mode = True
    folder_path = './spider_config'
    target_websites_dedicate = [file.split('.')[0] for file in os.listdir(folder_path)]
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and (sys.argv[-1] == 'full' or sys.argv[-1] == 'add')):
        target_websites = target_websites_dedicate
        if len(sys.argv) > 1:
            full_mode = sys.argv[-1] == 'full'
    else:
        if sys.argv[-1] == 'full' or sys.argv[-1] == 'add':
            target_websites = sys.argv[1:-1]
            full_mode = sys.argv[-1] == 'full'
        else:
            target_websites = sys.argv[1:]
        for website in target_websites:
            if website not in target_websites_dedicate:
                print(f'"{website}" is not define')
                exit(0)
    # 构建每个网站的独立参数字典
    params = [{'target_websites': website, 'full_mode': full_mode} for website in target_websites]

    with multiprocessing.Pool(processes=len(target_websites)) as pool:
        pool.map(crawl_website, params)



