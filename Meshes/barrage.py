from math import tan, atan
import gmesher as m
import mesh_transformer as mt

geo = m.geo
model = m.model

# ====================
#         Dam
# ====================
#  |-\------------/-|
#  |  \----------/  |
#  |   \        /   |
#  |    --------    |
#  |----------------|

m.options['transfinite'] = 10

# ==========
# Constantes
# ==========
dam_size_top = 320.0
dam_size_bottom = 100.0
dam_height = 90
dam_thickness = 5.0
wall_height = 100.0
wall_thickness = 100.0
ground_height = 10.0
water_height = 80.0
water_length = 1000.0
air_length = 1000.0
side_extension = 1000.0

pml_thickness = 1000.0

before_dam_elements = [1, 2, 4]
# before_dam_elements = [1]
around_dam_elements = [1]
# around_dam_elements = [1]
after_dam_elements = [4, 2, 1]
# after_dam_elements = [1]
extension_elements = [3, 2, 1, 1]
# extension_elements = [1]
pml_elements = [2]

# ==========
# Assertions
# ==========
assert dam_size_top > dam_size_bottom
assert wall_height >= dam_height
assert dam_height > water_height
assert wall_thickness > 0
assert ground_height > 0
assert water_height > 0

# ============
# Calculations
# ============
incline_rad = atan((dam_size_top - dam_size_bottom) / 2 / wall_height)

wall_thickness_top = wall_thickness
wall_thickness_bottom = wall_thickness + tan(incline_rad) * wall_height

x_zero = 0
y_zero = 0
z_zero = 0

x_upper = side_extension * 2 + dam_size_bottom + wall_thickness_bottom * 2
y_upper = 0
z_upper = water_length + dam_thickness + air_length

# ==========
# Points
# ==========

# Ground points
pg1 = m.Point(x_zero, y_zero, z_zero)
pg2 = pg1.offset_x(wall_thickness_bottom)
pg3 = pg2.offset_y(ground_height)
pg4 = pg3.offset_x(-wall_thickness_bottom)

pg5 = pg2.offset_x(dam_size_bottom)
pg6 = pg5.offset_x(wall_thickness_bottom)
pg7 = pg6.offset_y(ground_height)
pg8 = pg7.offset_x(-wall_thickness_bottom)

sgb1 = m.Quad(pg1, pg2, pg3, pg4)
sgb2 = m.Quad(pg2, pg5, pg8, pg3)
sgb3 = m.Quad(pg5, pg6, pg7, pg8)

pg9 = pg4.offset_y(water_height)
pg10 = pg9.offset_y(dam_height - water_height)
pg11 = pg10.offset_y(wall_height - dam_height)
pg12 = pg11.offset_x(wall_thickness_top)
pg13 = pg12.offset(tan(incline_rad) * (wall_height - dam_height), -(wall_height - dam_height))
pg14 = pg13.offset(tan(incline_rad) * (dam_height - water_height), -(dam_height - water_height))

sgl1 = m.Quad(pg4, pg3, pg14, pg9)
sgl2 = m.Quad(pg9, pg14, pg13, pg10)
sgl3 = m.Quad(pg10, pg13, pg12, pg11)

pg15 = pg7.offset_y(water_height)
pg16 = pg15.offset_y(dam_height - water_height)
pg17 = pg16.offset_y(wall_height - dam_height)
pg18 = pg17.offset_x(-wall_thickness_top)
pg19 = pg18.offset(-tan(incline_rad) * (wall_height - dam_height), -(wall_height - dam_height))
pg20 = pg19.offset(-tan(incline_rad) * (dam_height - water_height), -(dam_height - water_height))

sgr1 = m.Quad(pg8, pg7, pg15, pg20)
sgr2 = m.Quad(pg20, pg15, pg16, pg19)
sgr3 = m.Quad(pg19, pg16, pg17, pg18)

sgg = m.QuadGroup([sgb1, sgb2, sgb3, sgl1, sgl2, sgl3, sgr1, sgr2, sgr3])

sw = m.Quad(pg3, pg8, pg20, pg14)

sgw = m.QuadGroup([sw])

