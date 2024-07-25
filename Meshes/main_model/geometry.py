# ==========
# Points
# ==========
from math import tan
from Meshes.gmesher import (
    VolumeGroup,
    PML,
    Point,
    Quad,
    QuadGroup,
    Volume,
    geo,
    PhysicalGroupCollection,
    options,
)
from Meshes.main_model.materials import material_dam, material_ground, material_water
from Meshes.main_model.sizing import (
    pml_thickness,
    x_upper,
    z_upper,
    x_zero,
    y_zero,
    z_zero,
    wall_thickness_bottom,
    ground_height,
    dam_size_bottom,
    water_height,
    dam_height,
    wall_height,
    wall_thickness_top,
    incline_rad,
    water_length,
    dam_thickness,
    air_length,
    side_extension,
)

# ====================
#         Dam
# ====================
#  |-\------------/-|
#  |  \----------/  |
#  |   \        /   |
#  |    --------    |
#  |----------------|

before_dam_elements = [4, 4, 8, 8, 16]
# before_dam_elements = [1]
around_dam_elements = [1]
# around_dam_elements = [1]
after_dam_elements = [16, 8, 8, 4, 4]
# after_dam_elements = [1]
extension_elements = [16, 8, 8, 4, 4]
# extension_elements = [1]
pml_elements = [1]

options["transfinite"] = 16

# Ground points
pg1 = Point(x_zero, y_zero, z_zero)
pg2 = pg1.offset_x(wall_thickness_bottom)
pg3 = pg2.offset_y(ground_height)
pg4 = pg3.offset_x(-wall_thickness_bottom)

pg5 = pg2.offset_x(dam_size_bottom)
pg6 = pg5.offset_x(wall_thickness_bottom)
pg7 = pg6.offset_y(ground_height)
pg8 = pg7.offset_x(-wall_thickness_bottom)

sgb1 = Quad(pg1, pg2, pg3, pg4)
sgb2 = Quad(pg2, pg5, pg8, pg3)
sgb3 = Quad(pg5, pg6, pg7, pg8)

pg9 = pg4.offset_y(water_height)
pg10 = pg9.offset_y(dam_height - water_height)
pg11 = pg10.offset_y(wall_height - dam_height)
pg12 = pg11.offset_x(wall_thickness_top)
pg13 = pg12.offset(
    tan(incline_rad) * (wall_height - dam_height), -(wall_height - dam_height)
)
pg14 = pg13.offset(
    tan(incline_rad) * (dam_height - water_height), -(dam_height - water_height)
)

sgl1 = Quad(pg4, pg3, pg14, pg9)
sgl2 = Quad(pg9, pg14, pg13, pg10)
sgl3 = Quad(pg10, pg13, pg12, pg11)

pg15 = pg7.offset_y(water_height)
pg16 = pg15.offset_y(dam_height - water_height)
pg17 = pg16.offset_y(wall_height - dam_height)
pg18 = pg17.offset_x(-wall_thickness_top)
pg19 = pg18.offset(
    -tan(incline_rad) * (wall_height - dam_height), -(wall_height - dam_height)
)
pg20 = pg19.offset(
    -tan(incline_rad) * (dam_height - water_height), -(dam_height - water_height)
)

sgr1 = Quad(pg8, pg7, pg15, pg20)
sgr2 = Quad(pg20, pg15, pg16, pg19)
sgr3 = Quad(pg19, pg16, pg17, pg18)

sgg = QuadGroup([sgb1, sgb2, sgb3, sgl1, sgl2, sgl3, sgr1, sgr2, sgr3])

sw = Quad(pg3, pg8, pg20, pg14)

sgw = QuadGroup([sw])

water_volume = sgw.extrude_z(water_length, before_dam_elements)
ground_before_dam_volume = sgg.extrude_z(water_length, before_dam_elements)

