from .utils import inMixzone
from .location_desensitize import lap_coord_desensitize, Coord

def trace_desensitize(traces: list[Coord], zone_coords: list[Coord], eps=0.9, dist_thresh=1000) -> list[Coord]:
    new_traces = []
    for tr in traces:
        if inMixzone(tr, zone_coords, dist_thresh):
            new_traces.append(lap_coord_desensitize(*tr, eps))
        else:
            new_traces.append(tr)
    return new_traces


if __name__ == '__main__':
    # 东直门地铁站
    zone1_x = 116.435842
    zone1_y = 39.941626
    # 西直门
    zone2_x = 116.353714
    zone2_y = 39.939588
    # 建国门
    zone3_x = 116.435806
    zone3_y = 39.908501
    # 复兴门
    zone4_x = 116.356866
    zone4_y = 39.907242

    trace = [(1.0, 2.0), (116.435842, 39.941626), (3.0, 4.0)]
    print(trace_desensitize(trace, [(zone1_x, zone1_y), (zone2_x, zone2_y), (zone3_x, zone3_y), (zone4_x, zone4_y)]))
