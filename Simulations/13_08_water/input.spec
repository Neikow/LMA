# -*- mode: perl -*-
run_name = "13_08_water";

# duration of the run
sim_time = 5.0000;
mesh_file = "mesh4spec"; # input mesh file
mat_file = "material.input";
dim=3;
mpml_atn_param = 0.002;

snapshots {
    save_snap = true;
    snap_interval = 0.05;
    
    deselect all;
select box = -21.0 2299.0 -21.0 7301.0 2701.0 4986.0;
select box = 7279.0 -21.0 -21.0 -19.0 2701.0 5006.0;
select box = -21.0 -21.0 -21.0 21.0 2701.0 5026.0;
select box = -21.0 -21.0 4964.0 7321.0 2701.0 21.0;
select box = -21.0 -21.0 -21.0 7321.0 2701.0 21.0;

};

# Description des capteurs
save_traces = true;
traces_format=hdf5;

# Fichier protection reprise
prorep=false;
prorep_iter=1000;
restart_iter=298000;

# sources
source {
    coords = 300.00 300.00 300.00;
    type = impulse;
    dir = 0.00 0.00 1.00;
    func = file;
    time_file = "usds_th.csv";
};

source {
    coords = 300.00 300.00 300.00;
    type = impulse;
    dir = 0.00 1.00 0.00;
    func = file;
    time_file = "ud_th.csv";
};

source {
    coords = 300.00 300.00 300.00;
    type = impulse;
    dir = 1.00 0.00 0.00;
    func = file;
    time_file = "cross_str.csv";
};

time_scheme {
    accel_scheme = false;  # Acceleration scheme for Newmark
    veloc_scheme = true;   # Velocity scheme for Newmark
    alpha = 0.5;           # alpha (Newmark parameter)
    beta = 0.5;            # beta (Newmark parameter)
    gamma = 1;             # gamma (Newmark parameter)
    courant = 0.5;
};

ngll=5;

capteurs "UU" {
    type = points;
    file = "stations.txt";
    period = 100;
};

out_variables {
    enP = 0;   # P-wave energy (scalar field)
    enS = 0;    # S-wave energy (scalar field)
    evol = 0;   # volumetric strain (scalar field)
    pre  = 1;   # pressure (scalar field)
    dis   = 1;   # displacement (vector field)
    vel   = 1;   #  velocity (vector field)
    acc  = 1;   # acceleration (vector field)
    edev = 0;  # deviatoric strain (tensor field)
    sdev  = 0;  # deviatoric stress (tensor field)
};