ground_around_dam_volume = Volume(
    geo.extrude(
        ground_before_dam_volume.get_surfaces_in_extrusion_direction(),
        0,
        0,
        dam_thickness,
        around_dam_elements,
        recombine=True,
    )
)

dam_bottom_volume = Volume(
    geo.extrude(
        water_volume.get_surfaces_in_extrusion_direction(),
        0,
        0,
        dam_thickness,
        around_dam_elements,
        recombine=True,
    )
)

top_dam_surface = QuadGroup([Quad.from_ids([26, 30, 64, 94])])

dam_top_volume = top_dam_surface.extrude_z(dam_thickness, around_dam_elements)

ground_after_dam_volume = Volume(
    geo.extrude(
        ground_around_dam_volume.get_surfaces_in_extrusion_direction(),
        0,
        0,
        air_length,
        after_dam_elements,
        recombine=True,
    )
)

ground_extension_left_volume = Volume(
    geo.extrude(
        [
            (2, 119),
            (2, 207),
            (2, 229),
            (2, 251),
            (2, 317),
            (2, 405),
            (2, 427),
            (2, 449),
            (2, 560),
            (2, 648),
            (2, 670),
            (2, 692),
        ],
        side_extension,
        0,
        0,
        extension_elements,
        recombine=True,
    )
)

ground_extension_right_volume = Volume(
    geo.extrude(
        [
            (2, 83),
            (2, 149),
            (2, 171),
            (2, 193),
            (2, 281),
            (2, 347),
            (2, 369),
            (2, 391),
            (2, 524),
            (2, 590),
            (2, 612),
            (2, 634),
        ],
        -side_extension,
        0,
        0,
        extension_elements,
        recombine=True,
    )
)

pml_xm = Volume(
    geo.extrude(
        ground_extension_right_volume.get_surfaces_in_extrusion_direction(),
        -pml_thickness,
        0,
        0,
        [1],
        recombine=True,
    ),
)

pml_xp = Volume(
    geo.extrude(
        ground_extension_left_volume.get_surfaces_in_extrusion_direction(),
        pml_thickness,
        0,
        0,
        [1],
        recombine=True,
    ),
)

pml_zp = Volume(
    geo.extrude(
        ground_after_dam_volume.get_surfaces_in_extrusion_direction()
        + [
            ground_extension_left_volume.extrusion[i]
            for i in range(
                4 + 6 * 8, len(ground_extension_left_volume.extrusion), 5 + 1
            )
        ]
        + [
            ground_extension_right_volume.extrusion[i]
            for i in range(
                4 + 6 * 8, len(ground_extension_right_volume.extrusion), 5 + 1
            )
        ],
        0,
        0,
        pml_thickness,
        [1],
        recombine=True,
    )
)

pml_zm = Volume(
    geo.extrude(
        sgg.gmsh_surfaces()
        + [
            ground_extension_left_volume.extrusion[i]
            for i in range(2, 2 + 4 * 6, 5 + 1)
        ]
        + [
            ground_extension_right_volume.extrusion[i]
            for i in range(2, 2 + 4 * 6, 5 + 1)
        ],
        0,
        0,
        -pml_thickness,
        [1],
        recombine=True,
    )
)

pml_ym = Volume(
    geo.extrude(
        [ground_before_dam_volume.extrusion[i] for i in range(2, 2 + 2 * 6 + 1, 5 + 1)]
        + [
            ground_around_dam_volume.extrusion[i]
            for i in range(2, 2 + 2 * 6 + 1, 5 + 1)
        ]
        + [ground_after_dam_volume.extrusion[i] for i in range(2, 2 + 2 * 6 + 1, 5 + 1)]
        + [
            ground_extension_left_volume.extrusion[5],
            ground_extension_left_volume.extrusion[29],
            ground_extension_left_volume.extrusion[53],
        ]
        + [
            ground_extension_right_volume.extrusion[3],
            ground_extension_right_volume.extrusion[27],
            ground_extension_right_volume.extrusion[51],
        ],
        0,
        -pml_thickness,
        0,
        [1],
        recombine=True,
    ),
)

