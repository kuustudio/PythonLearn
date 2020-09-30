import json
a = {
    "bh": "{{bh1}}",
    "bhAj": "{{bhAj}}",
    "dwscsqr": "{{bh1}}",
    "jbfy": "{{jbfy}}",
    "lhgxr": "{{bh}}",
    "tzrq": 1568217600000,
    "ywlx": "{{ywlx}}",
    "yyms": "修改异议描述",
    "yyrq": 1568217600000
}
b = json.dumps(a,indent=2,allow_nan=True,ensure_ascii=False)
print(b)