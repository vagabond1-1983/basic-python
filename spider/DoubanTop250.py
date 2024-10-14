import bs4
import requests

rank = 0
for page in range(1, 11):
    resp = requests.get(
        url=f"https://movie.douban.com/top250?start={(page-1)*25}",
        headers={"User-Agent": "BaiduSpider"},
    )
    # 创建BeautifulSoup对象
    soup = bs4.BeautifulSoup(resp.text, "lxml")
    # 通过CSS选择器从页面中提取包含电影标题的span标签
    title_spans = soup.select("div.info > div.hd > a > span:nth-child(1)")
    # 通过CSS选择器从页面中提取包含电影评分的span标签
    rank_spans = soup.select("div.info > div.bd > div.star > span.rating_num")

    for title_span, rank_span in zip(title_spans, rank_spans):
        rank = rank + 1
        print(f"{rank}.{title_span.text}的评分：{rank_span.text}")
