'''
通过newsapi的能力，获取外国媒体的新闻
优势：不用一个一个采集新闻网站的新闻
缺点：只有英文媒体，不是中文
'''
import asyncio
import base64
import json
import os

import requests
from pathlib2 import Path
from urllib import parse
from dotenv import load_dotenv

from crawl4ai import AsyncWebCrawler

import socket
import socks

# 加载.env文件中的环境变量
load_dotenv()

async def extract_items(source='', input='', country='', category=''):
    screenshot_file = Path(f"../../screenshots/{Path(__file__).stem}.png")
    if source:
        url = f"https://newsapi.org/v2/top-headlines?sources={source}&apiKey={os.getenv('NEWSAPI_KEY')}"
    elif input:
        url = f"https://newsapi.org/v2/top-headlines?q={parse.quote(input)}&apiKey={os.getenv('NEWSAPI_KEY')}"
    elif country:
        url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={os.getenv('NEWSAPI_KEY')}"
    elif category:
        url = f"https://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey={os.getenv('NEWSAPI_KEY')}"
    print(f"crawl url: {url}")

    async with AsyncWebCrawler(
            verbose=True,
            headless=True,
            proxy=os.getenv('PROXY'),
    ) as crawler:
        result = await crawler.arun(
            url=url,
            screenshot=True,
        )
        assert result.success, "无法爬取该页面"

        with open(screenshot_file, mode="wb+") as f:
            f.write(base64.b64decode(result.screenshot))
            print(f"把截图保存到{screenshot_file}")
        # Soone will be change to result.markdown
        raw_response = json.loads(result.markdown_v2.raw_markdown.replace("```", "").strip())
        if raw_response['status'] == 'ok':
            articles = raw_response['articles']
            print(f"成功提取了 {len(articles)} 条")
            for article in articles:
                print(f"title: {article['title']}\ncontent: {article['content']}\nurl: {article['url']}")
                print()
        else:
            print(f"提取失败：{result.markdown_v2.raw_markdown}")



if __name__ == "__main__":
    asyncio.run(extract_items(source='the-wall-street-journal'))
    # asyncio.run(extract_items(country='us'))
    # asyncio.run(extract_items(category='business'))

    # 配置代理，访问newsapi的来源站点
    # socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 10808)
    # socket.socket = socks.socksocket
    # # 来源打印
    # sources = requests.get(f"https://newsapi.org/v2/top-headlines/sources?apiKey={os.getenv('NEWSAPI_KEY')}", proxies=dict(http=os.getenv('PROXY'),
    #                                                                                            https=os.getenv('PROXY')))
    # print(sources.content)
