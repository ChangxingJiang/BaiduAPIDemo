import json

import requests

import environment as env
import toolkit


def face_merge(target_base64, template_base64):
    """
    人脸融合
    文档地址:https://ai.baidu.com/ai-doc/FACE/5k37c1ti0#%E7%9B%AE%E6%A0%87%E5%9B%BE

    :param target_base64: <str> BASE64格式的目标图
    :param template_base64: <str> BASE64格式的模板图
    :return: <str> BASE64格式的结果图
    """

    # 生成API的Url(含参数）
    request_url = "https://aip.baidubce.com/rest/2.0/face/v1/merge" + "?access_token=" + env.ACCESS_TOKEN

    # 生成API的请求信息
    params = json.dumps({
        "image_template": {  # 模板图
            "image": template_base64,
            "image_type": "BASE64",
            "quality_control": "NONE"
        },
        "image_target": {  # 目标图
            "image": target_base64,
            "image_type": "BASE64",
            "quality_control": "NONE"
        }
    })  # 如果不使用json.dumps直接请求会报222001错误

    # 生成API的headers
    headers = {'content-type': 'application/json'}

    # 请求API并返回结果
    if response := requests.post(request_url, data=params, headers=headers):
        response_json = response.json()
        if "result" in response_json and response_json["result"] is not None:
            if "merge_image" in response_json["result"] and response_json["result"]["merge_image"] is not None:
                return response_json["result"]["merge_image"]
            else:
                print("调用人脸融合API失败，未找到merge_image属性:", response_json)
        else:
            print("调用人脸融合API失败，未找到result属性:", response_json)
    else:
        print("调用人脸融合API失败，请求失败")


if __name__ == "__main__":
    target_base64 = toolkit.load_file_in_base64("target.jpg")  # 载入目标图
    template_base64 = toolkit.load_file_in_base64("template.jpg")  # 载入模板图
    merge_base64 = face_merge(target_base64, template_base64)  # 请求API
    toolkit.save_file_as_base64("merge.png", merge_base64)  # 将结果图存入到文件中
