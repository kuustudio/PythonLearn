from functools import wraps


def log(func):
    @wraps(func)
    def wrapper():
        print('log开始 ...')
        func()
        print('log结束 ...')

    return wrapper


@log
def test1():
    print('test1 ..')


def test2():
    print('test2 ..')


print(test1.__name__)
print(test2.__name__)

