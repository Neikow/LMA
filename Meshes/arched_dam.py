from math import tan, atan, degrees, cos, sin
from typing import List

import Meshes.main_model.gmesher as m

tr = 5

geo = m.geo
model = m.model

dam_width_bottom = 140

dam_offset_bottom_l = 2
dam_offset_bottom_r = 2
dam_offset_middle_bottom_l = 4
dam_offset_middle_bottom_r = 4
dam_offset_middle_top_l = 6
dam_offset_middle_top_r = 6
dam_offset_water_l = 8
dam_offset_water_r = 8
dam_offset_dam_top_l = 10
dam_offset_dam_top_r = 10
dam_offset_top_l = 12
dam_offset_top_r = 12

dam_thickness_bottom_l = 12
dam_thickness_middle_bottom_l = 10
dam_thickness_middle_top_l = 10
dam_thickness_water_l = 10
dam_thickness_dam_l = 10
dam_thickness_top_l = 10
dam_thickness_bottom_r = 12
dam_thickness_middle_bottom_r = 10
dam_thickness_middle_top_r = 10
dam_thickness_water_r = 10
dam_thickness_dam_r = 10
dam_thickness_top_r = 10


wall_offset_middle_bottom_l = 2
wall_offset_middle_bottom_r = 2
wall_offset_middle_top_l = 3
wall_offset_middle_top_r = 3
wall_offset_water_l = 5
wall_offset_water_r = 5
wall_offset_top_l = 7
wall_offset_top_r = 7
wall_thickness_bottom_l = 10
wall_thickness_bottom_r = 10
wall_thickness_top_l = 2
wall_thickness_top_r = 2

ground_thickness = 10

ground_after_dam_length_bottom = 100

dam_middle_bottom_height = 15
dam_middle_top_height = 20
water_height = 50
dam_height = 60
wall_height = 70
dam_thickness = 5

# TODO: calculate the offset based on the curvature
dam_curvature_center_offset = 200


def add_line(p1: int, p2: int):
    l = geo.add_line(p1, p2)
    geo.mesh.set_transfinite_curve(l, tr)
    return l


def add_circle(p1: int, c: int, p2: int):
    l = geo.add_circle_arc(p1, c, p2)
    geo.mesh.set_transfinite_curve(l, tr)
    return l


def add_surface(l1: int, l2: int, l3: int, l4: int):
    cl = geo.add_curve_loop([l1, l2, l3, l4])
    ps = geo.add_plane_surface([cl])
    geo.mesh.set_transfinite_surface(ps)
    geo.mesh.set_recombine(2, ps)
    return ps


def add_volume(surfaces: List[int]):
    sl = geo.add_surface_loop(surfaces)
    v = geo.add_volume([sl])
    geo.mesh.set_transfinite_volume(v)
    return v


p1 = geo.add_point(-0.5 * dam_width_bottom, 0, -dam_offset_bottom_l)
p2 = geo.add_point(-0.5 * dam_width_bottom, 0, ground_after_dam_length_bottom)
p3 = geo.add_point(-0.5 * dam_width_bottom - wall_thickness_bottom_l, 0, ground_after_dam_length_bottom)
p4 = geo.add_point(-0.5 * dam_width_bottom - wall_thickness_bottom_l, 0, -dam_offset_bottom_l)

p5 = geo.add_point(-0.5 * dam_width_bottom, ground_thickness, -dam_offset_bottom_l)
p6 = geo.add_point(-0.5 * dam_width_bottom, ground_thickness, ground_after_dam_length_bottom)
p7 = geo.add_point(-0.5 * dam_width_bottom - wall_thickness_bottom_l, ground_thickness, ground_after_dam_length_bottom)
p8 = geo.add_point(-0.5 * dam_width_bottom - wall_thickness_bottom_l, ground_thickness, -dam_offset_bottom_l)

l1 = add_line(p1, p2)
l2 = add_line(p2, p3)
l3 = add_line(p3, p4)
l4 = add_line(p4, p1)

l5 = add_line(p5, p6)
l6 = add_line(p6, p7)
l7 = add_line(p7, p8)
l8 = add_line(p8, p5)

l9 = add_line(p1, p5)
l10 = add_line(p2, p6)
l11 = add_line(p3, p7)
l12 = add_line(p4, p8)

ps1 = add_surface(l1, l2, l3, l4)
ps2 = add_surface(l1, l10, -l5, -l9)
ps3 = add_surface(l2, l11, -l6, -l10)
ps4 = add_surface(l3, l12, -l7, -l11)
ps5 = add_surface(l4, l9, -l8, -l12)
ps6 = add_surface(l5, l6, l7, l8)

