import random

def guess(answer: int) -> int:
    """
    Return the counter of guess
    """
    counter = 0
    while True:
        counter += 1
        number = int(input('请输入一个 1-100的数字:'))
        if number > answer:
            print('大了点')
        elif number < answer:
            print('小了点')
        else:
            print('回答正确')
            break
    return counter

answer = random.randint(1, 100)
COUNTER = guess(answer=answer)
print(f'正确答案是：{answer}，您猜了{COUNTER}次')
