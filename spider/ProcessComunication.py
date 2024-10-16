import time
from multiprocessing import Process, Queue

"""
多线程-2
对于Python开发者来说，以下情况需要考虑使用多线程：

程序需要维护许多共享的状态（尤其是可变状态），Python 中的列表、字典、集合都是线程安全的（多个线程同时操作同一个列表、字典或集合，不会引发错误和数据问题），所以使用线程而不是进程维护共享状态的代价相对较小。
程序会花费大量时间在 I/O 操作上，没有太多并行计算的需求且不需占用太多的内存。
那么在遇到下列情况时，应该考虑使用多进程：

程序执行计算密集型任务（如：音视频编解码、数据压缩、科学计算等）。
程序的输入可以并行的分成块，并且可以将运算结果合并。
程序在内存使用方面没有任何限制且不强依赖于 I/O 操作（如读写文件、套接字等）。
"""


def sub_task(content, queue):
    counter = queue.get()
    while counter < 50:
        counter += 1
        queue.put(counter)
        print(f"{content}-{counter}", end="", flush=True)
        time.sleep(0.01)
        counter = queue.get()


def main():
    queue = Queue()
    queue.put(0)
    p1 = Process(target=sub_task, args=("Ping", queue))
    p1.start()
    p2 = Process(target=sub_task, args=("Pong", queue))
    p2.start()
    while p1.is_alive() and p2.is_alive():
        pass
    queue.put(50)


if __name__ == "__main__":
    main()