v1 = add_volume([ps1, ps2, ps3, ps4, ps5, ps6])

p9 = geo.add_point(-0.5 * dam_width_bottom - wall_offset_middle_bottom_l, dam_middle_bottom_height, -dam_offset_middle_bottom_l)
p10 = geo.add_point(-0.5 * dam_width_bottom - wall_offset_middle_bottom_l, dam_middle_bottom_height, ground_after_dam_length_bottom)
p11 = geo.add_point(-0.5 * dam_width_bottom - wall_thickness_bottom_l, dam_middle_bottom_height, ground_after_dam_length_bottom)
p12 = geo.add_point(-0.5 * dam_width_bottom - wall_thickness_bottom_l, dam_middle_bottom_height, -dam_offset_middle_bottom_l)

l13 = add_line(p9, p10)
l14 = add_line(p10, p11)
l15 = add_line(p11, p12)
l16 = add_line(p12, p9)

l17 = add_line(p5, p9)
l18 = add_line(p6, p10)
l19 = add_line(p7, p11)
l20 = add_line(p8, p12)

ps7 = add_surface(l5, l18, -l13, -l17)
ps8 = add_surface(l6, l19, -l14, -l18)
ps9 = add_surface(l7, l20, -l15, -l19)
ps10 = add_surface(l8, l17, -l16, -l20)
ps11 = add_surface(l13, l14, l15, l16)

v2 = add_volume([ps6, ps7, ps8, ps9, ps10, ps11])

p13 = geo.add_point(-0.5 * dam_width_bottom - wall_offset_middle_top_l, dam_middle_top_height, -dam_offset_middle_top_l)
p14 = geo.add_point(-0.5 * dam_width_bottom - wall_offset_middle_top_l, dam_middle_top_height, ground_after_dam_length_bottom)
p15 = geo.add_point(-0.5 * dam_width_bottom - wall_thickness_bottom_l, dam_middle_top_height, ground_after_dam_length_bottom)
p16 = geo.add_point(-0.5 * dam_width_bottom - wall_thickness_bottom_l, dam_middle_top_height, -dam_offset_middle_top_l)

l21 = add_line(p13, p14)
l22 = add_line(p14, p15)
l23 = add_line(p15, p16)
l24 = add_line(p16, p13)

l25 = add_line(p9, p13)
l26 = add_line(p10, p14)
l27 = add_line(p11, p15)
l28 = add_line(p12, p16)

ps12 = add_surface(l13, l26, -l21, -l25)
ps13 = add_surface(l14, l27, -l22, -l26)
ps14 = add_surface(l15, l28, -l23, -l27)
ps15 = add_surface(l16, l25, -l24, -l28)
ps16 = add_surface(l21, l22, l23, l24)

v3 = add_volume([ps11, ps12, ps13, ps14, ps15, ps16])

p17 = geo.add_point(-0.5 * dam_width_bottom - wall_offset_water_l, water_height, -dam_offset_water_l)
p18 = geo.add_point(-0.5 * dam_width_bottom - wall_offset_water_l, water_height, ground_after_dam_length_bottom)
p19 = geo.add_point(-0.5 * dam_width_bottom - wall_thickness_bottom_l, water_height, ground_after_dam_length_bottom)
p20 = geo.add_point(-0.5 * dam_width_bottom - wall_thickness_bottom_l, water_height, -dam_offset_water_l)

l29 = add_line(p17, p18)
l30 = add_line(p18, p19)
l31 = add_line(p19, p20)
l32 = add_line(p20, p17)

l33 = add_line(p13, p17)
l34 = add_line(p14, p18)
l35 = add_line(p15, p19)
l36 = add_line(p16, p20)

ps17 = add_surface(l21, l34, -l29, -l33)
ps18 = add_surface(l22, l35, -l30, -l34)
ps19 = add_surface(l23, l36, -l31, -l35)
ps20 = add_surface(l24, l33, -l32, -l36)
ps21 = add_surface(l29, l30, l31, l32)

v4 = add_volume([ps16, ps17, ps18, ps19, ps20, ps21])

p21 = geo.add_point(-0.5 * dam_width_bottom - wall_offset_top_l, dam_height, -dam_offset_dam_top_l)
p22 = geo.add_point(-0.5 * dam_width_bottom - wall_offset_top_l, dam_height, ground_after_dam_length_bottom)
p23 = geo.add_point(-0.5 * dam_width_bottom - wall_thickness_bottom_l, dam_height, ground_after_dam_length_bottom)
p24 = geo.add_point(-0.5 * dam_width_bottom - wall_thickness_bottom_l, dam_height, -dam_offset_dam_top_l)

