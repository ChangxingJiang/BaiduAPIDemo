import json

import requests

import baidu_environment as env
import toolkit as tool


def face_detect_by_base64(image_base64):
    """
    人脸监测和属性分析

    :param image_base64: <str> BASE64格式的目标图
    :return: <dict> 百度人脸检测API返回结果
    """
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"

    params = json.dumps({
        "image": image_base64,
        "image_type": "BASE64",
        "face_field": "age,beauty,expression,face_shape,gender,glasses,landmark,landmark150,race,quality,eye_status,emotion,face_type,mask,spoofing"
    })

    request_url = request_url + "?access_token=" + env.TOKEN["人脸识别"]
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=params, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None


if __name__ == "__main__":
    demo_base64 = tool.load_file_in_base64("demo2.jpg")  # 载入目标图
    detect_result = face_detect_by_base64(demo_base64)  # 请求API
    print(detect_result)
