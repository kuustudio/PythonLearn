import random
# import json
# a = {"bizId":"2050","bizVersion":1605684344353,"body":{"ajbh":"6a2561e9165d485b9afeff4e4998b3e3","ajlb":"0301","dsr":[{"ajbh":"6a2561e9165d485b9afeff4e4998b3e3","bh":"801e34ef11db466c888b34dcdd287b25","bhSscyr":"801e34ef11db466c888b34dcdd287b25","cjsj":1605684313187,"csrq":810144000000,"dwxz":"22","dwxzTranslateText":"有限责任公司","dwzt":"1","hjszd":"斯洛伐克","jbfy":"2050","jbfyTranslateText":"河南省高级人民法院","js":["1"],"jsTranslateText":[""],"lx":"1","lxTranslateText":"自然人","mc":"哈姆西克","ssdw":["2"],"xb":"1","ywlx":"0301","ywlxTranslateText":"民事一审","zhxgrTranslateText":"","zjhm":"21234567890","zjlxTranslateText":"","zzlxTranslateText":""}],"jbfy":"2050","bgqdsr":[]},"mqKeys":"6a2561e9165d485b9afeff4e4998b3e3","tag":"bg-dsrxx","timestamp":1605684344353,"version":0}
# b = {}
# for  i  in a["body"].keys():
#     b.update({i:a["body"][i]})
# result = json.dumps(b, ensure_ascii=False, indent=4, skipkeys=True, sort_keys=True,
#                     separators=(",", ":"))
# print(result)
# a = []
# for i in range(1,100):
#     b = '${c_bh_'+ str(i) + "}"
#     d = random.choice(range(1,4))
#     c = {
#         "bhAj":b,
#         "jbfy":"${jbfy}",
#         "pczt":str(d)
#     }
#     a.append(c)
# print(a)
import json
a = "{\n \"20100\":\"10102218\",\n \"20200\":\"10102301\",\n \"20501\":\"10102218\",\n \"20304\":\"10102501\",\n \"20601\":\"10102092\",\n \"20602\":\"10102092\",\n \"20603\":\"10102092\",\n }"

b = str(a).replace("\n","")
c = json.loads(b)
print(c)