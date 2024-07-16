import gmesher as gm

geo = gm.geo
model = gm.model
gmsh = gm.gmsh

p1 = gm.Point(0, 0, 0)
p2 = gm.Point(1, 0, 0)
p3 = gm.Point(1, 1, 0)
p4 = gm.Point(0, 1, 0)

p5 = gm.Point(0, 0, 1)
p6 = gm.Point(1, 0, 1)
p7 = gm.Point(1, 1, 1)
p8 = gm.Point(0, 1, 1)

q1 = gm.Quad(p1, p2, p3, p4)
q2 = gm.Quad(p5, p6, p7, p8)
q3 = gm.Quad(p1, p2, p6, p5)
q4 = gm.Quad(p2, p3, p7, p6)
q5 = gm.Quad(p3, p4, p8, p7)
q6 = gm.Quad(p4, p1, p5, p8)

geo.synchronize()

gmsh.write("output.msh")

gmsh.fltk.run()

gmsh.finalize()
