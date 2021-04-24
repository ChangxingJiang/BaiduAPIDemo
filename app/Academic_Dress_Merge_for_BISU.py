"""
毕业照图片生成
for 北二外·本科生
"""

import base64
import copy
import os
import re
from io import BytesIO

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from face.merge.call import face_merge_by_free

ACADEMY_TYPE = {
    "英语学院": "文科",
    "亚洲学院": "文科",
    "文化与传播学院": "文科",
    "日语学院": "文科",
    "欧洲学院": "文科",
    "高级翻译学院": "文科",
    "中东学院": "文科",
    "商学院": "理科",
    "旅游科学学院": "理科",
    "经济学院": "理科",
    "政党外交学院": "文科",
    "汉语学院": "文科",
    "马克思主义学院": "文科",
    "MTA/MBA教育中心": "理科"
}  # 学院学位对应表(文科粉色|理科灰色)


def load_students_info(path):
    """
    载入学生信息表

    :param path: <str> 学生信息表地址路径
    :return: <dict> 以学生身份证号为Key的学生信息表; <dict> 以学生学号为Key的学生信息表
    """
    # 读取学生信息表
    with open(path, 'rb') as f:
        file_content = f.read().decode("UTF-8", errors="ignore")
    file_content = file_content.replace("\r", "")

    # 解析学生信息表
    students_info_by_id = {}  # 以学生身份证号为Key的学生信息表
    students_info_by_number = {}  # 以学生学号为Key的学生信息表

    for file_line in file_content.split("\n")[1:]:
        if file_line == "":
            continue

        file_line_items = file_line.split(",")

        student_info = {
            "number": file_line_items[0],  # 学号
            "name": file_line_items[1],  # 姓名
            "gender": file_line_items[2],  # 性别
            "id": file_line_items[3],  # 身份证号
            "level": file_line_items[4],  # 学位等级：本科/硕士
            "academy": file_line_items[5],  # 学院
            "type": ACADEMY_TYPE[file_line_items[5]]  # 学位类型：文科/理科
        }

        students_info_by_id[file_line_items[3]] = student_info
        students_info_by_number[file_line_items[0]] = student_info

    return students_info_by_id, students_info_by_number


def load_template_image(path):
    """
    载入模板图列表

    :param path: <str> 学生信息表地址路径
    :return: <dict> 以文件名为键，PIL.Image图片对象为值的字典
    """
    template_image_dict = {}
    for file_name in os.listdir(path):
        file_obj = Image.open(path + "\\" + file_name)
        file_name = re.sub(r"\.(jpe?g|png)$", "", file_name)
        template_image_dict[file_name] = file_obj
    return template_image_dict


def face_merge(template_image, target_image):
    """
    人脸融合

    :param template_image: <PIL.Image> 模板图
    :param target_image: <PIL.Image> 目标图
    :return: <PIL.Image> 融合结果图
    """
    # 检查模板图尺寸是否正常
    if template_image.width < 2400 * 0.995 or template_image.height < 3600 * 0.995:
        print("模板图尺寸异常！")
        return None

    # 切割模板图，生成子模板图
    template_part_image = template_image.crop((1200, 1000, 2000, 2000))

    # 将子模板图转换为base64格式
    buffer = BytesIO()
    template_part_image.save(buffer, "png")
    template_part_base64 = str(base64.b64encode(buffer.getvalue()), encoding="utf-8")

    # 将目标图转换为base64格式
    buffer = BytesIO()
    target_image.save(buffer, "png")
    target_base64 = str(base64.b64encode(buffer.getvalue()), encoding="utf-8")

    # 执行人脸融合
    merge_code, merge_result = face_merge_by_free(target_image=target_base64, target_type="BASE64",
                                                  template_image=template_part_base64, template_type="BASE64")
    if merge_code:
        merge_part_image = Image.open(BytesIO(base64.b64decode(merge_result)))
    else:
        print(merge_result)
        return None

    # 将人脸融合结果图粘贴到模板图中
    merge_image = copy.deepcopy(template_image)
    merge_image.paste(merge_part_image, (1200, 1000, 1200 + merge_part_image.width, 1000 + merge_part_image.height))
    return merge_image


