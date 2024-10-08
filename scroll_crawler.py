import argparse
import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

# parser = argparse.ArgumentParser(description="Generate URLs and write to a JSON file.")
# parser.add_argument("filename", type=str)
#
# args = parser.parse_args()

filename = "output1.json"


# 初始化WebDriver（请确保chromedriver在你的系统路径中，或者提供它的路径）
driver = webdriver.Chrome()

# 打开目标网页
driver.get("https://www.theregister.com/security")

# 模拟滚动页面以加载更多内容
SCROLL_PAUSE_TIME = 3
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # 滚动到页面底部
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # 等待页面加载
    time.sleep(SCROLL_PAUSE_TIME)

    # 计算新的滚动高度并与之前的滚动高度进行比较
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

paper_links = []
elements = driver.find_elements(By.XPATH, "//*[@class='story_link']")
# elements = WebDriverWait(driver,30).until(
#         EC.presence_of_all_elements_located((By.XPATH, '//*[@id="_obv.shell._surface_1716515988707"]/div/div[4]/div/section/div/div/div[2]/a/@href'))
#     )
print(len(elements))
paper_links.append(["https://www.theregister.com"+element.get_attribute("href") for element in elements])
#article_links = dom.xpath('//*[@id="_obv.shell._surface_1716515988707"]/div/div[4]/div/section/div/div/div[2]/a/@href')
#print(article_links)
# sonatype
#paper_links.append([prefix+link for link in article_links])
#paper_links.append(article_links)
print(len(paper_links))
json_data = json.dumps(paper_links, indent=4)
with open(filename, 'w') as json_file:
    json_file.write(json_data)

print(f"文章链接已成功写入{filename}文件。")

# 关闭浏览器
driver.quit()

