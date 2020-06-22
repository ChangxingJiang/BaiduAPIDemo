from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

import tencent_environment as tencent_env


def open_cos_client():
    """
    打开腾讯云对象存储客户端对象

    :return: <CosS3Client> 腾讯云客户端对象
    """
    config = CosConfig(Region=tencent_env.COS[0]["Region"],
                       Scheme="http",
                       SecretId=tencent_env.COS[0]["SecretId"],
                       SecretKey=tencent_env.COS[0]["SecretKey"])
    return CosS3Client(config)
