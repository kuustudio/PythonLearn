import requests
headers = ''
url = "http://172.18.15.163:30121/api/v1/wbglaj?ahLike=%E6%B9%98%E6%B0%91%E5%88%9D&jbfy=2400"
data = {'ywlx':'',
        'jbfy':'2400'}
res =  requests.get(url=url, data=None).json()
for i in res:
    if i['jbfy'] != '2400':
        print('%s 的jbfy有问题为[%s]'%(i['bh'],i['jbfy']))
    # if i['ywlx'] != '0301':
    #     print('%s 的ywlx有问题为[%s]' % (i['bh'], i['ywlx']))
    if '湘民初' not in i['ah']:
        print(i['bh'])
print('-'*70)