pml_xpym = Volume(
    geo.extrude(
        [
            pml_ym.extrusion[58],
            pml_ym.extrusion[64],
            pml_ym.extrusion[70],
        ],
        pml_thickness,
        0,
        0,
        [1],
        recombine=True,
    )
)

offset_pml_xmym = 12
pml_xmym = Volume(
    geo.extrude(
        [
            pml_ym.extrusion[i]
            for i in range(
                4 + offset_pml_xmym * 6, 4 + (offset_pml_xmym + 3) * 6, 5 + 1
            )
        ],
        -pml_thickness,
        0,
        0,
        [1],
        recombine=True,
    )
)

pml_ymzm = Volume(
    geo.extrude(
        [
            pml_ym.extrusion[2],
            pml_ym.extrusion[8],
            pml_ym.extrusion[14],
            pml_ym.extrusion[57],
            pml_ym.extrusion[77],
        ],
        0,
        0,
        -pml_thickness,
        [1],
        recombine=True,
    )
)

pml_ymzp = Volume(
    geo.extrude(
        [
            pml_ym.extrusion[4 + 6 * 6],
            pml_ym.extrusion[4 + 6 * 7],
            pml_ym.extrusion[4 + 6 * 8],
            pml_ym.extrusion[3 + 6 * 14],
            pml_ym.extrusion[5 + 6 * 11],
        ],
        0,
        0,
        pml_thickness,
        [1],
        recombine=True,
    )
)

pml_water = Volume(
    geo.extrude(sgw.gmsh_surfaces(), 0, 0, -pml_thickness, [1], recombine=True)
)

pml_xmymzp = Volume(
    geo.extrude(
        [
            (2, 2966),
        ],
        0,
        0,
        pml_thickness,
        [1],
        recombine=True,
    )
)

pml_xmzp = Volume(
    geo.extrude(
        [
            (2, 1422),
            (2, 1444),
            (2, 1466),
            (2, 1488),
        ],
        0,
        0,
        pml_thickness,
        [1],
        recombine=True,
    )
)

pml_xpymzp = Volume(
    geo.extrude(
        [
            (2, 2892),
        ],
        0,
        0,
        pml_thickness,
        [1],
        recombine=True,
    )
)

pml_xpzp = Volume(
    geo.extrude(
        [
            (2, 1686),
            (2, 1708),
            (2, 1730),
            (2, 1752),
        ],
        0,
        0,
        pml_thickness,
        [1],
        recombine=True,
    )
)

pml_xpzm = Volume(
    geo.extrude(
        [
            (2, 1502),
            (2, 1524),
            (2, 1546),
            (2, 1568),
        ],
        0,
        0,
        -pml_thickness,
        [1],
        recombine=True,
    )
)

pml_xpymzm = Volume(
    geo.extrude(
        [
            (2, 2856),
        ],
        0,
        0,
        -pml_thickness,
        [1],
        recombine=True,
    )
)

pml_xmymzm = Volume(
    geo.extrude(
        [
            (2, 2914),
        ],
        0,
        0,
        -pml_thickness,
        [1],
        recombine=True,
    )
)

pml_xmzm = Volume(
    geo.extrude(
        [
            (2, 1238),
            (2, 1260),
            (2, 1282),
            (2, 1304),
        ],
        0,
        0,
        -pml_thickness,
        [1],
        recombine=True,
    )
)

collection = PhysicalGroupCollection()

