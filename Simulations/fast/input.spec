# -*- mode: perl -*-
run_name = "fast";

# duration of the run
sim_time = 20.0000;
mesh_file = "mesh4spec"; # input mesh file
mat_file = "material.input";
dim=3;
mpml_atn_param = 0.002;

snapshots {
    save_snap = true;
    snap_interval = 0.05;
    
    deselect all;
select box = -101.0 -101.0 -101.0 28001.0 14156.5 25711.0;
select box = 27799.0 -101.0 -101.0 -99.0 14156.5 25711.0;
select box = -101.0 -101.0 -101.0 101.0 14156.5 25811.0;
select box = -101.0 -101.0 25509.0 28001.0 14156.5 101.0;
select box = -101.0 -101.0 -101.0 28001.0 14156.5 101.0;

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
    coords = 8000.00 8000.00 8000.00;
    type = impulse;
    dir = 0.00 0.00 1.00;
    func = file;
    time_file = "usds_th.csv";
};

source {
    coords = 8000.00 8000.00 8000.00;
    type = impulse;
    dir = 0.00 1.00 0.00;
    func = file;
    time_file = "ud_th.csv";
};

source {
    coords = 8000.00 8000.00 8000.00;
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
