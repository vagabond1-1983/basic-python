from collections.abc import Callable
import random
from threading import Thread
import time
from typing import Any, Iterable, Mapping


class DownloadThread(Thread):
    def __init__(self, filename):
        self.filename = filename
        super().__init__()

    def run(self) -> None:
        start = time.time()
        print(f"start download {self.filename}")
        time.sleep(random.randint(3, 6))
        end = time.time()
        print(f"download finished and speed {end-start:.3f} secs")


def main():
    threads = [
        DownloadThread("Python从入门到住院.pdf"),
        DownloadThread("MySQL从删库到跑路.avi"),
        DownloadThread("Linux从精通到放弃.mp4"),
    ]

    start = time.time()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    end = time.time()
    print(f"total cost: {end-start:.3f} secs")


if __name__ == "__main__":
    main()
