# article_crawl Linux 部署
本项目依赖于框架scrapy，selenium(额外需要chrome的相关驱动)
```shell
conda create -n article_spider python=3.9
source activate article_spider
conda install scrapy
conda install selenium
# 安装chrome for ；linux
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt update
sudo apt install -y wget gdebi-core
sudo gdebi google-chrome-stable_current_amd64.deb
# 验证安装
google-chrome
# 安装chrome driver
google-chrome --version
wget https://chromedriver.storage.googleapis.com/<version>/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
# 验证安装
chromedriver --version
```
# how to use
# 启动程序 
```shell
cd /article
python run_spider -m xxx -web args1 args2 ...
# 说明 参数m指定了爬取的模式是全部爬取还是增量爬取，可选的参数为full或者add。 参数web为可选参数 如果不指定则默认全部爬取，如果指定则只爬取指定的web
python run_spider -m full
# 对所有的web进行全量爬取
python run_spider -m add
# 对所有的web进行增量爬取
python run_spider -m add -web fortinet githubblog
# 带参数就只会爬取参数部分的， python run_spider -m add -web args1 args2
```