def draw_frame(base_image, merge_image, font, number, name, academy):
    """
    绘制底板图内容

    :param base_image: <PIL.Image> 底板图
    :param merge_image: <PIL.Image> 完成人脸融合图
    :param font: <PIL.ImageFont> 底板图填写文字的字体
    :param number: <str> 学生学号
    :param name: <str> 学生姓名
    :param academy: <str> 学生所在学院
    :return: <PIL.Image> 绘制完成图
    """
    # 粘贴融合图到底板图上
    merge_image = merge_image.resize((1038, 1558), Image.ANTIALIAS)  # 调整融合图尺寸
    result_image = copy.deepcopy(base_image)
    result_image.paste(merge_image, (81, 50, 81 + 1038, 50 + 1558))  # 粘贴融合图到底板图上

    # 生成需要写入的文字
    text_1 = academy  # 第一行的文字
    text_2 = name + "　" + number  # 第二行的文字

    # 生成图片绘制对象
    result_image_draw = ImageDraw.Draw(result_image)

    # 绘制第一行的文字
    text_1_width, text_1_height = result_image_draw.textsize(text_1, font=font)
    result_image_draw.text((78, 1647, 80 + text_1_width, 1647 + text_1_height),
                           text_1, font=font, fill=(255, 255, 255))

    # 绘制第二行的文字
    text_2_width, text_2_height = result_image_draw.textsize(text_2, font=font)
    result_image_draw.text((78, 1700, 80 + text_2_width, 1700 + text_2_height),
                           text_2, font=font, fill=(255, 255, 255))

    return result_image


# 文件地址列表
PATH_STUDENT_INFO = r"E:\【工作文件】\北二外学位图合成\学生信息表.csv"  # 学生信息表
PATH_PHOTO_SOURCE = r"E:\【工作文件】\北二外学位图合成\目标图"  # 学生照片：目标图（原始图）——图片格式：jpg
PATH_PHOTO_MERGE = r"E:\【工作文件】\北二外学位图合成\融合图"  # 学生照片：融合图（第1步处理结果）——图片格式：jpg
PATH_PHOTO_FRAME = r"E:\【工作文件】\北二外学位图合成\边框图"  # 学生照片：边框图（第2步处理结果）——图片格式：jpg
PATH_TEMPLATE = r"E:\【工作文件】\北二外学位图合成\模板图"  # 模板图
PATH_BASE = r"E:\【工作文件】\北二外学位图合成\底板图.jpg"  # 底板图
PATH_FONT = r"E:\【工作文件】\北二外学位图合成\思源黑.otf"  # 字体文件


