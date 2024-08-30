import math
import time
from typing import List

import numpy as np

from gmesher import gmsh, geo
from geometry import collection
from sizing import (
    wall_thickness_top,
    ground_height,
    dam_size_top,
    dam_height,
    water_length,
    dam_thickness,
    side_extension,
    wall_height, air_length,
)
from instance import MSHInstance
from transformer import Transformer, BoundingBox
from tsankov_kamak_dam import forward_deformation, backward_deformation

gmsh.option.setNumber("General.Verbosity", 0)

geo.synchronize()

# gmsh.option.setNumber("Mesh.ElementOrder", 2)

start_time = time.time()

print("# Generating mesh...")
gmsh.model.mesh.generate(3)
gmsh.option.setNumber("Mesh.MshFileVersion", 2.2)

gmsh.write("output.msh")

collection.write_material_input("material.input")

h_min = +np.infty

threshold = 0.1

x_offset = dam_size_top / 3
y_offset = 2 * dam_height
z_offset = (water_length + air_length) / 2 / 100

bounding_box_front = BoundingBox(
    wall_thickness_top + side_extension - x_offset,
    wall_thickness_top + side_extension + x_offset + dam_size_top,
    ground_height - y_offset,
    ground_height + y_offset + dam_height,
    water_length + dam_thickness,
    water_length + dam_thickness + z_offset,
    threshold,
)

bounding_box_back = BoundingBox(
    wall_thickness_top + side_extension - x_offset,
    wall_thickness_top + side_extension + x_offset + dam_size_top ,
    ground_height - y_offset,
    ground_height + y_offset + dam_height,
    water_length - z_offset,
    water_length,
    threshold,
)

geo.synchronize()

source = (8000., 8000., 8000.)

points = [source]

max_y = 0
min_y = math.inf

def transform_front(x: float, y: float, z: float, mats: List[int], on_faces: List[str]):
    global max_y, min_y
    dx, dy, dz = 0, 0, 0
    x0, y0, z0 = (
        x - bounding_box_front.min_x - x_offset,
        y - bounding_box_front.min_y - y_offset,
        z - bounding_box_front.min_z,
    )
    qx = BoundingBox.get_dampening_coefficient(
        x, bounding_box_front.min_x, bounding_box_front.max_x
    )

    qz = (bounding_box_front.max_z - z) / (bounding_box_front.max_z - bounding_box_front.min_z)

    if y0 > max_y:
        max_y = y0
    if y0 < min_y:
        min_y = y0

    # move the nodes at the bottom of the dam
    dz += 10 * ((100 - y0) / 100) ** 4

    dz += 10 * ((100 - y0) / 100) ** 2 * ((x0 - dam_size_top / 2) / dam_size_top) ** 2

    dz += (
        backward_deformation(
            np.array([y0 - dam_height / 2]),
            np.array([x0 - dam_size_top / 2]),
        )[0]
    ) - 70 + dam_thickness

    dz *= qz

    if not use_topo:
        points.append((x + dx, y + dy, z + dz))

    return x + dx, y + dy, z + dz, False


def transform_back(x: float, y: float, z: float, mats: List[int], on_faces: List[str]):
    dx, dy, dz = 0, 0, 0
    x0, y0, z0 = (
        x - bounding_box_back.min_x - x_offset,
        y - bounding_box_back.min_y - y_offset,
        z - bounding_box_back.min_z,
    )

    qz = z0 / (bounding_box_back.max_z - bounding_box_back.min_z)

    dz += (
        (
            forward_deformation(
                np.array([y0 - dam_height / 2]),
                np.array([x0 - dam_size_top / 2]),
            )[0]
        ) - 70
    )

    dz *= qz

    # dz *= qx

    if not use_topo:
        points.append((x + dx, y + dy, z + dz))

    return x + dx, y + dy, z + dz, False


topography_threshold = ground_height / 3


