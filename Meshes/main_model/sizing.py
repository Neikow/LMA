from math import atan, tan

# ==========================
#  Preliminary calculations
# ==========================

# water max element size = 48m
# ground max element size = 256m
# ground min element size = 128m
# dam max element size = 256m

# f_min = 1Hz
# f_max = 25Hz

# lambda_max_ground = 6400m
# lambda_min_ground = 128m

# lambda_max_water = 1200m
# lambda_min_water = 24m

# # domain_size = ~4 * lambda_max_ground = 25600m
# # domain_size = ~2 * lambda_max_ground = 12800m

# depth = ~2 * lambda_max_ground = 12800m

# =============
#  Model sizes
# =============
dam_size_top = 300.0
dam_size_bottom = 120.0
dam_height = 90.0
dam_thickness = 15.0

wall_height = 100.0
wall_thickness = 500.0

# ground_height = 12800.0
ground_height = 2500.0

water_height = 80.0
# water_length = 12800.0
water_length = 2500.0

# air_length = 12800.0
air_length = 2500.0

# side_extension = 12800.0
side_extension = 2500.0

# pml_thickness = 12800.0
pml_thickness = 500.0

# ============
# Calculations
# ============
incline_rad = atan((dam_size_top - dam_size_bottom) / 2 / wall_height)

wall_thickness_top = wall_thickness
wall_thickness_bottom = wall_thickness + tan(incline_rad) * wall_height

x_zero = side_extension
y_zero = 0
z_zero = 0

x_upper = side_extension * 2 + dam_size_bottom + wall_thickness_bottom * 2
y_upper = 0
z_upper = water_length + dam_thickness + air_length

# ==========
# Assertions
# ==========
assert dam_size_top > dam_size_bottom
assert wall_height >= dam_height
assert dam_height > water_height
assert wall_thickness > 0
assert ground_height > 0
assert water_height > 0
