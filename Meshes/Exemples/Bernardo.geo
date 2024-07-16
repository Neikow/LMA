//geometry

PML=0.25;

L =  0.500; //m
C = 1.500;  //m
T = 7e-3; //m

D = 7e-3;
D = 8e-3;
D = 9e-3;
D = 11e-3;

d = 7e-3;
// mesh

lc = 2.5e-3;

NelPML = 15;

espel= 1;


Nell = 80; //elementos em x em cada metade
NelYRef = 3;
NelXRef = 3;
NelC = 60; //elementos em z


Point(1) = {-C/2 , 0.  , -PML, lc};
Point(2) = { C/2 , 0.  , -PML, lc};
Point(3) = { C/2 , T   , -PML, lc};
Point(4) = {-D/2 , T   , -PML, lc};
Point(5) = {-D/2 , 2*T , -PML, lc};
Point(6) = { D/2 , 2*T , -PML, lc};
Point(7) = { D/2 , T   , -PML, lc};
Point(8) = {-C/2 , T   , -PML, lc};

Point(9) = {-D/2 , 0   , -PML, lc};
Point(10) = {D/2 , 0   , -PML, lc};
//PML
Point(21) = {-C/2-PML , 0   , -PML, lc};
Point(22) = {-C/2-PML , T   , -PML, lc};

Point(23) = {C/2+PML , 0   , -PML, lc};
Point(24) = {C/2+PML , T   , -PML, lc};

Line(1) = {1, 9};
Line(2) = {9, 4};
Line(3) = {4, 8};
Line(4) = {8, 1};

Curve Loop(1) = {1, 2, 3, 4};
Plane Surface(1) = {1};
Transfinite Surface {1};

Line(5) = {9, 10};
Line(6) = {10, 7};
Line(7) = {7, 4};

Curve Loop(2) = {5, 6, 7, -2};
Plane Surface(2) = {2};
Transfinite Surface {2};

Line(8) = {10, 2};
Line(9) = {2, 3};
Line(10) = {3, 7};

Curve Loop(3) = {8, 9, 10, -6};
Plane Surface(3) = {3};
Transfinite Surface {3};


Line(11) = {7, 6};
Line(12) = {6, 5};
Line(13) = {5, 4};

Curve Loop(4) = {11, 12, 13, -7};
Plane Surface(4) = {4};
Transfinite Surface {4};

Line(27) = {21, 1};
Line(28) = {8, 22};
Line(29) = {22, 21};
Curve Loop(5) = {27, -4, 28, 29};
Plane Surface(5) = {5};
Transfinite Surface {5};


Line(30) = {2, 23};
Line(31) = {23, 24};
Line(32) = {24, 3};
Curve Loop(6) = {30, 31, 32, -9};
Plane Surface(6) = {6};
Transfinite Surface {6};


Transfinite Line {4, 2, 6,9,29,31} = espel;
Transfinite Line {3,1,8,10} = Nell;

Transfinite Line {13,11} = NelYRef;
Transfinite Line {12,7,5} = NelXRef;

Transfinite Line {30,32,28,27} = NelPML+1;

Recombine Surface "*";


Point(11) = {-C/2 , 0.  , L, lc};
Point(12) = { C/2 , 0.  , L, lc};
Point(13) = { C/2 , T   , L, lc};
Point(14) = {-d/2 , T   , L, lc};
Point(15) = {-d/2 , 2*T , L, lc};
Point(16) = { d/2 , 2*T , L, lc};
Point(17) = { d/2 , T   , L, lc};
Point(18) = {-C/2 , T   , L, lc};

Point(19) = {-d/2 , 0   , L, lc};
Point(20) = {d/2 , 0   , L, lc};

//PML
Point(25) = {-C/2-PML , 0   , L, lc};
Point(26) = {-C/2-PML , T   , L, lc};

Point(27) = {C/2+PML , 0   , L, lc};
Point(28) = {C/2+PML , T   , L, lc};


Line(14) = {11, 19};
Line(15) = {19, 14};
Line(16) = {14, 18};
Line(17) = {18, 11};

Curve Loop(7) = {14, 15, 16, 17};
Plane Surface(7) = {7};
Transfinite Surface {7};

Line(18) = {19, 20};
Line(19) = {20, 17};
Line(20) = {17, 14};

Curve Loop(8) = {18, 19, 20, -15};
Plane Surface(8) = {8};
Transfinite Surface {8};

