#!/bin/bash

# Navigate to the specified path
cd /Users/huangyh/File/华为项目恶意代码-情报分析/情报分析/article_spider/article || {
  echo "Failed to navigate to the specified directory.";
  exit 1;
}

# Specify the Python interpreter path
PYTHON_INTERPRETER="/opt/anaconda3/envs/scrapy/bin/python"

# Check if the Python interpreter exists
if [ ! -x "$PYTHON_INTERPRETER" ]; then
  echo "Python interpreter not found at $PYTHON_INTERPRETER.";
  exit 1;
fi

$PYTHON_INTERPRETER run_spider.py -web bleepingcomputer -m add
$PYTHON_INTERPRETER run_spider.py -web checkmarx-blog -m add
$PYTHON_INTERPRETER run_spider.py -web checkpoint -m add
$PYTHON_INTERPRETER run_spider.py -web cybersecuritynews -m add
$PYTHON_INTERPRETER run_spider.py -web fortinet -m add
$PYTHON_INTERPRETER run_spider.py -web githubblog -m add
$PYTHON_INTERPRETER run_spider.py -web iqt -m add
$PYTHON_INTERPRETER run_spider.py -web jfrog -m add
$PYTHON_INTERPRETER run_spider.py -web phylum -m add
$PYTHON_INTERPRETER run_spider.py -web reversinglabs -m add
$PYTHON_INTERPRETER run_spider.py -web securityintelligence -m add
$PYTHON_INTERPRETER run_spider.py -web snyk -m add
$PYTHON_INTERPRETER run_spider.py -web socketdev -m add
$PYTHON_INTERPRETER run_spider.py -web sonatype -m add
$PYTHON_INTERPRETER run_spider.py -web tencent -m add
$PYTHON_INTERPRETER run_spider.py -web thehackernews -m add
$PYTHON_INTERPRETER run_spider.py -web theregister -m add

echo "All commands executed successfully."