water_volume = sgw.extrude_z(water_length, before_dam_elements)
ground_before_dam_volume = sgg.extrude_z(water_length, before_dam_elements)

ground_around_dam_volume = m.Volume(geo.extrude(
    ground_before_dam_volume.get_surfaces_in_extrusion_direction(),
    0, 0, dam_thickness,
    around_dam_elements,
    recombine=True))

geo.synchronize()


dam_bottom_volume = m.Volume(geo.extrude(
    water_volume.get_surfaces_in_extrusion_direction(),
    0, 0, dam_thickness,
    around_dam_elements,
    recombine=True))

top_dam_surface = m.QuadGroup([m.Quad.from_ids([26, 30, 64, 94])])

dam_top_volume = top_dam_surface.extrude_z(dam_thickness, around_dam_elements)

ground_after_dam_volume = m.Volume(geo.extrude(
    ground_around_dam_volume.get_surfaces_in_extrusion_direction(),
    0, 0, air_length,
    after_dam_elements,
    recombine=True))

ground_extension_left_volume = m.Volume(
    geo.extrude([
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
        (2, 692)
    ], side_extension, 0, 0, extension_elements, recombine=True)
)

ground_extension_right_volume = m.Volume(
    geo.extrude([
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
    ], -side_extension, 0, 0, extension_elements, recombine=True)
)

pml_xm = m.Volume(
    geo.extrude(
        ground_extension_right_volume.get_surfaces_in_extrusion_direction(),
        -pml_thickness, 0, 0,
        [1],
        recombine=True
    ),
)

pml_xp = m.Volume(
    geo.extrude(
        ground_extension_left_volume.get_surfaces_in_extrusion_direction(),
        pml_thickness, 0, 0,
        [1],
        recombine=True
    ),
)

pml_zp = m.Volume(
    geo.extrude(
        ground_after_dam_volume.get_surfaces_in_extrusion_direction() + [
            ground_extension_left_volume.extrusion[i] for i in range(4 + 6 * 8, len(ground_extension_left_volume.extrusion), 5 + 1)
        ] + [
            ground_extension_right_volume.extrusion[i] for i in range(4 + 6 * 8, len(ground_extension_right_volume.extrusion), 5 + 1)
        ],
        0, 0, pml_thickness,
        [1],
        recombine=True
    )
)

pml_zm = m.Volume(
    geo.extrude(
        sgg.gmsh_surfaces() + [
            ground_extension_left_volume.extrusion[i] for i in range(2, 2 + 4 * 6, 5 + 1)
        ] + [
            ground_extension_right_volume.extrusion[i] for i in range(2, 2 + 4 * 6, 5 + 1)
        ],
        0, 0, -pml_thickness,
        [1],
        recombine=True
    )
)

pml_ym = m.Volume(
    geo.extrude(
        [ground_before_dam_volume.extrusion[i] for i in range(2, 2 + 2 * 6 + 1, 5 + 1)]
        + [ground_around_dam_volume.extrusion[i] for i in range(2, 2 + 2 * 6 + 1, 5 + 1)]
        + [ground_after_dam_volume.extrusion[i] for i in range(2, 2 + 2 * 6 + 1, 5 + 1)]
        + [
            ground_extension_left_volume.extrusion[5],
            ground_extension_left_volume.extrusion[29],
            ground_extension_left_volume.extrusion[53]]
        + [
            ground_extension_right_volume.extrusion[3],
            ground_extension_right_volume.extrusion[27],
            ground_extension_right_volume.extrusion[51]],
        0, -pml_thickness, 0,
        [1],
        recombine=True
    ),
)

pml_xpym = m.Volume(
    geo.extrude(
        [
            pml_ym.extrusion[58],
            pml_ym.extrusion[64],
            pml_ym.extrusion[70],
        ],
        pml_thickness, 0, 0,
        [1],
        recombine=True
    )
)

offset_pml_xmym = 12
pml_xmym = m.Volume(
    geo.extrude(
        [
            pml_ym.extrusion[i] for i in range(4 + offset_pml_xmym * 6, 4 + (offset_pml_xmym + 3) * 6, 5 + 1)
        ],
        -pml_thickness, 0, 0,
        [1],
        recombine=True
    )
)

