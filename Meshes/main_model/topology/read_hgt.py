import os
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource
from matplotlib import colormaps
from scipy.interpolate import CloughTocher2DInterpolator, LinearNDInterpolator

dirname = os.path.dirname(__file__)
fn = os.path.join(dirname, "N41E024.hgt")

siz = os.path.getsize(fn)
dim = int(math.sqrt(siz / 2))

assert dim * dim * 2 == siz, "Invalid file size"

data = np.fromfile(fn, np.dtype(">i2"), dim * dim).reshape((dim, dim))

dam_position = 41.822540, 24.442718

lat = np.linspace(41, 42, dim)
long = np.linspace(24, 25, dim)
# X, Y = np.meshgrid(x, y)
z = data - np.average(data)


def lat_long_to_xy(_lat, _long):
    return (
        (_long - dam_position[1]) * 110.574 + 2,
        (_lat - dam_position[0]) * 111.320 * 0.65,
    )


x, y = lat_long_to_xy(lat, long)

points = []
values = []

size = 15

for i in range(0, dim):
    for j in range(0, dim):
        if abs(x[i]) > size / 2 or abs(y[j]) > size / 2:
            continue

        points.append([x[i], y[j]])
        values.append(z[i, j])

interpolator_path = os.path.join(dirname, "interpolator.npy")

force_recompute = True

if os.path.exists(interpolator_path) and not force_recompute:
    interpolator = np.load(interpolator_path, allow_pickle=True).item()
else:
    interpolator = CloughTocher2DInterpolator(
        np.array(points), np.array(values), fill_value=0
    )
    np.save(interpolator_path, interpolator, allow_pickle=True)

if __name__ == "__main__":
    river_points = [
        (41.82215235500653, 24.441268306705258),
        (41.820384938737035, 24.43891909208987),
        (41.815338194065774, 24.43679989320894),
        (41.811318827470785, 24.438334296154082),
        (41.807547196337296, 24.439286592321697),
        (41.805478064297155, 24.438364317836818),
        (41.80355226689969, 24.435099800489528),
        (41.80104134907913, 24.436111329737844),
        (41.79982043386554, 24.435437244559534),
        (41.79888205498856, 24.43523063948444),
    ]

    x_new = np.linspace(-size / 2, size / 2, 100)
    y_new = np.linspace(-size / 2, size / 2, 100)

    X_new, Y_new = np.meshgrid(x_new, y_new)

    Z_new = interpolator((X_new.flatten(), Y_new.flatten())).reshape(X_new.shape)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X_new, Y_new, Z_new, cmap="viridis", alpha=0.8)

    for point in river_points:
        x, y = lat_long_to_xy(*point)
        ax.scatter(x - 1, y, interpolator((x - 1, y)) + 1, color="red")

    plt.show()
