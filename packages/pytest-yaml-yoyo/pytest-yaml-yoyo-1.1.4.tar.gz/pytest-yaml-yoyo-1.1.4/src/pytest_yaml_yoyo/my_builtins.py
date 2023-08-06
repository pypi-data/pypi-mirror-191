import random
import uuid
from faker import Faker
import time


def current_time(f: str = '%Y-%m-%d %H:%M:%S') -> str:
    """获取当前时间 2022-12-16 22:13:00"""
    return time.strftime(f)


def rand_value(target: list):
    """从返回的 list 结果随机取值"""
    if isinstance(target, list):
        return target[random.randint(0, len(target)-1)]
    else:
        return target


def rand_str(len_start=None, len_end=None) -> str:
    """生成随机字符串， 如
        ${rand_str()}  得到32位字符串
        ${rand_str(3)}  得到3位字符串
        ${rand_str(3, 10)}  得到3-10位字符串
    """
    uuid_str = str(uuid.uuid4()).replace('-', '')
    print(len(uuid_str))
    if not len_start and not len_end:
        return uuid_str
    if not len_end:
        return uuid_str[:len_start]
    else:
        return uuid_str[:random.randint(len_start, len_end)]


# 生成随机测试数据
fake = Faker(locale="zh_CN")
