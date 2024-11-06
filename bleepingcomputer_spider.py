import hashlib
import json
import logging
import os
import time
from pathlib import Path

from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 配置日志
logging.basicConfig(
    level=logging.INFO,  # 设置日志级别
    format='%(asctime)s - %(levelname)s - %(message)s',  # 日志格式
    handlers=[logging.StreamHandler()]  # 将日志输出到控制台
)


# 配置 Chrome 选项
chrome_options = Options()
chrome_options.add_argument('--headless')  # 启用无头模式，不弹出浏览器窗口
chrome_options.add_argument('--disable-gpu')  # 禁用GPU，避免某些系统问题
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=chrome_options)

# 检查是否已存在, 如果不存在则更新
def check_existed(url, output_dir, sha):
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
        logging.info(f"{url} existed")
        return True

    # 如果 URL 不存在，将其添加到记录中
    record[url] = sha

    # 将更新后的记录写回文件
    with open(record_file, 'w') as f:
        json.dump(record, f, indent=4)
    return False

# 通过selenium请求子页面
def selenium_parse_child_page(url):
    # 打开新的标签页并获取页面内容
    main_window = driver.current_window_handle
    driver.execute_script(f"window.open('{url}', '_blank');")

    time.sleep(1)
    new_window = [window for window in driver.window_handles if window != main_window][0]
    driver.switch_to.window(new_window)

    content = driver.page_source
    output_dir = 'bleepingcomputer_result'
    sha = hashlib.sha1(content.encode("utf-8")).hexdigest()
    if check_existed(url, output_dir, sha):
        return
    # 创建存储的文件夹
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    Path(output_dir + "/html").mkdir(parents=True, exist_ok=True)

    with open(f'{output_dir}/html/{sha}.html', 'w', encoding='utf-8') as f:
        logging.info(f'{url} saved')
        f.write(content)
    driver.close()
    driver.switch_to.window(main_window)

if __name__ == '__main__':
    try:
        # 访问起始页面
        driver.get('https://www.bleepingcomputer.com/news/security/')
        save_url_xpath = '//*[@id="bc-home-news-main-wrap"]/li/div[1]/a'
        next_page = 'https://www.bleepingcomputer.com/news/security/page/{}/'
        page = 2

        while True:
            time.sleep(2)

            # 交给 Scrapy 解析
            # 获取页面源码
            page_source = driver.page_source
            selector = Selector(text=page_source)
            elements = selector.xpath(save_url_xpath)

            if elements:
                for element in elements:
                    paper_link = element.xpath("@href").get()
                    if paper_link:
                        selenium_parse_child_page(paper_link)
            else:
                break
            # 翻页
            try:
                driver.get(next_page.format(page))
                logging.info(f'next page {page}')
                page += 1
            except Exception as e:
                logging.error(f"翻页出错: {e}")
                break

    finally:
        driver.close()

