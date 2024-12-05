import asyncio
import json

from crawl4ai import AsyncWebCrawler, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

# https://github.com/unclecode/crawl4ai
async def extract_baidu_news(input):
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
    extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(
            url=f"http://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&rsv_dl=ns_pc&word={input}",
            extraction_strategy=extraction_strategy,
            cache_mode=CacheMode.BYPASS
        )
        assert result.success, "无法爬取该页面"
        # Soone will be change to result.markdown
        # print(result.markdown_v2.raw_markdown)
        news_teasers = json.loads(result.extracted_content)
        print(f"成功提取了 {len(news_teasers)} 條新聞預告")
        print(json.dumps(news_teasers,indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(extract_baidu_news("韩国政府"))