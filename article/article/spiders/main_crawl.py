import json
import time

import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from ..pipelines import ArticlePipeline
from ..config import default_logger as logger
from ..items import ArticleItem
from selenium.common.exceptions import NoSuchElementException

class MainCrawlSpider(scrapy.Spider):
    name = "main_crawl"

    def __init__(self, spider_target=None, *args, **kwargs):
        super(MainCrawlSpider, self).__init__(*args, **kwargs)
        self.requested_urls = set()
        self.driver = None
        self.output_dir = None
        self.next_page_prefix = None
        self.next_page_spliced = None
        self.next_page_xpath = None
        self.clicked = None
        self.blog_prefix = None
        self.blog_spliced = None
        self.save_url_xpath = None
        self.child_seleniumed = None
        self.seleniumed = None
        self.allowed_domains = None
        self.init(spider_target)

    # 初始化，配置爬虫的相关信息
    def init(self, spider_target):
        config = self.load_config_from_json(spider_target)
        self.start_urls = config['start_urls']
        self.allowed_domains = config['allowed_domains']
        # 起始页面是否需要selenium的支持
        self.seleniumed = config['seleniumed']
        # 子页面是否需要selenium的支持
        self.child_seleniumed = config['child_seleniumed']

        # 需要保存的html页面 的链接提取位置
        self.save_url_xpath = config['save_url_xpath']
        # 是否需要拼接前缀
        self.blog_spliced = config['blog_spliced']
        # 如果需要拼接前缀，则从这里取，否则该属性值无效
        self.blog_prefix = config['blog_prefix']
        # 下一页是否需要点击
        self.clicked = config['clicked']
        # 下一页的xpath
        self.next_page_xpath = config['next_page_xpath']
        # 获取到的链接是否需要拼接域名前缀
        self.next_page_spliced = config['next_page_spliced']
        # 如果需要拼接域名前缀，则这里是前缀，否则该属性值无用
        self.next_page_prefix = config['next_page_prefix']
        # 保存到的目标文件
        self.output_dir = config['output_dir']
        # 如果需要selenium的支持，配置驱动
        if self.seleniumed:
            # 配置 Chrome WebDriver
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # 启用无头模式，不弹出浏览器窗口
            chrome_options.add_argument('--disable-gpu')  # 禁用GPU，避免某些系统问题
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            self.driver = webdriver.Chrome(options=chrome_options)

    def load_config_from_json(self, spider_target):
        # 根据需要爬取的网站名称，读取配置文件
        with open(f'spider_config/{spider_target}.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        logger.info(f"project config: {config}")
        return config


    def start_requests(self):
        # 如果需要selenium的支持，注意会比较慢，翻页和滚动都通过selenium进行
        if self.seleniumed:
            logger.info("use selenium")
            # Selenium 加载页面
            self.driver.get(self.start_urls[0])
            # 如果需要点击翻页
            if self.clicked:
                while True:
                    time.sleep(5)
                    # 获取页面源码
                    page_source = self.driver.page_source
                    # 交给 Scrapy 解析
                    selector = Selector(text=page_source)
                    elements = selector.xpath(self.save_url_xpath)
                    for element in elements:
                        paper_link = self.blog_prefix + element.extract() if self.blog_spliced else element.extract()
                        logger.info(f"will crawl paper {paper_link}")
                        if self.child_seleniumed:
                            self.selenium_parse_child_page(paper_link)
                        else:
                            yield scrapy.Request(url=paper_link, callback=self.parse_page)
                    # 翻页
                    try:
                        next_page = self.driver.find_element(By.XPATH, self.next_page_xpath)
                        if "disabled" in next_page.get_attribute("class") or not next_page:
                            logger.info("已到达最后一页")
                            break
                        logger.info("selenium next page")
                        self.driver.execute_script("arguments[0].click();", next_page)
                    except NoSuchElementException:
                        logger.error("未找到下一页按钮")
                        break
                    except Exception as e:
                        logger.error(f"点击下一页时发生错误: {e}")
                        break
                self.driver.close()
            # 需要滚动获取新内容
            else:
                last_height = self.driver.execute_script("return document.body.scrollHeight")
                # 不停的向下滚动，直到到底
                while True:
                    # 向页面底部滚动
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    # 等待页面加载完成（可以根据页面的实际加载速度调整时间）
                    time.sleep(5)
                    # 计算新的页面高度
                    new_height = self.driver.execute_script("return document.body.scrollHeight")
                    # 判断是否加载完成
                    if new_height == last_height:
                        break
                    last_height = new_height
                # 获取页面源码
                page_source = self.driver.page_source
                # 交给 Scrapy 解析
                selector = Selector(text=page_source)
                elements = selector.xpath(self.save_url_xpath)
                for element in elements:
                    paper_link = self.blog_prefix + element.extract() if self.blog_spliced else element.extract()
                    logger.info(f"will crawl paper {paper_link}")
                    if self.child_seleniumed:
                        self.selenium_parse_child_page(paper_link)
                    else:
                        yield scrapy.Request(url=paper_link, callback=self.parse_page)
                self.driver.close()
        # 如果不需要，直接获取就好
        else:
            # 这里你可以根据参数定义不同的起始请求
            logger.info("use scrapy")
            yield scrapy.Request(url=self.start_urls[0], callback=self.parse)


    def parse(self, response):
        elements = response.xpath(self.save_url_xpath)
        for element in elements:
            paper_link = self.blog_prefix + element.extract() if self.blog_spliced else element.extract()
            logger.info(f"will crawl paper {paper_link}")
            yield scrapy.Request(url=paper_link, callback=self.parse_page)

        next_page = response.xpath(self.next_page_xpath).extract_first()
        if next_page:
            next_page_url = self.next_page_prefix + next_page if self.next_page_spliced else next_page
            logger.info("next page : {}".format(next_page_url))
            yield scrapy.Request(url=next_page_url, callback=self.parse)


    def parse_page(self, response):
        item = ArticleItem()
        item['download_html'] = response.text
        item['url'] = response.url
        item['output_dir'] = self.output_dir
        yield item


    # 通过selenium请求子页面
    def selenium_parse_child_page(self, url):
        if url in self.requested_urls:
            return
        else:
            self.requested_urls.add(url)

        # 打开新的标签页并获取页面内容
        main_window = self.driver.current_window_handle
        self.driver.execute_script(f"window.open('{url}', '_blank');")

        time.sleep(1)
        new_window = [window for window in self.driver.window_handles if window != main_window][0]
        self.driver.switch_to.window(new_window)

        content = self.driver.page_source

        # Yield item to Scrapy's pipeline
        item = ArticleItem()
        item['download_html'] = content
        item['url'] = url
        item['output_dir'] = self.output_dir
        article = ArticlePipeline()
        article.process_item(item)
        # 关闭新窗口并切换回原窗口
        self.driver.close()
        self.driver.switch_to.window(main_window)