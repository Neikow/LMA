import gmsh
import sys

gmsh.initialize(sys.argv)

gmsh.model.add("BarrageSimple")

lc = 10

dam_height = 100.0
wall_height = 110.0
water_height = 90.0
dam_size = 100.0
water_length = 70.0
water_depth = 90.0
dam_thickness = 10.0
wall_thickness = 30.0
ground_height = 10.0
air_length = 100
model_length = water_length + dam_thickness + air_length


model = gmsh.model
geo = gmsh.model.geo


def get_points_from_size(dy: float, dz: float, oy: float = 0.0, oz: float = 0.0) -> [int, int, int, int]:
    return [
        geo.add_point(0, oy, oz, lc),
        geo.add_point(0, oy + dy, oz, lc),
        geo.add_point(0, oy + dy, oz + dz, lc),
        geo.add_point(0, oy, oz + dz, lc)
    ]


def get_lines_from_points(points: [int, int, int, int]) -> [int, int, int, int]:
    return [
        geo.add_line(points[0], points[1]),
        geo.add_line(points[1], points[2]),
        geo.add_line(points[2], points[3]),
        geo.add_line(points[3], points[0])
    ]


def get_curve_from_points(points: [int, int, int, int]) -> int:
    return geo.add_curve_loop(get_lines_from_points(points))


physical_groups = {}


def add_volume_to_phy_group(volumes, name: str) -> int:
    if name not in physical_groups:
        group = len(physical_groups) + 1
        physical_groups[name] = group
        model.addPhysicalGroup(3, [volume[1][1] for volume in volumes], group, name)
    else:
        group = physical_groups[name]
        model.add_physical_group(3, [volume[1][1] for volume in volumes], group)
    return group


# ground points
l_ground_points = get_points_from_size(wall_thickness, ground_height + wall_height)
c_ground_points = get_points_from_size(dam_size, ground_height, wall_thickness)
r_ground_points = get_points_from_size(wall_thickness, ground_height + wall_height, wall_thickness + dam_size)

# water points
water_points = get_points_from_size(dam_size, water_depth, wall_thickness, ground_height)

# ground surfaces
l_ground_curve = get_curve_from_points(l_ground_points)
c_ground_curve = get_curve_from_points(c_ground_points)
r_ground_curve = get_curve_from_points(r_ground_points)

# water surface
water_curve = get_curve_from_points(water_points)

# ground surfaces
r_ground_plane = geo.add_plane_surface([r_ground_curve])
c_ground_plane = geo.add_plane_surface([c_ground_curve])
l_ground_plane = geo.add_plane_surface([l_ground_curve])

# water surface
water_plane = geo.add_plane_surface([water_curve])

# transfinite curves
for i in [*get_lines_from_points(l_ground_points),
          *get_lines_from_points(c_ground_points),
          *get_lines_from_points(r_ground_points),
          *get_lines_from_points(water_points)]:
    geo.mesh.set_transfinite_curve(i, 10)

# transfinite surfaces
for i in [r_ground_plane, c_ground_plane, l_ground_plane, water_plane]:
    geo.mesh.set_transfinite_surface(i)
    gmsh.model.geo.mesh.setRecombine(2, i)

# Extrude
c_ground_volume = geo.extrude([(2, c_ground_plane)], model_length, 0, 0, [4], recombine=True)
l_ground_volume = geo.extrude([(2, l_ground_plane)], model_length, 0, 0, [4], recombine=True)
r_ground_volume = geo.extrude([(2, r_ground_plane)], model_length, 0, 0, [4], recombine=True)
water_volume = geo.extrude([(2, water_plane)], water_length, 0, 0, [4], recombine=True)
dam_under_water_volume = geo.extrude([water_volume[0]], dam_thickness, 0, 0, [4], recombine=True)
dam_above_water_volume = geo.extrude([dam_under_water_volume[4]], 0, 0, dam_height - water_depth, [4], recombine=True)

# Physical groups
ground_phy_group = add_volume_to_phy_group([l_ground_volume, c_ground_volume, r_ground_volume], 'Ground')
water_phy_group = add_volume_to_phy_group([water_volume], 'Water')
dam_phy_group = add_volume_to_phy_group([dam_under_water_volume, dam_above_water_volume], 'Dam')

geo.synchronize()

gmsh.model.mesh.generate(3)

# gmsh.write("barrage_simple2.msh")

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()
