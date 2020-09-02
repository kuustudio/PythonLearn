# import re
# a = '移送事项实体类型-（1-当事人管辖异议，2-管辖权争议协商，3-延长审限，4-附加诉讼审查反诉，5-云调解）'
# print(re.split('-| |\t',a))
import time
import uuid
import json
from T3_Z_Method import T3_04_ResuitMethod
import time
from datetime import datetime, date, timedelta

# data = {}
# data['bhAj'] = 'fb039c4d67e341c68bc0e768cfb89999'
# data["fzsl"] = 200
# data['jbfy'] = "2400"
# data['ahlb'] = []
# num = 201
# res_list = []
# ajbh_list = []
#
#
# def dict_to_str(dict_data) -> str:
#     jsondata = json.dumps(dict_data, skipkeys=True, ensure_ascii=False, check_circular=True,
#                           indent=2, sort_keys=True,
#                           separators=(",", ":"))
#     return jsondata
#
#
# def get_uuid():
#     uuid_str4 = str(uuid.uuid4())
#     uuid_str4_4 = str(uuid.uuid4()).replace("-", "")
#     return uuid_str4_4
#
#
# for i in range(1, num):
#     result = {}
#     result['ah'] = "000" + str(i) + "民事案件"
#     ajbh = get_uuid()
#     ajbs = get_uuid()
#     result['ajbh'] = ajbh
#     result['ajbs'] = ajbs
#     result['nh'] = 2020
#     result['phh'] = i
#     ajbh_list.append(ajbh)
#     data['ahlb'].append(result)
# jsondata = dict_to_str(data)
# print(jsondata)
# print('---------------------------------------------------------------------------------------------------------------')
# print(ajbh_list)
# post_url = 'http://172.18.4.211:30127/api/v1/xzaj/actions/fu_zhi'
# post_header = {'Content-Type': 'application/json'}
# print(type(post_header))
# b = T3_04_ResuitMethod.send_json_post_request(post_url, data, post_header)
# if b == 200:
#     time.sleep(600)
#     for j in ajbh_list:
#         url = 'http://172.18.4.211:30127/api/v1/xzaj?bhAj=' + j + '&jbfy=2400&limit=10&offset=0'
#         a = T3_04_ResuitMethod.send_get_request(url)
#         dsr = a[0]['dsrvo']
#         print(dsr)
#         if dsr:
#             if dsr[0]['bhAj'] == j:
#                 pass
#         else:
#             print(j + '复制当事人存在问题')
#             print(a[0]['xlazMc'])
#             res_list.append(j)
#
# time.sleep(3)
# post_header = {'Content-Type': 'application/json'}
# ajbh_list = ['954255a32e914032b5d6abb2a3e25b98', '35c903ae82f44f2fa03bb417abb6fe6e', 'accba44c91a44578a00f38df54827bc3', '2e243f41b2074851a51ebe2cc46f0d64', 'bdb6a80100504b80a2abdfb8a01f8d17', '36c5135c473446f383e756f0ffe77e8f', 'f0ea9b52b7a646fcb977e5ebff950cf3', 'dd517441b023474e98887dd5a6fff794', '7a3dca88201f4069982c3d6a29089fb8', '2621182366de4376986d0c93ddd4d0ae', 'fc23c144bc104079bc7efb2a35f467c4', '0c75a515302b4f79bb9bdba93515eb51', '359dd5fea6d144ad9d5a7844c9c18cb8', 'd0d0c76368f14e3a962ceced5f13fddc', 'f14262118e714ea0812c1da4a29eb509', '6bfaa905edeb488ba330ba658da236de', '7322bd40f1ed4166bd55e9641a1d672a', '8a139d4f5bf14db2a11c3f8147a272f1', '7f9d167c0bc949a09b18621c3ecaec5d', '928727c9ec0549adaace0f2fbdc9f574', '7869957e425d43d796e6aca344de87e2', '2fd0784db3bb42cbafdb411b3447ff8c', '4bcdda5835224a1e968f35f3b9370855', 'c31a8ecdce9c48b798c43e64fe184911', '5233ae9f0b034849a2977de2f2b0f836', '519147db4e4b4cc7881eb24ac4fca158', '5f4edd33101f4118bbc5b8be14d2f965', 'a3d6bd96635f4f6b9b7a02e381c49a73', '931874bef03b4e3b806e7137aecb7980', '110b3aeaf24f47c4914d9a007f716677', '7292333ae9db451e99f080d003810a90', 'b9e7c69d697443e2951fbb6737195967', '3938adafd1dd4852ab35425a2e8fc1e5', '3392ed70e4ee40aea7753ae53527ce85', '83122de251674991ac5b507ee97535c7', '7c00f70d45e24832bb824d04eea461b6', '6c364f26264e4161b8952d318cbe2400', '109fab8d14e2465e9c548c305bc09c21', '76f38f0ff3a849ea9dff3aaddf6b4ed7', '1374fa1dc787491a9590d275e406907c', '3138a0e3d47243c295b2d3b7d149ece6', '95c14d0bd4144a9c9804be442550cc66', '46ab09b7f7054e10a9c4b6019c8f563c', '517cbc0be11745c0bc110bf9b602c8fc', '871a4a76d251489c98b475655cca59dc', '07e07d21af00470387f8250d41c796b6', 'de3cbeaf15704b589c66255b577f0c11', 'de04b7bc75154cc6a8af244a56d84c3d', '87bd704ca6b9425ba801c53bb01da241', '11f44c46ba5e452baccfabfd56069a8a', '1ee4209cf0404664bee2820cda177476', '82d3ccdde7b141a8b8765340795673ec', '45053b5d35384951bdcddbf34ae32e81', '5b19b20f6bce437a8a0872e43e063852', '36197c795c0248aead97b3d303455324', '544537e12d084345a8a7d06daa1390ef', 'dfe8f43f1ad845be82459b22b51e45a2', '7f87a375342d4342bce29c2b9a73860c', 'bca9542b86ff4876a7b7f8898a4d956c', '10e5d207475146568091fcd7eedd8287', '88847bf417a3408b955f5bcfd6a70313', '03078e4259624b5ab78e64cab408eb4a', '5f359cfea7de4fbc92202046b2e34810', '2ed5a34e58754f6d8868b54a66b40c1c', 'f6959168923a4c3f835c4fc0ec9dd9b5', 'c8742a0a6c014eb9a416f1605f167870', 'e4fbbf0f874a4692b04f4ad351d7477f', 'c7a3078e880944f7a01ea35ff4ce2b7b', '6c749a6cd8fe4675ac7289efeed21339', '34dbf23eb53b475f90a080b47a9fd761', '06a22bb0c02e47c295a9937b35376ab2', '60ef68d690ae4ae68de2f178475cda26', '34738ed559714455b07b785ef046f77d', 'abb5fc11d6c9440fbf26b51bd6ad2f07', 'd9e38ea7a52340688e032faf795475ae', 'a3cc900b009b46edba1fa99f17d3968c', 'cc9de894138d40d784d5d08988a7c4d0', 'c973b458f21c4777b0f61229a255b87a', '03a39a8875eb4a58a91fc4dca21620e4', 'c9b15e65fdca42889040e6b99bcbdf71', 'e04510b7bf4b4dc2816dbd53a7235e3a', 'e889f451c9574ed9979ebd345c58b25c', '3d4bc613b56a47608b0648a14449d655', '0fd0875c3c6f4271b2ba07b1c042eede', '6ef0cf1e96954055a2b37c5cba8275eb', 'c3018c3d52724a8dbe0408b4c5b0aaa4', '3645ca4ee98c4128b9c3b2475a6c246f', '982f015bda7e4becb13584bc75251b2a', '95615b453c72414e83c1718dc8ceb319', 'beaa78d6760f484b81fa63def05101a2', '9e5d27aa08b84eaebbf995ed57aa036a', 'abcd94d917fe49c59c338dee3b04f359', '4fb52088e92844c0b4f9a7e208799d06', 'e36396ab90d14d329e34182f146a44c5', '5ada3c26eb044b6a925c5832c76671bc', 'd35619bcb92c41d7b35771ace855ef81', '42b0b805d71c43b5bc8663fa742b29e1', '2eef1bf7e84d42ee83d2a65013d712d4', 'f438b682b4c04e89a72d0aaae77180b4', '020929a674e64a898747cc39f796ec30', '8db21aa741724134974076eb8afed347', '1bbf929284aa4da89c018c963b7c6b7a', '3eed0586ca0546ebb7ebc5d06456b343', 'fd1e7c2dc492412f81f1b2354824d266', '8aab75dc101245c38e13d6ceb4f15f9a', '7e9a180bd10448cdb99b8617920e4af1', 'e121d19d8be8429c95ff4c9e07132cd7', 'a991975c6b254226b7bfef4c7cbf8c15', '6f00ddd33c784edcabf1fbbdf6c99451', '369f813731cb4e1ca45667bcdeda2642', 'cee2a727450d46ea9f1614ad88597e0f', 'fd5a2b3a7d6f4ce7812a33cdcbe28288', '68298bcba7f74cddaea226a16f8b48fe', '23251342f3c04a4faf335a080eab1c57', '25504f985c4443a38585832ea26270e4', '6f5d0ad60d924708a1cbc0b42bfce094', 'f9b7be97b50b48e39cb367c79c08943b', 'd1427cb7bd3647de9a373c3e65109aa3', '32b2cabff06d4b859f1bf014e6bebd7b', '266f123dd3494ebda544b14ae10b0591', '43b5cd77a7a24ead87d514de8a1f9e48', '306e66cb2d9f42fd816ddae927c3d812', 'c3f90d1aee1e43799eff02d365173dfd', 'e4a733cf40b04f45b479374348c14600', '995482c143bb469399190654cf31a5ae', 'b0611b2a68474816acf43f1096470079', '474e709bb8fd47bc92a9ac38510fe3e9', '47c7e1b4e61047dba5470ab19eb9e5a3', 'e7d675c53539444990afb9759fbb58ff', '429dabfbcdc644a3977a5f38eef3c14c', '881551b0775e40c287578032418e72ab', 'fb329a5a9283433d83d06784d5b83f39', 'c4c1454a84554c04b0258b3711a548f4', 'a7317d3ab30c4eb488da243c0c7ef7a4', '92b24bb28dc04e9cbe78695f305f7a1a', 'ffc711144b5a46d180ee762ac735f32e', '4b96094a845b42ccb81dea1f9dff7b22', '928fc294d2f84961818960f2415f817f', 'e78f49a7a98e451e94020642e2de95b3', '7131507fe3b74bc9aa210c4f59764404', 'ea3fb5936c2843c59612eb5d270e6cb1', '9d0f780d548a470cbcc1483f1ef531e3', '54cb98ab9d8f46738cc227522014ef44', 'c37d3ac5dba04510911e411f440e1c35', '93d96097b3dc46eeb62712ec6f23d3d5', 'bf35712b51334e9d865a753d36270b5d', '4ef0d70a735e4ad3bcc7f70bd5cb2477', '1cd50156401143f6a4e0f7945730cab8', 'ba12132eb87945cea637170789e2a901', '21f9f42ab5ea49ad94026c9c4ecc735b', 'f66d8c38097f45289251bf4d5892c586', '109103ca13634cf4bc6c164ccaadb3ca', '63afc7960a8f4208b7df1c96efc0ca1f', '53fb385ab5254db8a4513a60c7b1e89b', 'd8950c5fd2054fac9d817ff08e59ad92', 'c0b48b20424a44f8b5f2ecd2b3b813cf', 'e7955b9629de4f9582acaf62d4a753da', '03e8f03a96544d09aaa9e42905a1fa4d', 'ea6ded8703654c32baf98675930c430a', '8f42834dcb624435b7245e5f8757033e', '643887f452454eeb86229331e2c08644', '8ef183f806a0403ba58242baf7c08233', 'a5ccd6c5883d4aa9820b0ad03a6514f4', '24c3ea9250a74c6abbab3c4e8619cff5', 'fa6e62a309fb45d3adf653fba3e58282', 'b7b0e81493b04942b09ad861c170ede3', 'e41eface310a41fdb3a548175ce4933c', '087e453b6a2349ce8e2f0f5e8832dd18', 'a7d688e5741e46bba4af1c0b14278218', '08c7353a56254bd4b9fffb2dd13d44c9', '4bc8311f13c0499589db0ce12ccbc27b', 'd8b75528b6b34998986635cf2f07827d', '8d3918a26a7046cc80b0fd7978b98840', '3725a9ef6f714765be59a04bce83892f', '0e2682c6dcea4abea2eba5b8088e638f', '15a1091e3b024a3bb5ff5614d6d41985', '45c45c7ea4254f1b9dc0a1e3a39235aa', '71eba4232877400ba841da9aae5328c8', '089258891901413dab3b355d48c5798d', '0eb43f4177034040aaaf5c5df6f89eb3', '747c19100c234ad2b573f940fff3d592', '830685da3cf74be094791fa98e0d6229', '0536a92abee840e8ad01078618c6d640', '51591bf75e8f4792b09b378a2df76b55', '41a3ac56b075439ea42d0e113856c478', '886ab5e8a2d14f21b4f32fd03df9dbd2', '7b9a5d64d9ae423ba1c7c116414aaffe', '8146e24e7afc4c92908acd7584ece9f2', '8c1003e7137e4a96a84913a51006cbbd', '3c5895a70a69440cb51c4cddc4c5607c', '85fb660deea2415e82a06657e4fe4d2d', '80cc8f2808274025a0aa782f72a75124', '8bb4e2f6a6d046f1aee6be49fb1b1e90', 'e4a219a85777435287770517c0d576b2', 'ab1818fd37ea46f893025724b66bc58b', '96314567a82a41dd85b995113afdba9f', '6cd5648443334e059750e84652d44914', 'd8344ee379864266afe9e6245775f443', 'd92cdcc8016746fcbec8789b043e9f3a', 'ec18ac1fdce8485ca14646eae60728c4']
#
# for x in ajbh_list:
#     delete_url = 'http://172.18.4.211:30127/api/v1/xzaj/' +x+'?jbfy=2400'
#     data_delete = {'jbfy':'2400'}
#     c = T3_04_ResuitMethod.send_delete_request(delete_url,data_delete,post_header)
#     if c == 200:
#         print('测试案件删除')
#   -------------------------------------------------------------------------------------------------------------------
# str_location = '2020-07-16 10:52:04'
# timeArray = time.strptime(str_location, "%Y-%m-%d %H:%M:%S")
# location = int(time.mktime(timeArray))
# test = location - 12000
# location_time = int(location) * 1000
# test_time = int(test) * 1000
# ajlb = '0200'
# url = 'http://172.18.4.211:30121/api/v1/glajzl?ajlb=' + ajlb + '&jsrq=' + str(location_time) + '&ksrq=' + str(
#     test_time) + '&limit=10&offset=0'
# a = T3_04_ResuitMethod.send_get_request(url)
# print(url)
# print(a)


a = {'api': '/api/v1/ajtz/{ajbh}', 'method': 'delete', 'require_list': ['ajbh', 'jbfy', 'tz', 'ywlx'], 'api_name': '取消追加案件特征'}
b = str(a['DTO/VO']).split("'")[0]
print(b)