Line(21) = {20, 12};
Line(22) = {12, 13};
Line(23) = {13, 17};

Curve Loop(9) = {21, 22, 23, -19};
Plane Surface(9) = {9};
Transfinite Surface {9};

Line(24) = {17, 16};
Line(25) = {16, 15};
Line(26) = {15, 14};

Curve Loop(10) = {24, 25, 26, -20};
Plane Surface(10) = {10};
Transfinite Surface {10};


Line(33) = {25, 11};
Line(34) = {18, 26};
Line(35) = {26, 25};
Curve Loop(11) = {33, -17, 34, 35};
Plane Surface(11) = {11};
Transfinite Surface {11};


Line(36) = {12, 27};
Line(37) = {27, 28};
Line(38) = {28, 13};
Curve Loop(12) = {36, 37, 38, -22};
Plane Surface(12) = {12};
Transfinite Surface {12};

Transfinite Line {17, 15, 19,22,37,35} = espel;
Transfinite Line {16,14,23,21} = Nell;

Transfinite Line {26,24} = NelYRef;
Transfinite Line {25,20,18} = NelXRef;;


Transfinite Line {33,34,36,38} = NelPML+1;

Recombine Surface "*";

Extrude {0,0,PML}{Surface{1,2,3,4,5,6}; Layers{NelPML}; Recombine;};
Extrude {0,0,PML}{Surface{7,8,9,10,11,12}; Layers{NelPML}; Recombine;};

Line(1000) = {27,68};
Line(1001) = {28,72};

Line(1002) = {13,50};
Line(1003) = {12,46};

Line(1004) = {20,40};
Line(1005) = {17,44};
Line(1006) = {16,52};

Line(1007) = {19,30};
Line(1008) = {14,34};
Line(1009) = {15,56};

Line(1010) = {11,29};
Line(1011) = {18,38};

Line(1012) = {25,57};
Line(1013) = {26,66};


//surfaces... :'(
// 1
Curve Loop(1000) = {1000, 151, -1001, -37};
Plane Surface(1000) = {1000};
Transfinite Surface {1000};

Curve Loop(1001) = {1001,152,-1002,-38};
Plane Surface(1001) = {1001};
Transfinite Surface {1001};

Curve Loop(1002) = {1002, -85, -1003, 22};
Plane Surface(1002) = {1002};
Transfinite Surface {1002};

Curve Loop(1003) = {1003, 150, -1000, -36};
Plane Surface(1003) = {1003};
Transfinite Surface {1003};

Curve Loop(1004) = {150, 151, 152,-85};
Plane Surface(1004) = {1004};
Transfinite Surface {1004};

Surface Loop(1000) = {1000,1001,1004,1003,1002,12};
Volume(13) = {1000};
Transfinite Volume{13}  = {46,68,72,50,12,27,28,13};

Transfinite Line {85,151,63,41,43,131} = espel;
Transfinite Line {152,150,128,130} = NelPML+1;


// 2
n= 1005;
Curve Loop(n) = {1002,86,-1005,-23};
Plane Surface(n) = {n};
Transfinite Surface {n};
n= n+1;
Curve Loop(n) = {1005,-63,-1004,19};
Plane Surface(n) = {n};
Transfinite Surface {n};
n= n+1;
Curve Loop(n) = {1003,-84,-1004,21};
Plane Surface(n) = {n};
Transfinite Surface {n};
n= n+1;
Curve Loop(n) = {85,86,-63,84};
Plane Surface(n) = {n};
Transfinite Surface {n};

Surface Loop(1001) = {1005,1006,1007,1008,1002,9};
Volume(14) = {1001};
Transfinite Volume{14}  = {40,46,50,44,20,12,13,17};

Transfinite Line {152,150} = NelPML+1;
Transfinite Line {86,84,42,40} = Nell;

//3
n= 1009;
Curve Loop(n) = {1005,64,-1008,-20};
Plane Surface(n) = {n};
Transfinite Surface {n};
n= n+1;
Curve Loop(n) = {1008,-41,-1007,15};
Plane Surface(n) = {n};
Transfinite Surface {n};
n= n+1;
Curve Loop(n) = {1004,-62,-1007, 18};
Plane Surface(n) = {n};
Transfinite Surface {n};
n= n+1;
Curve Loop(n) = {62,63,64,-41};
Plane Surface(n) = {n};
Transfinite Surface {n};

