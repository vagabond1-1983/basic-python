from concurrent.futures import ThreadPoolExecutor
import random
import time


def download(*, filename):
    start = time.time()
    print(f"开始下载 {filename}.")
    time.sleep(random.randint(3, 6))
    print(f"{filename} 下载完成.")
    end = time.time()
    print(f"下载耗时: {end - start:.3f}秒.")


def main():
    with ThreadPoolExecutor(max_workers=4) as pool:
        filenames = [
            "Python从入门到住院.pdf",
            "MySQL从删库到跑路.avi",
            "Linux从精通到放弃.mp4",
        ]
        start = time.time()
        for f in filenames:
            pool.submit(download, filename=f)
    end = time.time()
    print(f"total cost: {end-start:.3f} secs")


if __name__ == "__main__":
    main()
