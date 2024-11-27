1. 搜索引擎
MITER ATLAS 
- https://atlas.mitre.org/ 暂无 
2. gitee, github区 
- https://github.blog/category/security    done
3. 安全厂商:
- https://jfrog.com/blog done
- https://blog.sonatype.com done
- https://snyk.io/blog/category/application-security done
- https://security.tencent.com/index.php/blog  done
- https://checkmarx.com/blog   done 需要关闭无头模式
- https://medium.com/checkmarx-security -重定向> https://zero.checkmarx.com/, fail，selenium打不开，一直显示加载时间过长
- https://blog.checkpoint.com done 需要关闭无头模式
4. 媒体 
- https://www.bleepingcomputer.com/news/security  done/fail, 偶尔会触发真人检测，尚不清楚规律，需要js 和 cookies，并且有selenium真人检测，无法规避
- https://www.theregister.com/security   done
- https://securityintelligence.com/news done，由于html源文件有问题，需要使用selenium进行修复之后，取快照在进行提取，
- https://thehackernews.com  done
5. 其它 
- https://www.iqt.org/knowledge-hub?category=Cyber#full-library done 需要VPN
6. news
- https://www.scmagazine.com done, 通过滚动翻页，所以需要滚动到最底下之后，在爬取
- https://blog.phylum.io/ done
- https://socket.dev/blog done
- https://www.reversinglabs.com/blog done
- https://cybersecuritynews.com/ done
- https://www.fortinet.com/blog done
- 
# 需要安装的依赖 
```shell
pip install scrapy
pip install selenium
见chrome测试驱动配置文档
```
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
# 配置文件说明
- 存放的文件夹 `/article_crawl/article/spider_config`
- example: 文件名`githubblog.json`， 程序会通过githubblog找到该配置文件
```json
{
  "name": "githubblog",  // 名称
  "start_urls": ["https://github.blog/security/"],  // 起始的url
  "allowed_domains": ["github.blog"],              // 允许的域名
  "seleniumed": false,                             // 访问起始的url是否需要启用selenium，适用于html源代码有问题 或 有一些强制需要浏览器，js支持的网页
  "child_seleniumed": false,                       // 爬取子页面是否需要启用selenium
  "save_url_xpath": "//*[@id=\"start-of-content\"]/div[2]/div/div/article/div/h3//@href", // 访问子页面提取的xpath
  "blog_spliced": false,                              // 访问子页面提取到的xpath是否需要前缀
  "blog_prefix": "",                                //  blog_spliced = true有用，表示前缀的具体值
  "clicked": true,                             // true 点击翻页，仅在启用了seleniumed有用，因为scrapy是直接请求接口的，与浏览器行为无关
  "roll": false,                               // false 滚动翻页，仅在启用了seleniumed有用
  "next_page_xpath": "//*[@id=\"start-of-content\"]/div[2]/div/div[2]/nav/div/a[last()]/@href", // 翻页的xpath位置，如果是使用selenium进行翻页，无需/@href部分
  "next_page_spliced": false,                     // 翻页的url是否需要拼接前缀，仅在使用scrapy时work
  "next_page_prefix": "",                          // 翻页的url是否具体拼接前缀，仅在next_page_spliced=true时work
  "output_dir": "githubblg_result"              // 爬取到的结果输出的文件夹, 可以采用相对/绝对
}
```