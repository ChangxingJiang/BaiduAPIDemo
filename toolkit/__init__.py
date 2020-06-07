import base64


def load_file_in_base64(path):
    """
    载入文件并进行Base64编码

    :param path: <str> 文件路径
    :return: <str> Base64编码后的文件
    """
    with open(path, 'rb') as f:
        return str(base64.b64encode(f.read()), encoding='utf-8')


def save_file_as_base64(path, data):
    """
    将数据进行Base64解码后存储到文件

    :param path: <str> 文件路径
    :param data: <str> Base64编码的数据
    :return: <None>
    """
    with open(path, 'wb') as f:
        f.write(base64.b64decode(data))
