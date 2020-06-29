from functools import wraps


def log(arg):
    def _log(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print('log开始 ...', func.__name__, arg)
            ret = func(*args, **kwargs)
            print('log结束 ...')
            return ret

        return wrapper
    return _log


@log('module1')
def test1(s):
    print('test1 ..', s)
    return s


@log('module1')
def test2(s1, s2):
    print('test2 ..', s1, s2)
    return s1 + s2


test1('a')
test2('a', 'bc')
