from OSMPythonTools.api import Api
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
import numpy as np

api = Api()
way = api.query("way/997484334")

# print([(node.lat(), node.lon()) for node in way.nodes()])

relation = api.query("relation/13383366")

members = relation.members()
river_lat = []
river_lng = []

for member in members:
    way = api.query(member.type() + "/" + str(member.id()))
    for node in way.nodes():
        river_lat.append(node.lat())
        river_lng.append(node.lon())

plt.plot(river_lat, river_lng)

fn = CubicSpline(river_lat, river_lng)

x = np.linspace(min(river_lat), max(river_lat), 100)
y = fn(x)

plt.plot(x, y)

plt.show()
