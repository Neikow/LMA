import math

from OSMPythonTools.api import Api
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
import numpy as np


def plot(points: list[tuple[float, float]], *args, **kwargs):
    x = []
    y = []
    for p in points:
        x.append(p[1] * 111.320 * math.cos(math.radians(p[0])))
        y.append(p[0] * 110.574)

    plt.plot(x, y, *args, **kwargs)


def get_points_from_way(way):
    pts = []
    for node in way.nodes():
        if node.lat() < 41.775:
            continue
        if node.lat() > 41.850:
            continue
        if node.lon() < 24.40:
            continue
        pts.append((node.lat(), node.lon()))

    return pts


api = Api()
way = api.query("way/997484334")

relation = api.query("relation/13383366")
members = relation.members()
river = []
for member in members:
    way = api.query(member.type() + "/" + str(member.id()))
    river += get_points_from_way(way)
plot(river, 'b.')

dam_water = api.query('way/119088050')
dam_water_points = get_points_from_way(dam_water)
plot(dam_water_points)

dam = api.query('way/282669441')
dam_points = get_points_from_way(dam)
plot(dam_points)

plt.gca().set_aspect('equal')

plt.show()

