from Meshes.topology import Topology
import Meshes.gmesher as m

topo = Topology("./topo.msh")
boundaries = topo.get_boundaries()

# print(topo.get_height(10, 10))

m.gmsh.open("./topo.msh")


m.geo.synchronize()

m.gmsh.fltk.run()

m.gmsh.finalize()
