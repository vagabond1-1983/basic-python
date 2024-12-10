import asyncio
import base64
import json
from pathlib2 import Path

from crawl4ai import AsyncWebCrawler, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

url = f"https://top.baidu.com/board?tab=realtime"
schema = {
    "name": "Baidu Hot Search News Teaser Extractor",
    "baseSelector": ".container-bg_lQ801 .category-wrap_iQLoo",
    "fields": [
        {"name": "title", "selector": ".content_1YWBm .c-single-text-ellipsis", "type": "text"},
        {"name": "summary", "selector": ".content_1YWBm .large_nSuFU", "type": "text"},
        {"name": "hot_point", "selector": ".trend_2RttY .hot-index_1Bl1a", "type": "text"},
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