l37 = add_line(p21, p22)
l38 = add_line(p22, p23)
l39 = add_line(p23, p24)
l40 = add_line(p24, p21)

l41 = add_line(p17, p21)
l42 = add_line(p18, p22)
l43 = add_line(p19, p23)
l44 = add_line(p20, p24)

ps22 = add_surface(l29, l42, -l37, -l41)
ps23 = add_surface(l30, l43, -l38, -l42)
ps24 = add_surface(l31, l44, -l39, -l43)
ps25 = add_surface(l32, l41, -l40, -l44)
ps26 = add_surface(l37, l38, l39, l40)

v5 = add_volume([ps21, ps22, ps23, ps24, ps25, ps26])

p25 = geo.add_point(-0.5 * dam_width_bottom - wall_thickness_bottom_l + wall_thickness_top_l, wall_height, -dam_offset_top_l)
p26 = geo.add_point(-0.5 * dam_width_bottom - wall_thickness_bottom_l + wall_thickness_top_l, wall_height, ground_after_dam_length_bottom)
p27 = geo.add_point(-0.5 * dam_width_bottom - wall_thickness_bottom_l, wall_height, ground_after_dam_length_bottom)
p28 = geo.add_point(-0.5 * dam_width_bottom - wall_thickness_bottom_l, wall_height, -dam_offset_top_l)

l45 = add_line(p25, p26)
l46 = add_line(p26, p27)
l47 = add_line(p27, p28)
l48 = add_line(p28, p25)

l49 = add_line(p21, p25)
l50 = add_line(p22, p26)
l51 = add_line(p23, p27)
l52 = add_line(p24, p28)

ps27 = add_surface(l37, l50, -l45, -l49)
ps28 = add_surface(l38, l51, -l46, -l50)
ps29 = add_surface(l39, l52, -l47, -l51)
ps30 = add_surface(l40, l49, -l48, -l52)
ps31 = add_surface(l45, l46, l47, l48)

v6 = add_volume([ps26, ps27, ps28, ps29, ps30, ps31])

p29 = geo.add_point(0.5 * dam_width_bottom + wall_thickness_bottom_r, 0, -dam_offset_bottom_r)
p30 = geo.add_point(0.5 * dam_width_bottom + wall_thickness_bottom_r, 0, ground_after_dam_length_bottom)
p31 = geo.add_point(0.5 * dam_width_bottom, 0, ground_after_dam_length_bottom)
p32 = geo.add_point(0.5 * dam_width_bottom, 0, -dam_offset_bottom_r)

p33 = geo.add_point(0.5 * dam_width_bottom + wall_thickness_bottom_r, ground_thickness, -dam_offset_bottom_r)
p34 = geo.add_point(0.5 * dam_width_bottom + wall_thickness_bottom_r, ground_thickness, ground_after_dam_length_bottom)
p35 = geo.add_point(0.5 * dam_width_bottom, ground_thickness, ground_after_dam_length_bottom)
p36 = geo.add_point(0.5 * dam_width_bottom, ground_thickness, -dam_offset_bottom_r)

l53 = add_line(p29, p30)
l54 = add_line(p30, p31)
l55 = add_line(p31, p32)
l56 = add_line(p32, p29)

l57 = add_line(p33, p34)
l58 = add_line(p34, p35)
l59 = add_line(p35, p36)
l60 = add_line(p36, p33)

l61 = add_line(p29, p33)
l62 = add_line(p30, p34)
l63 = add_line(p31, p35)
l64 = add_line(p32, p36)

ps32 = add_surface(l53, l54, l55, l56)
ps33 = add_surface(l53, l62, -l61, -l57)
ps34 = add_surface(l54, l63, -l62, -l58)
ps35 = add_surface(l55, l64, -l63, -l59)
ps36 = add_surface(l56, l61, -l64, -l60)
ps37 = add_surface(l57, l58, l59, l60)

v7 = add_volume([ps32, ps33, ps34, ps35, ps36, ps37])

