import gmsh
import sys

gmsh.initialize(sys.argv)

gmsh.model.add("BarrageSimple")

water_height = dam_height = 100.0
dam_size = 100.0
water_length = 70.0
dam_thickness = 10.0
wall_thickness = 10.0
ground_height = 10.0
air_length = 100
model_length = water_length + dam_thickness + air_length

lc = 1

model = gmsh.model
geo = gmsh.model.geo

# Ground points
pg1 = geo.addPoint(0, 0, 0, lc)
pg2 = geo.addPoint(0, wall_thickness + dam_size + wall_thickness, 0, lc)
pg3 = geo.addPoint(0, wall_thickness + dam_size + wall_thickness, ground_height + dam_height, lc)
pg4 = pw2 = geo.addPoint(0, wall_thickness + dam_size, ground_height + dam_height, lc)
pg5 = pw1 = geo.addPoint(0, wall_thickness + dam_size, ground_height, lc)
pg6 = pw0 = geo.addPoint(0, wall_thickness, ground_height, lc)
pg7 = pw3 = geo.addPoint(0, wall_thickness, ground_height + dam_height, lc)
pg8 = geo.addPoint(0, 0, ground_height + dam_height, lc)

# Ground lines
lg1 = geo.addLine(pg1, pg2)
lg2 = geo.addLine(pg2, pg3)
lg3 = geo.addLine(pg3, pg4)
lg4 = geo.addLine(pg4, pg5)
lg5 = geo.addLine(pg5, pg6)
lg6 = geo.addLine(pg6, pg7)
lg7 = geo.addLine(pg7, pg8)
lg8 = geo.addLine(pg8, pg1)

# Water lines
lw0 = geo.addLine(pw0, pw1)
lw1 = geo.addLine(pw1, pw2)
lw2 = geo.addLine(pw2, pw3)
lw3 = geo.addLine(pw3, pw0)

# Curves
ground_curve = geo.addCurveLoop([lg1, lg2, lg3, lg4, lg5, lg6, lg7, lg8])
water_curve = geo.addCurveLoop([lw0, lw1, lw2, lw3])

# Planes
ground_plane = geo.addPlaneSurface([ground_curve])
water_plane = geo.addPlaneSurface([water_curve])

# Surface Loops
ground_surface = geo.addSurfaceLoop([ground_plane])
water_surface = geo.addSurfaceLoop([water_plane])


# Extrude
ground_volume = geo.extrude([(2, ground_surface)], model_length, 0, 0)
water_volume = geo.extrude([(2, water_surface)], water_length, 0, 0)
dam_volume = geo.extrude([water_volume[0]], dam_thickness, 0, 0)

# Physical groups
ground_phy_group = model.addPhysicalGroup(3, [ground_volume[1][1]], 1, 'Ground')
water_phy_group = model.addPhysicalGroup(3, [water_volume[1][1]], 2, 'Water')
dam_phy_group = model.addPhysicalGroup(3, [dam_volume[1][1]], 3, 'Dam')

geo.synchronize()

# gmsh.model.mesh.generate(3)

gmsh.write("barrage_simple.msh")

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()
