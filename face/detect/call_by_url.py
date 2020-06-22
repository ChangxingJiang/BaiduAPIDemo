import json

import requests

import baidu_environment as env
import toolkit as tool


def face_detect_url(demo_url):
    """
    人脸监测和属性分析
    :param demo_base64: <str> BASE64格式的目标图
    :return:
    """
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"

    params = json.dumps({
        "image": demo_url,
        "image_type": "URL",
        # "face_field": "age,beauty,expression,face_shape,gender,glasses,landmark,landmark150,race,quality,eye_status,emotion,face_type,mask,spoofing"
        "face_field": "quality"
    })

    request_url = request_url + "?access_token=" + env.TOKEN["人脸识别"]
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        return response.json()


def face_detect_base64(demo_base64):
    """
    人脸监测和属性分析
    :param demo_base64: <str> BASE64格式的目标图
    :return:
    """
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"

    params = json.dumps({
        "image": demo_base64,
        "image_type": "BASE64",
        # "face_field": "age,beauty,expression,face_shape,gender,glasses,landmark,landmark150,race,quality,eye_status,emotion,face_type,mask,spoofing"
        "face_field": "quality"
    })

    request_url = request_url + "?access_token=" + env.TOKEN["人脸识别"]
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        return response.json()


if __name__ == "__main__":
    image_base64 = tool.load_file_in_base64("demo2.jpg")
    detect_result = face_detect_base64(image_base64)
    print(detect_result)
