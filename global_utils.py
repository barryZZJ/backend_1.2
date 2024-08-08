import base64
import math
import os
from math import asin, sqrt, pow, sin, cos

from desensitize.location_desensitize import Coord
from myeasyofd import OFD


def ofd_to_img(input_file):
    file_prefix = os.path.splitext(os.path.split(input_file)[1])[0]
    temp_dir = os.getenv('TEMP')
    with open(input_file, "rb") as f:
        ofdb64 = str(base64.b64encode(f.read()), "utf-8")
    ofd = OFD()  # 初始化OFD 工具类
    ofd.read(ofdb64, save_xml=True, xml_name=os.path.join(temp_dir, f'{file_prefix}_xml'))  # 读取ofdb64
    imgs = ofd.to_jpg()  # 转图片
    ofd.del_data()
    return imgs


EARTH_RADIUS = 6378137.0
DEG2RAD = math.pi / 180


def distance(lon1, lat1, lon2, lat2):
    """
    功能：计算两个位置点的距离（m）
    """
    lon1_rad = lon1 * DEG2RAD
    lon2_rad = lon2 * DEG2RAD
    lat1_rad = lat1 * DEG2RAD
    lat2_rad = lat2 * DEG2RAD
    lon_rad_diff_2to1 = lon2_rad - lon1_rad
    lat_rad_diff_2to1 = lat2_rad - lat1_rad

    # 转换距离
    range_2to1 = 2 * asin(sqrt(pow(sin(lat_rad_diff_2to1 / 2.0), 2) +
                               cos(lat1_rad) * cos(lat2_rad) * pow(sin(lon_rad_diff_2to1 / 2.0), 2))) * EARTH_RADIUS

    return range_2to1


def inMixzone(coord: Coord, zone_coords: list[Coord], dist_thresh=1000):
    """
    功能：判断是否在混合区内
    输入：
    coord: 目标的坐标
    zone_coords: 混合区的坐标列表
    dist_thresh: 距离阈值（米）
    输出：是否在混合区内
    """
    distances = [distance(*coord, zone_x, zone_y) for zone_x, zone_y in zone_coords]

    return any(dist <= dist_thresh for dist in distances)


def pdf_to_ofd(input_file, output_file):
    with open(input_file, "rb") as f:
        pdfb64 = f.read()
    ofd = OFD()
    ofd_bytes = ofd.pdf2ofd(pdfb64, optional_text=False)  # 转ofd # optional_text 生成可操作文本 True 输入也需要可编辑pdf
    ofd.del_data()
    with open(output_file, "wb") as f:
        f.write(ofd_bytes)


def ofd_to_pdf(input_file, output_file):
    with open(input_file, "rb") as f:
        ofdb64 = str(base64.b64encode(f.read()), "utf-8")
    ofd = OFD()  # 初始化OFD 工具类
    ofd.read(ofdb64, save_xml=False, xml_name="testxml")  # 读取ofdb64
    pdf_bytes = ofd.to_pdf()  # 转pdf
    ofd.del_data()
    with open(output_file, "wb") as f:
        f.write(pdf_bytes)
