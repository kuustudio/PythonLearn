# import uuid
# def get_uuid():
#     uid = str(uuid.uuid4())
#     UUID = ''.join(uid.split('-'))
#     return UUID
# if __name__ == '__main__':
#     a = get_uuid()
#     print(a)
def get_config_content(self):
  """
   获取配置内容
  :return:
  """
  dd = ''
  ExportOutDataAddress = 'D:\\SJT\\moddle_docs\\20_工程过程\\30_设计相关\\30_概要设计\\各服务概要设计\\存证服务\\xml模板\\对接智能审判管理平台（办案流程规范化监管）'
  a = ExportOutDataAddress + dd


  try:
    file = open(ExportOutDataAddress, 'r', encoding="UTF-8")
    file_content = file.read()
    # eval  将字典字符串转字典。
    self.dict_config_content = eval(file_content)
  except Exception as e:
    pass
    exit()