Surface Loop(1002) = {8,1009,1010,1011,1012,1006};
Volume(15) = {1002};
Transfinite Volume{15}  = {30,40,44,34,19,20,17,14};


//4
n= 1013;
Curve Loop(n) = {1005,106,-1006,-24};
Plane Surface(n) = {n};
Transfinite Surface {n};
n= n+1;
Curve Loop(n) = {1006,107,-1009,-25};
Plane Surface(n) = {n};
Transfinite Surface {n};
n= n+1;
Curve Loop(n) = {1009,108,-1008,-26};
Plane Surface(n) = {n};
Transfinite Surface {n};
n= n+1;
Curve Loop(n) = {107,108,-64,106};
Plane Surface(n) = {n};
Transfinite Surface {n};

Surface Loop(1003) = {1009,10,1013,1014,1015,1016};
Volume(16) = {1003};
Transfinite Volume{16}  = {34,44,52,56,14,17,16,15};


//5
n= 1017;
Curve Loop(n) = {1008,42,-1011,-16};
Plane Surface(n) = {n};
Transfinite Surface {n};
n= n+1;
Curve Loop(n) = {1011,43,-1010,-17};
Plane Surface(n) = {n};
Transfinite Surface {n};
n= n+1;
Curve Loop(n) = {1010,40,-1007,-14};
Plane Surface(n) = {n};
Transfinite Surface {n};
n= n+1;
Curve Loop(n) = {40,41,42,43};
Plane Surface(n) = {n};
Transfinite Surface {n};

Surface Loop(1004) = {1010,1017,1018,1019,1020,7};
Volume(17) = {1004};
Transfinite Volume{17}  = {29,30,34,38,11,19,14,18};


//6
n= 1021;
Curve Loop(n) = {1011,130,-1013,-34};
Plane Surface(n) = {n};
Transfinite Surface {n};
n= n+1;
Curve Loop(n) = {1013,131,-1012,-35};
Plane Surface(n) = {n};
Transfinite Surface {n};
n= n+1;
Curve Loop(n) = {1010,-128,-1012,33};
Plane Surface(n) = {n};
Transfinite Surface {n};
n= n+1;
Curve Loop(n) = {128,-43,130,131};
Plane Surface(n) = {n};
Transfinite Surface {n};

Surface Loop(1005) = {1021,1022,1023,1024,1018,11};
Volume(18) = {1005};
Transfinite Volume{18}  = {57,29,38,66,25,11,18,26};





Transfinite Line {1000,1001,1002,1003,1004,1005} = NelC;
Transfinite Line {1006,1007,1008,1009,1010,1011} = NelC;
Transfinite Line {1012,1013} = NelC;

Recombine Surface "*";
Recombine Volume "*";

// material
Physical Volume ( 1 ) = {14,15,16,17};

//Z-x-
Physical Volume ( 2 ) = {5};

//Z-
Physical Volume ( 3 ) = {1,2,3,4};

//Z-x-
Physical Volume ( 4 ) = {6};

//x+
Physical Volume ( 5 ) = {13};

//Z+x+
Physical Volume ( 6 ) = {12};

//Z-
Physical Volume ( 7 ) = {7,8,9,10};

//Z+x-
Physical Volume ( 8 ) = {11};

//x-
Physical Volume ( 9 ) = {18};

/*
ii=1;
For(1:18)

Physical Volume ( ii ) = {ii};
ii=ii+1;
EndFor
*/

Mesh.Algorithm = 8;//delquad
Mesh.Algorithm3D=6;//Frontal Hex
//Mesh.CharacteristicLengthFactor = 10;//Factor applied to all mesh element sizes
Mesh.RecombineAll = 1;//Apply recombination algorithm to all surfaces, ignoring per-surface spec
Mesh.Recombine3DAll = 1;//Apply recombination3D algorithm to all volumes, ignoring per-volume spec
//Mesh.SubdivisionAlgorithm = 2;//Mesh subdivision algorithm (0=none, 1=all quadrangles, 2=all hexahedra)
//Mesh.Smoothing = 20;//Number of smoothing steps applied to the final mesh
//Mesh.SaveAll = 0;//Ignore Physical definitions and save all elements
//Mesh.CharacteristicLengthExtendFromBoundary = 0;
Mesh.ElementOrder = 1;//linear

Mesh 3;
