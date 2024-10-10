"""
案例1：设计一个生成验证码的函数。
说明：验证码由数字和英文大小写字母构成，长度可以用参数指定。
http://jenkins-developer.glodon.com/job/GEPM/job/auto-test/job/API-auto-parent/
"""

import random
import string

ALL_CHARS = string.digits + string.ascii_letters


def generate_code(code_len=4):
    """生成指定长度的验证码

    :param code_len: 验证码的长度(默认4个字符)
    :return: 由大小写英文字母和数字构成的随机验证码字符串
    """
    return "".join(random.choices(ALL_CHARS, k=code_len))


for _ in range(10):
    print(generate_code())

print("----关键字参数----")
print(
    "关键字参数会将传入的带参数名的参数组装成一个字典，参数名就是字典中键值对的键，而参数值就是字典中键值对的值"
)


def calc(*args, **kwargs):
    result = 0
    for arg in args:
        if type(arg) in (int, float):
            result += arg
    for value in kwargs.values():
        if type(value) in (int, float):
            result += value
    return result


print(calc(1, 2, 3))
print(calc(1, 2, a=3, b=4))

print("----高阶函数应用----")
import operator


def calc(*args, init_value, op, **kwargs):
    result = init_value
    for arg in args:
        if type(arg) in (int, float):
            result = op(result, arg)
    for value in kwargs.values():
        if type(value) in (int, float):
            result = op(result, value)
    return result


print(calc(1, 2, 3, init_value=0, op=operator.add, x=4, y=5))  # 1+2+3+4+5=15
print(calc(1, 2, 3, init_value=1, op=operator.mul, x=4, y=5))  # 1*2*3*4*5=120

print("---lambda---")
numbers1 = [35, 12, 8, 99, 60, 52]
numbers2 = list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, numbers1)))
print(numbers2)

"""
简单的总结
Python中的函数可以使用可变参数*args和关键字参数**kwargs来接收任意数量的参数，
而且传入参数时可以带上参数名也可以没有参数名，可变参数会被处理成一个元组，
而关键字参数会被处理成一个字典。
Python中的函数是一等函数，可以赋值给变量，也可以作为函数的参数和返回值，
这也就意味着我们可以在Python中使用高阶函数。如果我们要定义的函数非常简单，
只有一行代码且不需要函数名，可以使用Lambda函数（匿名函数）。
"""
