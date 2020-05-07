import sys
import traceback

try:
    num = int(input("请输入一个数字:"))
    print(num)
except ValueError as e:
    exc_type, exc_value, exc_traceback_obj = sys.exc_info()
    traceback.print_tb(exc_traceback_obj)