p37 = geo.add_point(0.5 * dam_width_bottom + wall_thickness_bottom_r, dam_middle_bottom_height, -dam_offset_middle_bottom_r)
p38 = geo.add_point(0.5 * dam_width_bottom + wall_thickness_bottom_r, dam_middle_bottom_height, ground_after_dam_length_bottom)
p39 = geo.add_point(0.5 * dam_width_bottom + wall_offset_middle_bottom_r, dam_middle_bottom_height, ground_after_dam_length_bottom)
p40 = geo.add_point(0.5 * dam_width_bottom + wall_offset_middle_bottom_r, dam_middle_bottom_height, -dam_offset_middle_bottom_r)

l65 = add_line(p37, p38)
l66 = add_line(p38, p39)
l67 = add_line(p39, p40)
l68 = add_line(p40, p37)

l69 = add_line(p33, p37)
l70 = add_line(p34, p38)
l71 = add_line(p35, p39)
l72 = add_line(p36, p40)

ps38 = add_surface(l57, l70, -l65, -l69)
ps39 = add_surface(l58, l71, -l66, -l70)
ps40 = add_surface(l59, l72, -l67, -l71)
ps41 = add_surface(l60, l69, -l68, -l72)
ps42 = add_surface(l65, l66, l67, l68)

v8 = add_volume([ps37, ps38, ps39, ps40, ps41, ps42])

p41 = geo.add_point(0.5 * dam_width_bottom + wall_thickness_bottom_r, dam_middle_top_height, -dam_offset_middle_top_r)
p42 = geo.add_point(0.5 * dam_width_bottom + wall_thickness_bottom_r, dam_middle_top_height, ground_after_dam_length_bottom)
p43 = geo.add_point(0.5 * dam_width_bottom + wall_offset_middle_top_r, dam_middle_top_height, ground_after_dam_length_bottom)
p44 = geo.add_point(0.5 * dam_width_bottom + wall_offset_middle_top_r, dam_middle_top_height, -dam_offset_middle_top_r)

l73 = add_line(p41, p42)
l74 = add_line(p42, p43)
l75 = add_line(p43, p44)
l76 = add_line(p44, p41)

l77 = add_line(p37, p41)
l78 = add_line(p38, p42)
l79 = add_line(p39, p43)
l80 = add_line(p40, p44)

ps43 = add_surface(l65, l78, -l73, -l77)
ps44 = add_surface(l66, l79, -l74, -l78)
ps45 = add_surface(l67, l80, -l75, -l79)
ps46 = add_surface(l68, l77, -l76, -l80)
ps47 = add_surface(l73, l74, l75, l76)

v9 = add_volume([ps42, ps43, ps44, ps45, ps46, ps47])

p45 = geo.add_point(0.5 * dam_width_bottom + wall_thickness_bottom_r, water_height, -dam_offset_water_r)
p46 = geo.add_point(0.5 * dam_width_bottom + wall_thickness_bottom_r, water_height, ground_after_dam_length_bottom)
p47 = geo.add_point(0.5 * dam_width_bottom + wall_offset_water_r, water_height, ground_after_dam_length_bottom)
p48 = geo.add_point(0.5 * dam_width_bottom + wall_offset_water_r, water_height, -dam_offset_water_r)

l81 = add_line(p45, p46)
l82 = add_line(p46, p47)
l83 = add_line(p47, p48)
l84 = add_line(p48, p45)

l85 = add_line(p41, p45)
l86 = add_line(p42, p46)
l87 = add_line(p43, p47)
l88 = add_line(p44, p48)

ps48 = add_surface(l73, l86, -l81, -l85)
ps49 = add_surface(l74, l87, -l82, -l86)
ps50 = add_surface(l75, l88, -l83, -l87)
ps51 = add_surface(l76, l85, -l84, -l88)
ps52 = add_surface(l81, l82, l83, l84)

v10 = add_volume([ps47, ps48, ps49, ps50, ps51, ps52])

p49 = geo.add_point(0.5 * dam_width_bottom + wall_thickness_bottom_r, dam_height, -dam_offset_dam_top_r)
p50 = geo.add_point(0.5 * dam_width_bottom + wall_thickness_bottom_r, dam_height, ground_after_dam_length_bottom)
p51 = geo.add_point(0.5 * dam_width_bottom + wall_offset_top_r, dam_height, ground_after_dam_length_bottom)
p52 = geo.add_point(0.5 * dam_width_bottom + wall_offset_top_r, dam_height, -dam_offset_dam_top_r)

l89 = add_line(p49, p50)
l90 = add_line(p50, p51)
l91 = add_line(p51, p52)
l92 = add_line(p52, p49)

l93 = add_line(p45, p49)
l94 = add_line(p46, p50)
l95 = add_line(p47, p51)
l96 = add_line(p48, p52)