def main(test=False, valid_number=None):
    """
    毕业照生成运行主程序

    :param test: <bool> 测试模式开关，为True则启动标准测试模式，每种模板图测试2张
    :param valid_number: <list> 测试模式开关，非空则启动自定义测试模式，只测试列表中包含的学号
    """
    # 【测试】各模板图测试数量变量
    test_model = {}

    # 读取学生信息及照片列表
    students_info_by_id, students_info_by_number = load_students_info(PATH_STUDENT_INFO)  # 载入学生信息表
    template_image_dict = load_template_image(PATH_TEMPLATE)  # 载入模板图列表
    students_photo_source = [re.sub(r"\.(jpe?g|png)$", "", name) for name in os.listdir(PATH_PHOTO_SOURCE)]
    students_photo_merge = [re.sub(r"\.(jpe?g|png)$", "", name) for name in os.listdir(PATH_PHOTO_MERGE)]

    # 检查数据的完整性
    print("\n只有照片，学生信息表里没有信息的学生：")
    for student_id in students_photo_source:
        if student_id not in students_info_by_id:
            print(student_id)

    print("\n学生信息表里有信息，但是没照片的学生：")
    for student_id in students_info_by_id:
        if student_id not in students_photo_source:
            print(student_id)

    # 筛选需要进行第1步处理（人脸融合）的图片列表
    step_1_list = []
    for student_id in students_info_by_id:
        student_number = students_info_by_id[student_id]["number"]  # 依据学生身份证号提取学生学号
        if student_number not in students_photo_merge and student_id in students_photo_source:
            step_1_list.append(student_id)
    print("\n需要进行第1步处理（人脸融合）的图片数量:", len(step_1_list), "\n")

    # 进行第1步处理（人脸融合）
    for i in range(len(step_1_list)):
        # 载入学生信息
        student_id = step_1_list[i]  # 提取学生身份证号
        student_number = students_info_by_id[student_id]["number"]  # 依据学生身份证号提取学生学号
        student_gender = students_info_by_id[student_id]["gender"]  # 依据学生身份证号提取学生性别
        student_level = students_info_by_id[student_id]["level"]  # 依据学生身份证号提取学生学位等级：本科/硕士
        student_type = students_info_by_id[student_id]["type"]  # 依据学生身份证号提取学生学位类型：文科/理科

        # 计算模板图名称
        template_name = student_level + "_" + student_type + "_" + student_gender

        # 【测试】控制各模板图测试数量
        if test:
            if template_name not in test_model:
                test_model[template_name] = 1
            elif test_model[template_name] < 10:
                test_model[template_name] += 1
            else:
                continue
        if valid_number:
            if student_number not in valid_number:
                continue

        print("执行人脸融合", "(" + str(i + 1) + "/" + str(len(step_1_list)) + ")", ":", student_number, "...")

        # 选择对应模板图
        if template_name in template_image_dict:
            template_image = template_image_dict[template_name]
        else:
            print("缺少模板图:", template_name)
            continue

        # 打开对应的目标图
        target_image = Image.open(os.path.join(PATH_PHOTO_SOURCE, student_id + ".jpg"))

        # 执行人脸融合
        merge_image = face_merge(template_image, target_image)

        # 存储人脸融合结果图
        merge_image.save(os.path.join(PATH_PHOTO_MERGE, student_number + ".jpg"), quality=100)

    # 读取照片列表
    students_photo_merge = [re.sub(r"\.(jpe?g|png)$", "", name) for name in os.listdir(PATH_PHOTO_MERGE)]
    students_photo_frame = [re.sub(r"\.(jpe?g|png)$", "", name) for name in os.listdir(PATH_PHOTO_FRAME)]
    base_image = Image.open(PATH_BASE)  # 打开底板图到PIL.Image对象

    # 筛选需要进行第2步处理（配置底板）的图片列表
    step_2_list = []
    for student_number in students_photo_merge:
        if student_number not in students_photo_frame:
            step_2_list.append(student_number)
    print("\n需要进行第2步处理（配置底板）的图片数量:", len(step_2_list))

    # 载入底板图绘制使用的字体
    font = ImageFont.truetype(PATH_FONT, 31)

    # 执行外框处理
    for i in range(len(step_2_list)):
        # 载入学生信息
        student_number = step_2_list[i]  # 提取学生身份证号
        student_name = students_info_by_number[student_number]["name"]  # 依据学生学号提取学生姓名
        student_academy = students_info_by_number[student_number]["academy"]  # 依据学生学号提取学生所在学院
        print("执行边框绘制", "(" + str(i + 1) + "/" + str(len(step_2_list)) + ")", ":", student_number, "...")

        # 准备学生融合图
        merge_image = Image.open(os.path.join(PATH_PHOTO_MERGE, student_number + ".jpg"))

        # 绘制底板图内容
        result_image = draw_frame(base_image, merge_image, font, student_number, student_name, student_academy)

        # 存储底板绘制结果图
        result_image.save(os.path.join(PATH_PHOTO_FRAME, student_number + ".jpg"), quality=100)


if __name__ == "__main__":
    main(test=True)