pml = {
    "x-y-z-": (
        pml_xmymzm,
        material_ground,
        PML(
            (0, -pml_thickness),
            (0, -pml_thickness),
            (0, -pml_thickness),
            0,
        ),
    ),
    "x-y-": (
        pml_xmym,
        material_ground,
        PML(
            (0, -pml_thickness),
            (0, -pml_thickness),
            (0, 0),
            0,
        ),
    ),
    "x-z-": (
        pml_xmzm,
        material_ground,
        PML(
            (0, -pml_thickness),
            (0, 0),
            (0, -pml_thickness),
            0,
        ),
    ),
    "x-": (
        pml_xm,
        material_ground,
        PML(
            (0, -pml_thickness),
            (0, 0),
            (0, 0),
            0,
        ),
    ),
    "x+": (
        pml_xp,
        material_ground,
        PML(
            (x_upper, pml_thickness),
            (0, 0),
            (0, 0),
            0,
        ),
    ),
    "z+": (
        pml_zp,
        material_ground,
        PML(
            (0, 0),
            (0, 0),
            (z_upper, pml_thickness),
            0,
        ),
    ),
    "z-": (
        pml_zm,
        material_ground,
        PML(
            (0, 0),
            (0, 0),
            (0, -pml_thickness),
            0,
        ),
    ),
    "y-": (
        pml_ym,
        material_ground,
        PML(
            (0, 0),
            (0, -pml_thickness),
            (0, 0),
            0,
        ),
    ),
    "x+y-": (
        pml_xpym,
        material_ground,
        PML(
            (x_upper, pml_thickness),
            (0, -pml_thickness),
            (0, 0),
            0,
        ),
    ),
    "y-z-": (
        pml_ymzm,
        material_ground,
        PML(
            (0, 0),
            (0, -pml_thickness),
            (0, -pml_thickness),
            0,
        ),
    ),
    "y-z+": (
        pml_ymzp,
        material_ground,
        PML(
            (0, 0),
            (0, -pml_thickness),
            (z_upper, pml_thickness),
            0,
        ),
    ),
    "x-z+": (
        pml_xmzp,
        material_ground,
        PML(
            (0, -pml_thickness),
            (0, 0),
            (z_upper, pml_thickness),
            0,
        ),
    ),
    "x+z-": (
        pml_xpzm,
        material_ground,
        PML(
            (x_upper, pml_thickness),
            (0, 0),
            (0, -pml_thickness),
            0,
        ),
    ),
    "x+z+": (
        pml_xpzp,
        material_ground,
        PML(
            (x_upper, pml_thickness),
            (0, 0),
            (z_upper, pml_thickness),
            0,
        ),
    ),
    "x-y-z+": (
        pml_xmymzp,
        material_ground,
        PML(
            (0, -pml_thickness),
            (0, -pml_thickness),
            (z_upper, pml_thickness),
            0,
        ),
    ),
    "x+y-z+": (
        pml_xpymzp,
        material_ground,
        PML(
            (x_upper, pml_thickness),
            (0, -pml_thickness),
            (z_upper, pml_thickness),
            0,
        ),
    ),
    "x+y-z-": (
        pml_xpymzm,
        material_ground,
        PML(
            (x_upper, pml_thickness),
            (0, -pml_thickness),
            (0, -pml_thickness),
            0,
        ),
    ),
    "water": (
        pml_water,
        material_water,
        PML(
            (0, 0),
            (0, 0),
            (0, -pml_thickness),
            2,
        ),
    ),
}

VolumeGroup(
    [
        ground_before_dam_volume,
        ground_around_dam_volume,
        ground_after_dam_volume,
        ground_extension_left_volume,
        ground_extension_right_volume,
    ]
).set_phy_group(collection, "Ground", material_ground)

VolumeGroup(
    [
        dam_top_volume,
        dam_bottom_volume,
    ]
).set_phy_group(collection, "Dam", material_dam)

VolumeGroup([water_volume]).set_phy_group(collection, "Water", material_water)

# Create PMLs
for direction, (volume, material, pml) in pml.items():
    VolumeGroup([volume]).set_pml(
        collection,
        f"PML_{direction}",
        material,
        pml,
    )
