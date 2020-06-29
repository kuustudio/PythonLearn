# import json
# json_data ={
# 	 "ah": "${ah1}",
# 	  "bglajAh": "${ah3}",
# 	  "bglajGxdm": "${bglajGxdm_zs}",
# 	  "bglajJbfy": "${jbfy}",
# 	  "bglajLarq": "${larq_ajbh8}",
# 	  "bglajYwlx": "${ywlx_baaj_zssc}",
# 	  "bglajbh": "${ajbh3}",
# 	  "gxdm": "${bagxdm}",
# 	  "jbfy": "${jbfy}",
# 	  "larq": "${larq_ajbh10}",
# 	  "ywlx": "${ywlx_baaj_zs}",
# 	  "bglajAy": "${bglajay_ms}"
# 	}
# a = json_data.keys()
# b=[
#     'xah', 'ah', 'bglajGxdm', 'jbfy', 'larq', 'ywlx', 'bh', 'gxdm', 'xjbfy', 'xlarq', 'xywlx', 'ay'
# ]
# c = {}
# for i  in list (a):
#     n = list(a).index(i)
#     j = json_data[i]
#     m = b[n]
#     c[m] = j
# data = json.dumps(c, indent=4)
# print(data)
a = [1,2,3,4,5,6]
a.remove(2)
print(a)