ps53 = add_surface(l81, l94, -l89, -l93)
ps54 = add_surface(l82, l95, -l90, -l94)
ps55 = add_surface(l83, l96, -l91, -l95)
ps56 = add_surface(l84, l93, -l92, -l96)
ps57 = add_surface(l89, l90, l91, l92)

v11 = add_volume([ps52, ps53, ps54, ps55, ps56, ps57])

p53 = geo.add_point(0.5 * dam_width_bottom + wall_thickness_bottom_r, wall_height, -dam_offset_top_r)
p54 = geo.add_point(0.5 * dam_width_bottom + wall_thickness_bottom_r, wall_height, ground_after_dam_length_bottom)
p55 = geo.add_point(0.5 * dam_width_bottom + wall_thickness_bottom_r - wall_thickness_top_r, wall_height, ground_after_dam_length_bottom)
p56 = geo.add_point(0.5 * dam_width_bottom + wall_thickness_bottom_r - wall_thickness_top_r, wall_height, -dam_offset_top_r)

l97 = add_line(p53, p54)
l98 = add_line(p54, p55)
l99 = add_line(p55, p56)
l100 = add_line(p56, p53)

l101 = add_line(p49, p53)
l102 = add_line(p50, p54)
l103 = add_line(p51, p55)
l104 = add_line(p52, p56)

ps58 = add_surface(l89, l102, -l97, -l101)
ps59 = add_surface(l90, l103, -l98, -l102)
ps60 = add_surface(l91, l104, -l99, -l103)
ps61 = add_surface(l92, l101, -l100, -l104)
ps62 = add_surface(l97, l98, l99, l100)

v12 = add_volume([ps57, ps58, ps59, ps60, ps61, ps62])

p57 = geo.add_point(0, 0, dam_curvature_center_offset)
p58 = geo.add_point(0, ground_thickness, dam_curvature_center_offset)

l105 = add_circle(p1, p57, p32)
l106 = add_circle(p5, p58, p36)
l107 = add_line(p2, p31)
l108 = add_line(p6, p35)

ps63 = add_surface(-l1, l105, -l55, -l107)
ps64 = add_surface(l105, -l9, -l106, l64)
ps65 = add_surface(-l107, l10, l108, -l63)
ps66 = add_surface(l5, -l106, l59, l108)

v13 = add_volume([ps2, ps35, ps63, ps64, ps65, ps66])

p59 = geo.add_point(-0.5 * dam_width_bottom, 0, -dam_thickness_bottom_l)
p60 = geo.add_point(-(0.5 * dam_width_bottom + wall_thickness_bottom_l), 0, -dam_thickness_bottom_l)
p61 = geo.add_point(-(0.5 * dam_width_bottom + wall_thickness_bottom_l), ground_thickness, -dam_thickness_bottom_l)
p62 = geo.add_point(-0.5 * dam_width_bottom, ground_thickness, -dam_thickness_bottom_l)

l109 = add_line(p1, p59)
l110 = add_line(p4, p60)
l111 = add_line(p59, p60)
l112 = add_line(p59, p62)
l113 = add_line(p60, p61)
l114 = add_line(p5, p62)
l115 = add_line(p62, p61)
l116 = add_line(p8, p61)

ps67 = add_surface(-l4, l110, -l111, -l109)
ps68 = add_surface(l110, -l12, -l116, l113)
ps69 = add_surface(l111, -l112, -l115, l113)
ps70 = add_surface(l109, -l9, -l114, l112)
ps71 = add_surface(-l8, l116, -l115, -l114)

v14 = add_volume([ps5, ps67, ps68, ps69, ps70, ps71])

p63 = geo.add_point(-(0.5 * dam_width_bottom + wall_offset_middle_bottom_l), dam_middle_bottom_height, -dam_offset_middle_bottom_l - dam_thickness_middle_bottom_l)
p64 = geo.add_point(-(0.5 * dam_width_bottom + wall_thickness_bottom_l), dam_middle_bottom_height, -dam_offset_middle_bottom_l - dam_thickness_middle_bottom_l)

l117 = add_line(p62, p63)
l118 = add_line(p61, p64)
l119 = add_line(p12, p64)
l120 = add_line(p64, p63)
l121 = add_line(p63, p9)

ps72 = add_surface(-l114, l17, -l121, -l117)
ps73 = add_surface(l117, -l120, -l118, -l115)
ps74 = add_surface(l20, l119, -l118, -l116)
ps75 = add_surface(-l16, l119, l120, l121)

