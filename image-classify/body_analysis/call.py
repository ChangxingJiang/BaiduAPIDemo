import requests

import baidu_environment as env
import toolkit as tool


def body_analysis(demo_base64):
    """
    人脸监测和属性分析
    :param demo_base64: <str> BASE64格式的目标图
    :return:
    """
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_analysis"

    params = {"image": demo_base64}

    request_url = request_url + "?access_token=" + env.TOKEN["人体识别"]
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        return response.json()


if __name__ == "__main__":
    demo_base64 = tool.load_file_in_base64("demo_1.jpg")  # 载入目标图
    detect_result = body_analysis(demo_base64)  # 请求API
    print(detect_result)
