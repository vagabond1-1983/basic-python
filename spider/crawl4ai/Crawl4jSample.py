import asyncio
import json

from crawl4ai import AsyncWebCrawler, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

# https://github.com/unclecode/crawl4ai
async def main():
    schema = {
        "name": "News Teaser Extractor",
        "baseSelector": ".wide-tease-item__wrapper",
        "fields": [
            {"name": "category", "selector": ".unibrow span[data-testid='unibrow-text']", "type": "text"},
            {"name": "headline", "selector": ".wide-tease-item__headline", "type": "text"},
            {"name": "summary", "selector": ".wide-tease-item__description", "type": "text"},
            {"name": "time", "selector": "[data-testid='wide-tease-date']", "type": "text"},
            {
                "name": "image",
                "type": "nested",
                "selector": "picture.teasePicture img",
                "fields": [
                    {"name": "src", "type": "attribute", "attribute": "src"},
                    {"name": "alt", "type": "attribute", "attribute": "alt"},
                ],
            },
            {"name": "link", "selector": "a[href]", "type": "attribute", "attribute": "href"},
        ],
    }
    extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)
    async with AsyncWebCrawler(verbose=True, proxy="socks5://127.0.0.1:10808") as crawler:
        result = await crawler.arun(
            url="https://www.nbcnews.com/business",
            extraction_strategy=extraction_strategy,
            cache_mode=CacheMode.BYPASS
        )
        assert result.success, "无法爬取该页面"
        # Soone will be change to result.markdown
        # print(result.markdown_v2.raw_markdown)
        news_teasers = json.loads(result.extracted_content)
        print(f"成功提取了 {len(news_teasers)} 條新聞預告")
        print(json.dumps(news_teasers[0], indent=2))

if __name__ == "__main__":
    asyncio.run(main())