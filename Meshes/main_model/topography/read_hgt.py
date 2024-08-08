import os
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource
from matplotlib import colormaps
from scipy.interpolate import CloughTocher2DInterpolator as CT, LinearNDInterpolator

from OSMPythonTools.api import Api

dam_position = 41.822540, 24.442718


def get_interpolator(x_size, y_size, compute_size = 30):
    dirname = os.path.dirname(__file__)
    fn = os.path.join(dirname, "N41E024.hgt")

    siz = os.path.getsize(fn)
    dim = int(math.sqrt(siz / 2))

    assert dim * dim * 2 == siz, "Invalid file size"

    data = np.fromfile(fn, np.dtype(">i2"), dim * dim).reshape((dim, dim))

    lat = np.linspace(42, 41, dim)
    long = np.linspace(24, 25, dim)
    # X, Y = np.meshgrid(x, y)
    z = data - np.average(data)

    topo_h_min = np.min(z)
    topo_h_max = np.max(z)

    def rotate(x, y):
        angle = np.deg2rad(-36)  # rad
        rot = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])

        u0 = np.array([x, y])
        u0 = np.dot(rot, u0)

        return u0[0], u0[1]

    def lat_long_to_xy(_lat, _long):
        return (
            (dam_position[0] - _lat) * 110.574,
            (_long - dam_position[1]) * 111.320 * np.cos(np.radians(_lat)),
        )

    x, y = lat_long_to_xy(lat, long)

    points = []
    values = []

    x_max = x_size / 2
    x_min = -x_size / 2
    y_max = y_size / 2
    y_min = -y_size

    def interpolate(xy, z):
        x = xy[:, 0]
        y = xy[:, 1]
        print('# Compiling the interpolator')
        f = CT(xy, z)

        # this inner function will be returned to a user
        def new_f(xx, yy):
            # evaluate the CT interpolator. Out-of-bounds values are nan.
            zz = f(xx, yy)
            nans = np.isnan(zz)

            if nans.any():
                # for each nan point, find its nearest neighbor
                inds = np.argmin(
                    (x[:, None] - xx[nans]) ** 2 + (y[:, None] - yy[nans]) ** 2, axis=0
                )
                # ... and use its value
                zz[nans] = z[inds]
            return zz

        print('# Interpolator ready')

        return new_f


    sqrt2 = np.sqrt(2)

    print('# Preparing the topological data')

    N = dim * dim
    steps = N // 10

    for i in range(0, dim):
        for j in range(0, dim):
            if (i * dim + j) % steps == 0:
                print(f'{((i * dim + j) / (dim * dim) * 100):.0f}%')

            if abs(x[i]) / sqrt2 > compute_size / 2 or abs(y[j]) / sqrt2 > compute_size / 2:
                continue

            _x, _y = rotate(x[i], y[j])

            if x_min > _x or x_max < _x or y_min > _y or y_max < _y:
                continue

            points.append([_x, _y])
            values.append(z[i, j])

    interpolator = interpolate(np.array(points), np.array(values))

    return interpolator, topo_h_min, topo_h_max


if __name__ == "__main__":
    size = 3

    x_new = np.linspace(-size / 2, size / 2, 60)
    y_new = np.linspace(-size / 2, size / 2, 60)

    X_new, Y_new = np.meshgrid(x_new, y_new)

    print('Interpolating new values')
    Z_new = get_interpolator(X_new, Y_new)[0]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    print('Plotting surface')
    ax.plot_surface(X_new, Y_new, Z_new, cmap="viridis", alpha=0.8)

    def get_points_from_way(way):
        pts = []
        for node in way.nodes():
            pts.append((node.lat(), node.lon()))

        return pts

    def plot(pts: list[tuple[float, float]], *args, **kwargs):
        x, y, z = [], [], []
        for pt in pts:
            _x, _y = lat_long_to_xy(pt[0], pt[1])

            _x, _y = rotate(_x, _y)

            if abs(_x) > size / 2 or abs(_y) > size / 2:
                continue

            _z = interpolator(_x, _y)

            x.append(_x)
            y.append(_y)
            z.append(_z + 0.2)

        ax.plot(x, y, z, *args, **kwargs)

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
    plot(dam_water_points, 'r.')

    dam = api.query('way/282669441')
    dam_points = get_points_from_way(dam)
    plot(dam_points, 'g.')

    plot([dam_position], 'y.')
    # plt.gca().set_aspect('equal')

    plt.show()
