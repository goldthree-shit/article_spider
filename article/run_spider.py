from scrapy.crawler import CrawlerProcess
from article.spiders.main_crawl import MainCrawlSpider
from scrapy.utils.project import get_project_settings
import multiprocessing
def crawl_website(website):
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(MainCrawlSpider, spider_target=website)
    process.start()

if __name__ == '__main__':
    target_websites = ["githubblog", "jfrog", "sonatype", "snyk", "tencent", "checkpoint",
                       "checkmarx-blog", "theregister", "securityintelligence", "thehackernews", "phylum", "iqt"]

    with multiprocessing.Pool(processes=len(target_websites)) as pool:
        pool.map(crawl_website, target_websites)

# if __name__ == '__main__':
#     crawl_website("checkpoint")



