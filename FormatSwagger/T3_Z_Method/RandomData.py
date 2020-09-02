import string,random
import math
class RandomData:
    def RandomData(self,NUM):
        A=NUM
        if NUM>=50:
            NUM=50
        CS=math.ceil(A/NUM)
        src_digits = string.digits  # string_数字  '0123456789'
        src_uppercase = string.ascii_uppercase  # string_大写字母 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        src_lowercase = string.ascii_lowercase  # string_小写字母 'abcdefghijklmnopqrstuvwxyz'
        src_special = string.punctuation  # string_特殊字符 '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
        # sample从序列中选择n个随机独立的元素，返回列表
        num = random.sample(src_digits, int(NUM/5))  # 随机取1位数字
        lower = random.sample(src_uppercase, int(NUM/5))  # 随机取1位小写字母
        upper = random.sample(src_lowercase, int(NUM/5))  # 随机取1位大写字母
        special = random.sample(src_special,int(NUM/5))  # 随机取1位大写字母特殊字符
        other = random.sample(string.ascii_letters + string.digits + string.punctuation,int(NUM/5))  # 随机取4位
        # 生成字符串
        pwd_list = num + lower + upper + special + other
        # shuffle将一个序列中的元素随机打乱，打乱字符串
        random.shuffle(pwd_list)
        RandomData = ((((''.join((pwd_list)*CS)).replace(",",".")).replace("|",".")).replace('"',".").replace('"','.'))
        return RandomData
    #随机生成数据 float
    def INTRandomData(self, INT,FLOAT):
        A = INT
        if INT >= 10:
            INT = 10
        CS = math.ceil(A / INT)
        src_digits = string.digits  # string_数字  '0123456789'
        num = random.sample(src_digits, INT )  # 随机取1位数字
        Float = random.sample(src_digits, FLOAT)#
        pwd_list = list(num*2) +["."]+ Float
        RandomData = float(str(''.join(pwd_list)).replace("0","1"))
        return RandomData




