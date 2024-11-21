# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    url = scrapy.Field()
    web_name = scrapy.Field()
    download_html = scrapy.Field()
    output_dir = scrapy.Field()
    pass
