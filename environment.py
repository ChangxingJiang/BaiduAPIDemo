import json
from urllib import parse

import requests

KEY_PATH = r"E:\【微云工作台】\环境配置\百度API环境配置.json"  # 百度API环境配置文件路径


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

    print(params)

    url = "https://aip.baidubce.com/oauth/2.0/token?" + parse.urlencode(params)  # 生成API请求的Url

    if response := requests.get(url):
        if "access_token" in (response_json := response.json()):
            return response_json["access_token"]
        else:
            print("获取Access Token失败，失败原因:", response.json())
    else:
        print("获取Access Token失败，失败原因:", "请求失败")
    return None


with open(KEY_PATH, "r", encoding="UTF-8") as f:
    setting = json.loads(f.read())

API_KEY = dict()
SECRET_KEY = dict()
ACCESS_TOKEN = dict()

for name, application in setting.items():
    if "API Key" in application:
        API_KEY[name] = application["API Key"]
    else:
        API_KEY[name] = None
        print("载入百度API环境配置(API Key)失败")

    if "Secret Key" in application:
        SECRET_KEY[name] = application["Secret Key"]
    else:
        SECRET_KEY[name] = None
        print("载入百度API环境配置(Secret Key)失败")

    if "Access Token" in application:
        ACCESS_TOKEN[name] = application["Access Token"]
        print("载入现有的Access Token:", ACCESS_TOKEN[name])
    else:
        if API_KEY[name] and SECRET_KEY[name]:
            ACCESS_TOKEN[name] = get_token(API_KEY[name], SECRET_KEY[name])
            print("没有现有的Access Token，重新请求获得:", ACCESS_TOKEN[name])
