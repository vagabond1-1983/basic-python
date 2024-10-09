# This is a sample Python script.

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    current_date = datetime.now()
    print(f'Today is: {str(current_date)}')
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.
    print('Today is: {}, Hello {}'.format(str(current_date), name))

    # print yesterday
    yesterday = current_date - timedelta(days=1)
    print('Yesterday is: {}'.format(str(yesterday)))
    
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    name = input('Please input your name:')
    print_hi(name)

    load_dotenv()
    password = os.getenv('PASSWORD')
    print(password)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/