import json

with open(r"E:\【微云工作台】\环境配置\腾讯云环境配置.json", "r", encoding="UTF-8") as f:  # 载入腾讯云API环境配置文件
    setting = json.loads(f.read())

if "COS" in setting:
    COS = setting["COS"]
else:
    COS = None
    print("载入腾讯云对象存储(COS)环境配置失败")
