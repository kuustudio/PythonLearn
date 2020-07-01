from functools import wraps


def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('log开始 ...', func.__name__)
        ret = func(*args, **kwargs)
        print('log结束 ...')
        return ret

    return wrapper


@log
def test1(s):
    print('test1 ..', s)
    return s


@log
def test2(s1, s2):
    print('test2 ..', s1, s2)
    return s1 + s2


test1('a')
test2('a', 'bc')