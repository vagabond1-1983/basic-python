from random import randint


def roll_dice(n=2):
    total = 1
    for _ in range(n):
        total += randint(1, 6)
    return total


print(roll_dice())
print(roll_dice(3))
