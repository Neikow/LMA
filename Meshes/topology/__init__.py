from math import inf
from Meshes.msh_transformer.instance import MSHInstance
from Meshes.msh_transformer.transformer import BoundingBox
from scipy.interpolate import griddata
import numpy as np


class Topology:
    boundaries: BoundingBox | None

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.msh = MSHInstance(file_path)
        self.boundaries = None
        self.boundaries = self.get_boundaries()

        xy, z = [], []

        for node in self.msh.nodes:
            xy.append([node.x, node.y])
            z.append(node.z)

        print(self.boundaries)

        XY = np.array(xy)
        print(XY.shape)
        Z = np.array(z)
        print(Z.shape)
        XI = np.array([(0, 0)])
        print(XI.shape)

        print(griddata(XY, np.array(z), XI, method="linear"))

    def get_boundaries(self):
        if self.boundaries:
            return self.boundaries
        else:
            self.boundaries = self._compute_boundaries()
            return self.boundaries

    def _compute_boundaries(self):
        min_x, min_y, min_z = inf, inf, inf
        max_x, max_y, max_z = -inf, -inf, -inf

        for node in self.msh.nodes:
            min_x = min(min_x, node.x)
            max_x = max(max_x, node.x)
            min_y = min(min_y, node.y)
            max_y = max(max_y, node.y)
            min_z = min(min_z, node.z)
            max_z = max(max_z, node.z)

        return BoundingBox(min_x, max_x, min_y, max_y, min_z, max_z)

    def get_height(self, x: float, y: float):
        return self.interpolator((x, y))