pml_ymzm = m.Volume(
    geo.extrude(
        [
            pml_ym.extrusion[2],
            pml_ym.extrusion[8],
            pml_ym.extrusion[14],
            pml_ym.extrusion[57],
            pml_ym.extrusion[77],
        ],
        0, 0, -pml_thickness,
        [1],
        recombine=True
    )
)

pml_ymzp = m.Volume(
    geo.extrude(
        [
            pml_ym.extrusion[4 + 6 * 6],
            pml_ym.extrusion[4 + 6 * 7],
            pml_ym.extrusion[4 + 6 * 8],
            pml_ym.extrusion[3 + 6 * 14],
            pml_ym.extrusion[5 + 6 * 11],
        ],
        0, 0, pml_thickness,
        [1],
        recombine=True
    )
)

pml_water = m.Volume(
    geo.extrude(
        sgw.gmsh_surfaces(),
        0, 0, -pml_thickness,
        [1],
        recombine=True
    )
)

pml_xmymzp = m.Volume(
    geo.extrude(
        [
            (2, 2966),
        ],
        0, 0, pml_thickness,
        [1],
        recombine=True
    )
)

pml_xmzp = m.Volume(
    geo.extrude(
        [
            (2, 1422),
            (2, 1444),
            (2, 1466),
            (2, 1488),
        ],
        0, 0, pml_thickness,
        [1],
        recombine=True
    )
)

pml_xpymzp = m.Volume(
    geo.extrude(
        [
            (2, 2892),
        ],
        0, 0, pml_thickness,
        [1],
        recombine=True
    )
)

pml_xpzp = m.Volume(
    geo.extrude(
        [
            (2, 1686),
            (2, 1708),
            (2, 1730),
            (2, 1752),
        ],
        0, 0, pml_thickness,
        [1],
        recombine=True
    )
)

pml_xpzm = m.Volume(
    geo.extrude(
        [
            (2, 1502),
            (2, 1524),
            (2, 1546),
            (2, 1568),
        ],
        0, 0, -pml_thickness,
        [1],
        recombine=True
    )
)

pml_xpymzm = m.Volume(
    geo.extrude(
        [
            (2, 2856),
        ],
        0, 0, -pml_thickness,
        [1],
        recombine=True
    )
)

pml_xmymzm = m.Volume(
    geo.extrude(
        [
            (2, 2914),
        ],
        0, 0, -pml_thickness,
        [1],
        recombine=True
    )
)

pml_xmzm = m.Volume(
    geo.extrude(
        [
            (2, 1238),
            (2, 1260),
            (2, 1282),
            (2, 1304),
        ],
        0, 0, -pml_thickness,
        [1],
        recombine=True
    )
)

collection = m.PhysicalGroupCollection()

material_ground = m.Material('S', 6400, 3200, 2700)
material_water = m.Material('F', 1200, 0, 1000)
material_dam = m.Material('S', 6400, 3200, 2700)