v15 = add_volume([ps10, ps71, ps72, ps73, ps74, ps75])

p65 = geo.add_point(-(0.5 * dam_width_bottom + wall_offset_middle_top_l), dam_middle_top_height, - dam_offset_middle_top_l - dam_thickness_middle_top_l)
p66 = geo.add_point(-(0.5 * dam_width_bottom + wall_thickness_bottom_l), dam_middle_top_height, -dam_offset_middle_top_l - dam_thickness_middle_top_l)

l122 = add_line(p63, p65)
l123 = add_line(p65, p13)
l124 = add_line(p64, p66)
l125 = add_line(p65, p66)
l126 = add_line(p66, p16)

ps76 = add_surface(l121, l25, -l123, -l122)
ps77 = add_surface(l120, l122, l125, -l124)
ps78 = add_surface(l28, -l126, -l124, -l119)
ps79 = add_surface(l123, -l24, -l126, -l125)

v16 = add_volume([ps15, ps75, ps76, ps77, ps78, ps79])

p67 = geo.add_point(-(0.5 * dam_width_bottom + wall_offset_water_l), water_height, -dam_offset_water_l - dam_thickness_water_l)
p68 = geo.add_point(-(0.5 * dam_width_bottom + wall_thickness_bottom_l), water_height, -dam_offset_water_l - dam_thickness_water_l)

l127 = add_line(p65, p67)
l128 = add_line(p66, p68)
l129 = add_line(p17, p67)
l130 = add_line(p67, p68)
l131 = add_line(p68, p20)

ps80 = add_surface(l33, l129, -l127, l123)
ps81 = add_surface(-l125, l127, l130, -l128)
ps82 = add_surface(l126, l36, -l131, -l128)
ps83 = add_surface(l32, l131, l130, l129)

v17 = add_volume([ps20, ps79, ps80, ps81, ps82, ps83])

p69 = geo.add_point(-0.5 * dam_width_bottom - wall_offset_top_l, dam_height, -dam_offset_dam_top_l - dam_thickness_dam_l)
p70 = geo.add_point(-(0.5 * dam_width_bottom + wall_thickness_bottom_l), dam_height, -dam_offset_dam_top_l - dam_thickness_dam_l)

l132 = add_line(p67, p69)
l133 = add_line(p68, p70)
l134 = add_line(p21, p69)
l135 = add_line(p69, p70)
l136 = add_line(p70, p24)

ps84 = add_surface(-l129, l41, l134, -l132)
ps85 = add_surface(-l130, l132, l135, -l133)
ps86 = add_surface(l131, l44, -l136, -l133)
ps87 = add_surface(l134, l40, l136, l135)

v18 = add_volume([ps25, ps83, ps84, ps85, ps86, ps87])

p71 = geo.add_point(-0.5 * dam_width_bottom - wall_thickness_bottom_l + wall_thickness_top_l, wall_height, -dam_offset_top_l - dam_thickness_top_l)
p72 = geo.add_point(-0.5 * dam_width_bottom - wall_thickness_bottom_l, wall_height, -dam_offset_top_l - dam_thickness_top_l)

l137 = add_line(p69, p71)
l138 = add_line(p70, p72)
l139 = add_line(p25, p71)
l140 = add_line(p71, p72)
l141 = add_line(p72, p28)

ps88 = add_surface(-l134, l49, l139, -l137)
ps89 = add_surface(-l135, l137, l140, -l138)
ps90 = add_surface(l52, -l141, -l138, l136)
ps91 = add_surface(l48, l141, l140, l139)

v19 = add_volume([ps30, ps87, ps88, ps89, ps90, ps91])

p73 = geo.add_point(0.5 * dam_width_bottom, 0, -dam_thickness_bottom_r)
p74 = geo.add_point((0.5 * dam_width_bottom + wall_thickness_bottom_r), 0, -dam_thickness_bottom_r)
p75 = geo.add_point((0.5 * dam_width_bottom + wall_thickness_bottom_r), ground_thickness, -dam_thickness_bottom_r)
p76 = geo.add_point(0.5 * dam_width_bottom, ground_thickness, -dam_thickness_bottom_r)

l142 = add_line(p32, p73)
l143 = add_line(p73, p74)
l144 = add_line(p74, p29)

l145 = add_line(p74, p75)
l146 = add_line(p73, p76)


geo.synchronize()



m.gmsh.model.mesh.generate(3)

m.gmsh.fltk.run()

m.gmsh.finalize()
