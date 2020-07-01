def log(func):
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
# 可见test1的函数名称变了，如果某些代码用到就会出问题，可以使用functools模块提供的修改函数属性的方法wraps