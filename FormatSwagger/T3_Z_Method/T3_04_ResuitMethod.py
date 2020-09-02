# 这个是python 操作request请求的相关方法
import requests, json


class RequestMethod:
    pass


def send_get_request(url):
    try:
        data_list = requests.get(url)

        if data_list.status_code == 200:
            result = data_list.text
            json_result = json.loads(result)
            return json_result
        else:
            print("请求结果发生错误,状态码是" + data_list.status_code)
    except Exception as e:
        print("请求地址发生错误，请求地址是 [%s]" % url)



def send_str_get_request(url):
    try:
        data_list = requests.get(url)

        if data_list.status_code == 200:
            result = data_list.text
            return result
        else:
            print("请求结果发生错误,状态码是" + data_list.status_code)
    except Exception as e:
        print("请求地址发生错误")
        return e


def send_json_post_request(url, data, header):
    res = requests.post(url=url, data=json.dumps(data), headers=header)
    print(res.text)
    return res.status_code


def send_delete_request(url, data, header):

    resp = requests.delete(url, data=data, headers=header, verify=False)
    print(resp.url)

    print(resp.text)
    return resp.status_code

