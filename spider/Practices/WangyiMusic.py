import requests
import bs4


# 热歌榜地址
url = "https://music.163.com/discover/toplist?id=3779629"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Referer": "https://music.163.com/",
}

resp = requests.get(url=url, headers=headers)
print(resp)
soup = bs4.BeautifulSoup(resp.text, "lxml")
song_ids = soup.select("div > table")
print(song_ids)
