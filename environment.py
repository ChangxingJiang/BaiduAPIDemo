import json

from api_token import get_token

KEY_PATH = r"E:\【微云工作台】\环境配置\百度API环境配置.json"  # 百度API环境配置文件路径

with open(KEY_PATH, "r", encoding="UTF-8") as f:
    setting = json.loads(f.read())

if "API_KEY" in setting:
    API_KEY = setting["API_KEY"]
else:
    API_KEY = None
    print("载入百度API环境配置(API_KEY)失败")

if "SECRET_KEY" in setting:
    SECRET_KEY = setting["SECRET_KEY"]
else:
    SECRET_KEY = None
    print("载入百度API环境配置(SECRET_KEY)失败")

if "ACCESS_TOKEN" in setting:
    ACCESS_TOKEN = setting["ACCESS_TOKEN"]
    print("载入现有的ACCESS TOKEN:", ACCESS_TOKEN)
else:
    if API_KEY and SECRET_KEY:
        ACCESS_TOKEN = get_token(API_KEY, SECRET_KEY)
        print("没有现有的ACCESS TOKEN，重新请求获得:", ACCESS_TOKEN)
