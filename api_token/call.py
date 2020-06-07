from urllib import parse

import requests


def get_token(api_key, secret_key):
    """
    鉴权认证机制:获取Access Token
    文档地址:https://ai.baidu.com/ai-doc/REFERENCE/Ck3dwjhhu

    :param api_key: <str> 应用的API Key
    :param secret_key: <str> 应用的Secret Key
    :return: <str> Access Token
    """

    params = {
        "grant_type": "client_credentials",
        "client_id": api_key,  # 官网获得的API Key
        "client_secret": secret_key  # 官网获得的Secret Key
    }

    url = "https://aip.baidubce.com/oauth/2.0/token?" + parse.urlencode(params)  # 生成API请求的Url

    if response := requests.get(url):
        if "access_token" in (response_json := response.json()):
            return response_json["access_token"]
        else:
            print("获取Access Token失败，失败原因:", response.json())
    else:
        print("获取Access Token失败，失败原因:", "请求失败")
    return None


if __name__ == "__main__":
    pass
