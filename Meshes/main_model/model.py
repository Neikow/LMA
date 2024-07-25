from typing import List

import numpy as np

from Meshes.gmesher import gmsh, geo
from Meshes.main_model.geometry import collection
from Meshes.main_model.sizing import (
    wall_thickness_top,
    ground_height,
    dam_size_top,
    dam_height,
    water_length,
    dam_thickness,
    side_extension,
    wall_height,
)
from Meshes.msh_transformer.instance import MSHInstance
from Meshes.msh_transformer.transformer import Transformer, BoundingBox
from Meshes.tsankov_kamak_dam import forward_deformation

from Meshes.main_model.topology.read_hgt import interpolator as height_deformation

gmsh.option.setNumber("General.Verbosity", 0)

geo.synchronize()

# gmsh.option.setNumber("Mesh.ElementOrder", 2)

print("# Generating mesh...")
gmsh.model.mesh.generate(3)
gmsh.option.setNumber("Mesh.MshFileVersion", 2.2)

gmsh.write("output.msh")

collection.write_material_input("material.input")

h_min = +np.infty

threshold = 1
bounding_box_front = BoundingBox(
    wall_thickness_top + side_extension,
    wall_thickness_top + side_extension + dam_size_top,
    ground_height,
    ground_height + dam_height,
    water_length + dam_thickness,
    water_length + dam_thickness,
    threshold,
)

bounding_box_back = BoundingBox(
    wall_thickness_top + side_extension,
    wall_thickness_top + side_extension + dam_size_top,
    ground_height,
    ground_height + dam_height,
    water_length,
    water_length,
    threshold,
)

geo.synchronize()


def transform_front(x: float, y: float, z: float, mats: List[int], on_faces: List[str]):
    dx, dy, dz = 0, 0, 0
    x0, y0, z0 = (
        x - bounding_box_front.min_x,
        y - bounding_box_front.min_y,
        z - bounding_box_front.min_z,
    )
    qx = BoundingBox.get_dampening_coefficient(
        x, bounding_box_front.min_x, bounding_box_front.max_x
    )

    dz += (
        forward_deformation(
            np.array([y0 - dam_height / 2]),
            np.array([x0 - dam_size_top / 2]),
        )[0]
        - 50
    )

    dz *= qx

    return x + dx, y + dy, z + dz, False


def transform_back(x: float, y: float, z: float, mats: List[int], on_faces: List[str]):
    dx, dy, dz = 0, 0, 0
    x0, y0, z0 = (
        x - bounding_box_back.min_x,
        y - bounding_box_back.min_y,
        z - bounding_box_back.min_z,
    )

    qx = BoundingBox.get_dampening_coefficient(
        x, bounding_box_back.min_x, bounding_box_back.max_x
    )

    dz += (
        (
            forward_deformation(
                np.array([y0 - dam_height / 2]),
                np.array([x0 - dam_size_top / 2]),
            )[0]
        )
        - 50
        - dam_thickness
    )

    dz *= qx

    return x + dx, y + dy, z + dz, False


def apply_topology(x: float, y: float, z: float, mats: List[int], on_faces: List[str]):
    x0, y0, z0 = (
        x - (side_extension + wall_thickness_top + dam_size_top / 2),
        y,
        z - (water_length + dam_thickness / 2),
    )

    c = 1

    angle = 35  # deg

    # height factor
    mu = max(0, y0 / (ground_height + wall_height))

    u0 = np.array([x0 / 1000 - 1, z0 / 1000])
    # apply rotation
    rot = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
    # matrix product
    u0 = np.dot(rot, u0)

    deformation = height_deformation(*u0)

    dy = deformation * c * mu

    return x, y + dy, z, False


print("# Applying transforms...")
MSHInstance("output.msh").apply_transform(
    [
        Transformer(
            bounding_box_front,
            transform_front,
        ),
        Transformer(
            bounding_box_back,
            transform_back,
        ),
        Transformer(
            BoundingBox.infinite(),
            apply_topology,
        ),
    ],
    "output_transformed.msh",
)

print("# Writing output...")
gmsh.open("output_transformed.msh")

gmsh.write("output_transformed.vtk")

gmsh.fltk.run()

gmsh.finalize()
