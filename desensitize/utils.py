import math
from math import asin, sqrt, pow, sin, cos

from desensitize.location_desensitize import Coord

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
