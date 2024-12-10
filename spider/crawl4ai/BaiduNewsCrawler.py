import asyncio
import base64
import json
from pathlib2 import Path

from crawl4ai import AsyncWebCrawler, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

input = "韩国政府"
url = f"http://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&rsv_dl=ns_pc&word={input}"
schema = {
        "name": "News Teaser Extractor",
        "baseSelector": "div[id=content_left] .result-op",
        "fields": [
            {"name": "title", "selector": "h3 a[aria-label]", "type": "attribute", "attribute": "aria-label"},
            {"name": "publish_time", "selector": ".c-row span.c-color-gray2", "type": "text"},
            {"name": "summary", "selector": ".c-row span.c-color-text", "type": "attribute", "attribute": "aria-label"},
            {"name": "link", "selector": "a[href]", "type": "attribute", "attribute": "href"},
            {"name": "source_name", "selector": ".c-row span.c-color-gray", "type": "text"},
        ],
    }


# https://github.com/unclecode/crawl4ai
async def extract_items(input):
    screenshot_file = Path(f"../../screenshots/{Path(__file__).stem}.png")

    extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(
            url=url,
            extraction_strategy=extraction_strategy,
            cache_mode=CacheMode.BYPASS,
            screenshot=True,
        )
        assert result.success, "无法爬取该页面"

        with open(screenshot_file, mode="wb+") as f:
            f.write(base64.b64decode(result.screenshot))
            print(f"把截图保存到{screenshot_file}")
        # Soone will be change to result.markdown
        # print(result.markdown_v2.raw_markdown)
        news_teasers = json.loads(result.extracted_content)
        print(f"成功提取了 {len(news_teasers)} 条")
        print(json.dumps(news_teasers,indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(extract_items(input))
