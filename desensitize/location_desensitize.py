from typing import TypeVar, Union, Tuple
from sympy import Symbol, solve, pi, log
import math
import random

Latitude = TypeVar('Latitude', bound=float)
Longitude = TypeVar('Longitude', bound=float)
CoordComponent = Union[Latitude, Longitude]
Coord = Tuple[Latitude, Longitude]

x = Symbol('x')
e = 2.718281828459045


def lap_alg(X: int, x1: float, y1: int, eps: float):
    theta = random.uniform(0, 2 * pi)
    p = random.uniform(0, 1)
    M = solve(x - log((p / x), e), x)
    r = -(1.0 / eps) * (M[0] * ((p - 1) / math.e) + 1)
    x2 = int(x1 + r * math.cos(theta))
    y2 = int(y1 + r * math.sin(theta))
    z = (y2 - 1) * 32 + x2
    return z


def lap_component_desensitize(coord: CoordComponent, eps: float=0.9) -> float:
    # coord_int = int(coord)
    coord_dec = coord - int(coord)

    X = int(coord_dec * 100) + 1

    X_dec = (X-1) % 32 + 1
    X_int = int((X-1)/32) + 1
    pseudo_coord = lap_alg(X, X_dec, X_int, eps)
    pseudo_coord = coord - float(pseudo_coord) / 10000

    return pseudo_coord

def lap_coord_desensitize(lat: Latitude, lng: Longitude, eps: float=0.9) -> (float, float):
    reslat = lap_component_desensitize(lat, eps)
    reslng = lap_component_desensitize(lng, eps)
    return reslat, reslng

if __name__ == '__main__':
    print(lap_coord_desensitize(10.3,10.3, eps=0.1))