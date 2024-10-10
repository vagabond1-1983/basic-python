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
    return ''.join(random.choices(ALL_CHARS, k=code_len))


for _ in range(10):
    print(generate_code())