def apply_topography(x: float, y: float, z: float, mats: List[int], on_faces: List[str]):
    x0, y0, z0 = (
        x - (side_extension + wall_thickness_top + dam_size_top / 2),
        y,
        z - (water_length + dam_thickness / 2),
    )

    c = 1

    u0 = np.array([-x0 / 1000, z0 / 1000])

    # mu = 1
    mu = max(0, min(1, y0 / (ground_height + wall_height - topography_threshold)))

    # deformation = 0
    # center_coefficient = 4
    # average_around = 20
    #
    # for j in range(-1, 2):
    #     for k in range(-1, 2):
    #         dd = height_deformation(u0[0] + j * average_around / 1000, u0[1] + k * average_around / 1000)
    #         if j == k == 0:
    #             deformation += dd * center_coefficient
    #         else:
    #             deformation += dd
    #
    # deformation /= (8 + center_coefficient)

    deformation = height_deformation(*u0)

    dy = deformation * c * mu

    if 2 in mats:
        points.append((x, y + dy, z))

    return x, y + dy, z, False


x_extent = side_extension + wall_thickness_top + dam_size_top + wall_thickness_top + side_extension
z_extent = water_length + dam_thickness + air_length

use_topo = True

z_extent_offset = (air_length + water_length) / 2 / 3
x_extent_offset = (side_extension + wall_thickness_top) / 3

if use_topo:
    from read_hgt import get_interpolator
    height_deformation, topo_h_min, topo_h_max = get_interpolator(
        (z_extent - z_extent_offset) / 1000,
        (x_extent - x_extent_offset) / 1000,
        (max(z_extent - z_extent_offset, x_extent - x_extent_offset)) / 1000 * 1.4)
else:
    topo_h_min = -dam_height * 2
    topo_h_max = dam_height * 2


def create_stations(x: float, y: float, z: float, mats: List[int], on_faces: List[str]):
    points.append((x, y, z))

    return x, y, z, False


print("# Applying transforms...")
MSHInstance("output.msh").apply_transform(
    [
        # Transformer.material_filter(-3),
        Transformer(
            bounding_box_back,
            transform_back,
        ),
        Transformer(
            bounding_box_front,
            transform_front,
        ),
        # Transformer(
        #     bounding_box_back,
        #     create_stations,
        # ),
        # Transformer(
        #     bounding_box_front,
        #     create_stations,
        # ),
        Transformer(
            BoundingBox.infinite(),
            apply_topography,
        ) if use_topo else None,
    ],
    "output_transformed.msh",
    100,
)

print("# Writing output...")

gmsh.open("output_transformed.msh")

gmsh.write("output_transformed.vtk")

print(len(points))

with open('stations.txt', 'w') as f:
    f.write('\n'.join([' '.join([f'{x:.4f}' for x in p]) for p in points]))

offset = 1

box_threshold = 100

boxes = [
    # top
    (
        -box_threshold, 0 - box_threshold, -box_threshold,
        x_extent + box_threshold, ground_height + topo_h_max + box_threshold, z_extent + box_threshold
    ),
    # x+
    (
        x_extent - box_threshold, -box_threshold, -box_threshold,
        -box_threshold, ground_height + topo_h_max + box_threshold, z_extent + box_threshold
    ),
    # x-
    (
        -box_threshold, -box_threshold, -box_threshold,
        box_threshold, ground_height + topo_h_max + box_threshold, z_extent + box_threshold + box_threshold
    ),
    # z+
    (
        -box_threshold, -box_threshold, z_extent - box_threshold,
        x_extent + box_threshold, ground_height + topo_h_max + box_threshold, box_threshold
    ),
    # z-
    (
        -box_threshold, -box_threshold, -box_threshold,
        x_extent + box_threshold, ground_height + topo_h_max + box_threshold, +box_threshold
    ),
]

with open('selection.txt', 'w') as f:
    f.write('deselect all;\n')
    for box in boxes:
        parts = []
        for i in range(6):
            if i > 2:
                parts.append(f'{box[i] + offset:.1f}')
            else:
                parts.append(f'{box[i] - offset:.1f}')

        f.write('select box = ' + ' '.join(parts) + ';\n')


end_time = time.time()

print(f'# Execution took : {end_time - start_time} s')

gmsh.fltk.run()

gmsh.finalize()
