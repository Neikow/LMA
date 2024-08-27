from math import sqrt

from gmesher import Material

# =========================
#  Dam concrete properties
# =========================

Ed = 34e9  # Dynamic Elastic Modulus (Pa)
nu = 0.2  # Poisson's ratio (/)
rho_dam = 2370  # Density (kg/m^3)

vp_dam = sqrt((Ed * (1 - nu)) / (rho_dam * (1 + nu) * (1 - 2 * nu)))
vs_dam = sqrt(Ed / (2 * rho_dam * (1 + nu)))

# ===================
#  Ground properties
# ===================

vp_ground = 6000  # m/s (Average for the south-east of Europe)
vs_ground = 3400  # m/s (Average for the south-east of Europe)
rho_ground = 2650  # kg/m^3 (Average for the south-east of Europe)

# ==================
#  Water properties
# ==================

vp_water = 1400  # m/s (0°C 1atm)
vs_water = 0  # m/s
rho_water = 1000  # kg/m^3 (0°C 1atm)

# =====================
#  Material Definition
# =====================

material_ground = Material("S", vp_ground, vs_ground, rho_ground)
material_water = Material("F", vp_water, vs_water, rho_water)
material_dam = Material("S", vp_dam, vs_dam, rho_dam)
