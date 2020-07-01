# 普通函数
def sum(x, y):
    return x + y


# lambda 函数
p = lambda x, y: x + y
if __name__ == '__main__':
    a = sum(3, 4)
    print(a)
    print(p(1, 2))
x = lambda f,g,k:f*g/k
print(x(3,4,5))
