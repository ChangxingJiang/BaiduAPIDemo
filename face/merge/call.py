import json

import requests

import baidu_environment as env
import toolkit


def face_merge_by_free(target_image, target_type, template_image, template_type):
    """
    请求百度云人脸融合API
    文档地址:https://ai.baidu.com/ai-doc/FACE/5k37c1ti0#%E7%9B%AE%E6%A0%87%E5%9B%BE

    :param target_image: <str> 目标图内容
    :param target_type: <str> 目标图类型
    :param template_image: <str> 模板图内容
    :param template_type: <str> 模板图类型
    :return: <str> BASE64格式的融合结果图
    """

    # 生成API的Url(含参数）
    request_url = "https://aip.baidubce.com/rest/2.0/face/v1/merge" + "?access_token=" + env.TOKEN["人脸识别"]

    # 生成API的请求信息
    params = json.dumps({
        "image_template": {  # 模板图
            "image": template_image,
            "image_type": template_type,
            "quality_control": "NONE"
        },
        "image_target": {  # 目标图
            "image": target_image,
            "image_type": target_type,
            "quality_control": "NONE"
        }
    })  # 如果不使用json.dumps直接请求会报222001错误

    # 请求API并返回结果
    response = requests.post(request_url, data=params, headers={"content-type": "application/json"})
    if response.status_code == 200:
        response_json = response.json()
        if response_json["error_code"] == 0:
            return True, response_json["result"]["merge_image"]
        else:
            return False, "人脸融合API请求错误 (Error Code = " + str(response_json["error_code"]) + ")"
    else:
        return False, "人脸融合API请求异常 (Status Code = " + str(response.status_code) + ")"


if __name__ == "__main__":
    demo_target_base64 = toolkit.load_file_in_base64("target.jpg")  # 载入目标图
    demo_template_base64 = toolkit.load_file_in_base64("template.jpg")  # 载入模板图
    merge_base64 = face_merge_by_free(demo_target_base64, "BASE64", demo_template_base64, "BASE64")  # 请求API
    toolkit.save_file_as_base64("merge.png", merge_base64)  # 将结果图存入到文件中
