import json
from urllib import parse

import requests


def get_token(api_key, secret_key):
    """
    【鉴权认证】获取Access Token
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

    if (response := requests.get(url)) == 200:
        if "access_token" in (response_json := response.json()):
            return response_json["access_token"]
        else:
            print("获取Access Token失败，失败返回结果:", response.json())
    else:
        print("获取Access Token失败，错误代码：", response.status_code)
    return None


with open(r"E:\【微云工作台】\环境配置\百度API环境配置.json", "r", encoding="UTF-8") as f:  # 载入百度API环境配置文件
    setting = json.loads(f.read())

KEY = dict()  # AK和SK
TOKEN = dict()  # Access Token

# 载入百度智能云各个产品的鉴权信息
for name, application in setting.items():
    # 载入AK(API Key)
    if "API Key" in application:
        KEY[name]["API_KEY"] = application["API Key"]
    else:
        KEY[name]["API_KEY"] = None
        print("载入百度API环境配置(API Key)失败")

    # 载入SK(Secret Key)
    if "Secret Key" in application:
        KEY[name]["Secret Key"] = application["Secret Key"]
    else:
        KEY[name]["Secret Key"] = None
        print("载入百度API环境配置(Secret Key)失败")

    # 请求获取Access Token
    TOKEN[name] = get_token(KEY[name]["API_KEY"], KEY[name]["Secret Key"])
    print("获取Access Token:", TOKEN[name])
