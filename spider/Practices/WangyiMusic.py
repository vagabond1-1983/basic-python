import requests
import bs4
import os

filename = "music"
if not os.path.exists(filename):
    os.mkdir(filename)

# 热歌榜地址
url = "https://music.163.com/discover/toplist?id=3779629"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Referer": "https://music.163.com/",
}

resp = requests.get(url=url, headers=headers)
# print(resp.text)
soup = bs4.BeautifulSoup(resp.text, "lxml")
song_ids = soup.css.select("div[data-key=song_toplist-3779629] ul li a:nth-of-type(1)")


# 下载前5首歌曲
for song in song_ids[:5]:
    print(f"歌曲原始格式：{song}")
    title = song.contents[0]
    id = song["href"][song["href"].find("id=") : len(song["href"])]
    music_download_url = f"http://music.163.com/song/media/outer/url?{id}.mp3"
    print(f"音乐下载地址：{music_download_url}")
    # mp3 地址有重定向，需要拿到最终的重定向中headers 头部的 location 信息，作为歌曲的下载地址
    resp = requests.get(url=music_download_url, headers=headers)
    reditList = resp.history
    print(f"获取最终重定向的headers头部信息：{reditList[len(reditList) - 1].headers}")
    redirect_url = reditList[len(reditList) - 1].headers["location"]
    print(f"获取重定向最终的url：{redirect_url}")
    # 获取到歌曲的二进制流，输出到文件中保存
    media_content = requests.get(url=redirect_url, headers=headers).content
    with open(filename + os.path.sep + title + ".mp3", mode="wb") as f:
        f.write(media_content)
        print("歌曲下载完成\n============================")
