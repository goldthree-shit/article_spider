import argparse
import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

parser = argparse.ArgumentParser(description="Generate URLs and write to a JSON file.")

parser.add_argument("base_url", type=str, help="Base URL to generate.")
parser.add_argument("filename", type=str)

args = parser.parse_args()

base_url = args.base_url
filename = args.filename
paper_links = []
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(options = chrome_options)
driver.get(base_url)
input("请手动解决人类校验问题，然后按 Enter 继续...")
while True:
    elements = driver.find_elements(By.XPATH,"//*[@class='body-post clear']/a")
    json_data = json.dumps([element.get_attribute("href") for element in elements], indent=4)
    with open(filename, 'a') as json_file:
        json_file.write(json_data)
    paper_links.clear()
    try:
        next_page = driver.find_element(By.XPATH, "//*[@id='Blog1_blog-pager-older-link']")
        driver.execute_script("arguments[0].click();", next_page)
        time.sleep(5)
    except:
        print("nonononono")
        break

print(f"文章链接已成功写入{filename}文件。")


#driver.has_element(By.XPATH)
#time.sleep(10)
# for i in range(1,count+1):
#     #url = f"{base_url}{i}"
#     # response = requests.get(url)
#     # response.raise_for_status() 
#     elements = driver.find_elements(By.XPATH,"//*[@class='post__text']/h3/a")
#     paper_links.append([element.get_attribute("href") for element in elements])
#     if i==count:
#         break
#     next_page = driver.find_element(By.XPATH,"//*[@class='atbs-pagination__item atbs-pagination__item-next']")
#     #time.sleep(10)
#     #wait.until(EC.element_to_be_clickable(next_page))
#     #next_page.click()
# #driver.execute_script("$(arguments[0]).click()",next_page)
#     #time.sleep(10)
#     driver.execute_script("arguments[0].click();", next_page)
#     time.sleep(5)


    #wait.until(EC.presence_of_element_located((By.XPATH,"//*[@class='post__text']/h3/a")))
    #wait.until(EC.presence_of_element_located((By.XPATH,"//*[@class='atbs-pagination__item atbs-pagination__item-next']")))



