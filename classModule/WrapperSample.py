"""
函数进阶-装饰器
"""

from functools import wraps
import random
import time


def record_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__}执行时间：{end-start:.3f}秒")
        return result

    return wrapper


@record_time
def download(filename):
    print(f"开始下载{filename}.")
    time.sleep(random.randint(2, 6))
    print(f"{filename}下载完成")


@record_time
def upload(filename):
    print(f"开始上传{filename}")
    time.sleep(random.randint(2, 6))
    print(f"{filename}上传完成")


download("xxx.pdf")
upload("xxx.doc")
# 取消装饰器
download.__wrapped__("mysql.pdf")
upload = upload.__wrapped__
upload("python.doc")


# 斐波拉契数
def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


for i in range(1, 21):
    print(fib(i))

"""
装饰器是Python中的特色语法，可以通过装饰器来增强现有的函数，
这是一种非常有用的编程技巧。一些复杂的问题用函数递归调用的方式写起来真的很简单，
但是函数的递归调用一定要注意收敛条件和递归公式，找到递归公式才有机会使用递归调用，
而收敛条件确定了递归什么时候停下来。
函数调用通过内存中的栈空间来保存现场和恢复现场，栈空间通常都很小，
所以递归如果不能迅速收敛，很可能会引发栈溢出错误，从而导致程序的崩溃。
"""
