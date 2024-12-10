import asyncio
import base64
import json
from pathlib2 import Path

from crawl4ai import AsyncWebCrawler, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
"""
废弃：新闻只有标题没有内容，总排行不好定位只能按照位置定位
"""

url = f"https://news.sina.com.cn/hotnews/"
schema = {
    "name": "Sina Hot News Teaser Extractor",
    "baseSelector": ".loopblk:nth-of-type(1) div[id=Con11] table tbody tr",
    "fields": [
        {"name": "no", "selector": "td:nth-of-type(1)", "type": "text"},
        {"name": "title", "selector": "td[class=ConsTi] a", "type": "text"},
        {"name": "link", "selector": "td[class=ConsTi] a[href]", "type": "attribute", "attribute": "href"},
        {"name": "source", "selector": "td:nth-of-type(3)", "type": "text"},
        {"name": "time", "selector": "td:nth-of-type(4)", "type": "text"},
    ],
}


# https://github.com/unclecode/crawl4ai
async def extract_items(input):
    screenshot_file = Path(f"../../screenshots/{Path(__file__).stem}.png")

    extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)
    async with AsyncWebCrawler(
            verbose=True,
            headless=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    ) as crawler:
        result = await crawler.arun(
            url=url,
            extraction_strategy=extraction_strategy,
            cache_mode=CacheMode.BYPASS,
            screenshot=True,
            # screenshot_wait_for=5.0,  # Wait 2 seconds before capture
            # magic=True,  # Enables all anti-detection features
        )
        assert result.success, "无法爬取该页面"

        with open(screenshot_file, mode="wb+") as f:
            f.write(base64.b64decode(result.screenshot))
            print(f"把截图保存到{screenshot_file}")
        # Soone will be change to result.markdown
        # print(result.markdown_v2.raw_markdown)
        news_teasers = json.loads(result.extracted_content)
        print(f"成功提取了 {len(news_teasers)} 条")
        print(json.dumps(news_teasers, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(extract_items(input))