pml = {
    'x-y-z-': (pml_xmymzm, material_ground, m.PML(
        (0, -pml_thickness),
        (0, -pml_thickness),
        (0, -pml_thickness),
        0,
    )),

    'x-y-': (pml_xmym, material_ground, m.PML(
        (0, -pml_thickness),
        (0, -pml_thickness),
        (0, 0),
        0,
    )),

    'x-z-': (pml_xmzm, material_ground, m.PML(
        (0, -pml_thickness),
        (0, 0),
        (0, -pml_thickness),
        0,
    )),

    'x-': (pml_xm, material_ground, m.PML(
        (0, -pml_thickness),
        (0, 0),
        (0, 0),
        0,
    )),

    'x+': (pml_xp, material_ground, m.PML(
        (x_upper, pml_thickness),
        (0, 0),
        (0, 0),
        0,
    )),

    'z+': (pml_zp, material_ground, m.PML(
        (0, 0),
        (0, 0),
        (z_upper, pml_thickness),
        0,
    )),

    'z-': (pml_zm, material_ground, m.PML(
        (0, 0),
        (0, 0),
        (0, -pml_thickness),
        0,
    )),

    'y-': (pml_ym, material_ground, m.PML(
        (0, 0),
        (0, -pml_thickness),
        (0, 0),
        0,
    )),

    'x+y-': (pml_xpym, material_ground, m.PML(
        (x_upper, pml_thickness),
        (0, -pml_thickness),
        (0, 0),
        0,
    )),

    'y-z-': (pml_ymzm, material_ground, m.PML(
        (0, 0),
        (0, -pml_thickness),
        (0, -pml_thickness),
        0,
    )),

    'y-z+': (pml_ymzp, material_ground, m.PML(
        (0, 0),
        (0, -pml_thickness),
        (z_upper, pml_thickness),
        0,
    )),

    'x-z+': (pml_xmzp, material_ground, m.PML(
        (0, -pml_thickness),
        (0, 0),
        (z_upper, pml_thickness),
        0,
    )),

    'x+z-': (pml_xpzm, material_ground, m.PML(
        (x_upper, pml_thickness),
        (0, 0),
        (0, -pml_thickness),
        0,
    )),

    'x+z+': (pml_xpzp, material_ground, m.PML(
        (x_upper, pml_thickness),
        (0, 0),
        (z_upper, pml_thickness),
        0,
    )),

    'x-y-z+': (pml_xmymzp, material_ground, m.PML(
        (0, -pml_thickness),
        (0, -pml_thickness),
        (z_upper, pml_thickness),
        0,
    )),

    'x+y-z+': (pml_xpymzp, material_ground, m.PML(
        (x_upper, pml_thickness),
        (0, -pml_thickness),
        (z_upper, pml_thickness),
        0,
    )),

    'x+y-z-': (pml_xpymzm, material_ground, m.PML(
        (x_upper, pml_thickness),
        (0, -pml_thickness),
        (0, -pml_thickness),
        0,
    )),

    'water': (pml_water, material_water, m.PML(
        (0, 0),
        (0, 0),
        (0, -pml_thickness),
        2,
    )),
}

m.VolumeGroup([
    ground_before_dam_volume,
    ground_around_dam_volume,
    ground_after_dam_volume,
    ground_extension_left_volume,
    ground_extension_right_volume,
]).set_phy_group(collection,
                 'Ground',
                 material_ground)

m.VolumeGroup([
    dam_top_volume,
    dam_bottom_volume,
]).set_phy_group(collection,
                 'Dam',
                 material_dam)

m.VolumeGroup([
    water_volume
]).set_phy_group(collection,
                 'Water',
                 material_water)

# Create PMLs
for direction, (volume, material, pml) in pml.items():
    m.VolumeGroup([volume]).set_pml(
        collection,
        f'PML_{direction}',
        material,
        pml,
    )

collection.write_material_input('material.input')

m.gmsh.option.setNumber("General.Verbosity", 0)
geo.synchronize()

m.gmsh.model.mesh.generate(3)

m.gmsh.option.setNumber("Mesh.MshFileVersion", 2.2)
m.gmsh.write("output.msh")

threshold = 20
bounding_box = mt.BoundingBox(wall_thickness_top, wall_thickness_top + dam_size_top,
                              ground_height, ground_height + dam_height,
                              water_length, water_length + dam_thickness,
                              threshold)

bounding_box.render(m, offset=threshold)

geo.synchronize()


def transform(x: float, y: float, z: float):
    dx, dy, dz = 0, 0, 0
    x0, y0, z0 = x - bounding_box.min_x, y - bounding_box.min_y, z - bounding_box.min_z
    qx = mt.BoundingBox.get_dampening_coefficient(x, bounding_box.min_x, bounding_box.max_x)

    dz += (bounding_box.max_y - y0) ** 2.05 / 220

    dz += (x0 - 0.5 * (bounding_box.max_x - bounding_box.min_x)) ** 2 / 500 - 50

    dz *= qx

    return x + dx, y + dy, z + dz


mt.transform_mesh_file("output.msh", [
    mt.Transformer(
        bounding_box,
        transform,
    )
], "output_transformed.msh")

m.gmsh.open("output_transformed.msh")

m.gmsh.fltk.run()

m.gmsh.finalize()

