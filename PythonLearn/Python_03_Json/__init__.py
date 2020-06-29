print("本次学习的例子会结合之前学习的注解\n")
print("方法:dumps：将 obj 转化为json，json.dumps()函数是将字典转化为字符串")
print("skipkeys =true 保证如果dict的key 不是正常的key 则不报 typeerror ")
print("正常情况下 dumps 返回的 字符串编码是 ascii 中的编码集合 如果想使用\n "
      "其他默认字符集 需要加入 ensure_ascii参数并且传参为 False 为否")
print("indent 代表缩进 格式化json str 使用 一般使用 indent = 4 或者2 ")
print("-"*50)
print("方法：json.loads()\n"
      "函数是将json格式数据转换为字典（可以这么理解，json.loads()函数是将字符串转化为字典）")
'''
“”将“obj”序列化为JSON格式的“str”。


如果“skipkeys”为true，则“dict”键不是基本类型

（``str``，``int`，``float`，``bool`，``None`）将被跳过

而不是引发“TypeError”。

正常情况下 dumps 返回的 字符串编码是 ascii 中的编码集合 如果想使用 其他默认字符集 需要加入 ensure_ascii参数
并且传参为 False 为否
如果“确保ascii”为false，则返回值可以包含非ascii

字符，如果它们出现在“obj”中包含的字符串中。否则，所有
fa756068b83047729640bf8a2233dc94 8e8a8f8deacc448dbad8de962cc24674
这些字符在JSON字符串中转义。


如果“check_circular”为false，则循环引用检查

对于容器类型，将跳过循环引用

导致“溢出错误”（或更糟）。


如果“allow_nan”为false，则将为

在中序列化超出范围的“float”值（“nan”、“inf”、“inf”）

严格遵守JSON规范，而不是使用

JavaScript等价物（`NaN``、`Infinity``、`-Infinity``）。


如果“indent”是非负整数，那么JSON数组元素和

对象成员将以该缩进级别很好地打印出来。缩进

级别0将只插入换行符。``没有一个是最紧凑的

代表性。


如果指定了“`separators`”，则它应该是一个``（item_separator，key_separator）``

元组。默认值为`（'，'，'，'：'）``if*indent*为`None``并且

``（'，'，'：'）``否则。要获得最紧凑的JSON表示，

您应该指定'`（'，'，'，'：'）``来消除空白。


``default（obj）``是一个应返回可序列化版本的函数

对象或引发类型错误。默认值只是引发TypeError。


如果*sort_keys*为true（默认值：``False``），则

字典将按键排序。


使用自定义的“JSONEncoder”子类（例如重写

``.default（）``方法来序列化其他类型），使用

使用“cls”kwarg；否则使用“JSONEncoder”。
'''