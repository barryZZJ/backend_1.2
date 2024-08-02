import hashlib
import math
import random
import re
from datetime import datetime


def hashing_md5(s: str) -> str:
    """返回值为小写16进制字符串"""
    return hashlib.md5(s.encode()).hexdigest()


def hashing_sha256(s: str) -> str:
    """返回值为小写16进制字符串"""
    return hashlib.sha256(s.encode()).hexdigest()


def number_desensitize(text: float):
    text = re.sub(r'\d', lambda d: str(random.randint(0, 9)), str(text))
    return float(text)
    # return float(text) if '.' in text else int(text)

