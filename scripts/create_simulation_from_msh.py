from typing import List, Tuple

# copernicus account
account = 'b401'
# user email
email = 'vitaly.lysen@gmail.com'


def format_timeout_str(timeout: int) -> str:
    """
    Format the timeout in minutes to a string
    :param timeout: timeout in minutes
    :return: formatted timeout string
    """
    return f'{timeout // 60}:{str(timeout % 60).ljust(2, "0")}:00'


def get_mesh_input(procs_count: int, msh_file: int) -> str:
    """
    Get the contents of the mesh.input file
    :param procs_count: number of processors for the job
    :param msh_file: name of the mesh file
    :return: contents of the mesh.input file
    """
    return f'''{procs_count}
4
1
{msh_file}
'''


def get_stations_txt(pts: List[Tuple[float, float, float]]):
    """
    Get the contents of the stations.txt file
    :param pts: a list of points
    :return: contents of the stations.txt file
    """
    return '\n'.join([f'{x:.2f} {y:.2f} {z:.2f}' for x, y, z in pts])


def get_input_spec(job_name: str, sim_time: float, mat_file: str, source: Tuple[float, float, float]) -> str:
    return f'''# -*- mode: perl -*-
run_name = {job_name};

# duration of the run
sim_time = {sim_time:.4f};
mesh_file = "mesh4spec"; # input mesh file
mat_file = "{mat_file}";
dim=3;
mpml_atn_param = 0.002;

snapshots {{
    save_snap = true;
}};

# Description des capteurs
save_traces = true;
traces_format=hdf5;

# Fichier protection reprise
prorep=false;
prorep_iter=1000;
restart_iter=298000;

# introduce a source
source {{
    # coordinates of the sources ((x,y,z) or (lat,long,R) if rotundity is considered)
    coords = {' '.join([f'{x:.2f}' for x in source])};
    # the numbers before the labels are here to help convert from previous input.spec format
    # Type (1.Impulse, 2.moment Tensor, 3.fluidpulse)
    type = impulse;
    # Direction 0.x,1.y ou 2.z (only for Impulse)
    dir = 0. 0. 1.;
    # Function 1.gaussian,2.ricker,3.tf_heaviside,4.gabor,5.file,6.spice_bench,7.sinus
    func = ricker;
    tau = 0.4;
    freq = 3.;   # source main frequency / cutoff frequency
}}

time_scheme {{
    accel_scheme = false;  # Acceleration scheme for Newmark
    veloc_scheme = true;   # Velocity scheme for Newmark
    alpha = 0.5;           # alpha (Newmark parameter)
    beta = 0.5;           # beta (Newmark parameter)
    gamma = 1;             # gamma (Newmark parameter)
    courant = 0.2;
}};

ngll=5;

capteurs "UU" {{
    type = points;
    file = "stations.txt";
    period = 40;
}}

out_variables {{
    enP = 0;   # P-wave energy (scalar field)
    enS = 0;    # S-wave energy (scalar field)
    evol = 0;   # volumetric strain (scalar field)
    pre  = 1;   # pressure (scalar field)
    dis   = 1;   # displacement (vector field)
    vel   = 1;   #  velocity (vector field)
    acc  = 1;   # acceleration (vector field)
    edev = 0;  # deviatoric strain (tensor field)
    sdev  = 0;  # deviatoric stress (tensor field)
}}
'''


def get_prepro_sh(job_name: str, timeout: int):
    """
    Get the contents of the prepro.sh file
    :param job_name: name of the current job
    :param timeout: timeout in minutes
    :return: contents of the prepro.sh file
    """
    return f'''#!/bin/sh
#SBATCH -J {job_name}_SEMMesh
#SBATCH -p skylake # partition utilisee
#SBATCH -n 1 # nombre de proc
#SBATCH -A {account} # compte de decompte
#SBATCH -t {format_timeout_str(timeout)} # temps de timeout
#SBATCH -o ./%N.%x.out
#SBATCH -e ./%N.%x.err
# #SBATCH --mail-type=BEGIN,END
# #SBATCH --mail-user={email}
#SBATCH --mem=85G # max 191G

# chargement des modules
module purge
module load userspace/all
module load cmake/3.20.2
module load intel-compiler/64/2018.0.128
module load intel-mpi/64/2018.0.128
module load intel-mkl/64/2018.0.128
module load hdf5/icc18/impi/1.10.1

### export I_MPI_LINK=opt_mt
export CC=icc CXX=icpc FC=ifort
export I_MPI_CC=icc I_MPI_CXX=icpc I_MPI_FC=ifort I_MPI_F90=ifort
export EXTRAMPI=/trinity/shared/apps/tr17.10/x86_64/intel-2018.0.128/compilers_and_libraries_2018.0.128/linux/mpi/intel64
export HDF5_PATH=/trinity/shared/apps/tr17.10/x86_64/hdf5-icc18-impi-1.10.1
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/trinity/shared/apps/tr17.10/x86_64/hdf5-icc18-impi-1.10.1/lib
export LIBRARY_PATH=$LIBRARY_PATH:/trinity/shared/apps/tr17.10/x86_64/hdf5-icc18-impi-1.10.1/lib

# echo of commands
set -x

# To compute in the submission directory
cd ${{SLURM_SUBMIT_DIR}}

rm -r sem
mkdir sem

# run mesh
srun /home/${{SLURM_JOB_USER}}/SEM/buildSEM/MESH/mesher < mesh.input > outputmesh.log

mv mesh4spec* sem/
'''


def get_run_sh(job_name: str, procs_count: int, timeout: int):
    return f'''#!/bin/sh
#SBATCH -J {job_name}_SEMRun
#SBATCH -p skylake
#SBATCH -n {procs_count}
#SBATCH -N 1
#SBATCH -A {account}
#SBATCH -t {format_timeout_str(timeout)}
#SBATCH -o ./%N.%x.out
#SBATCH -e ./%N.%x.err
# #SBATCH --mail-type=BEGIN,END
# #SBATCH --mail-user={email}

# chargement des modules
module purge
module load userspace/all
module load cmake/3.20.2
module load intel-compiler/64/2018.0.128
module load intel-mpi/64/2018.0.128
module load intel-mkl/64/2018.0.128
module load hdf5/icc18/impi/1.10.1

### export I_MPI_LINK=opt_mt
export CC=icc CXX=icpc FC=ifort
export I_MPI_CC=icc I_MPI_CXX=icpc I_MPI_FC=ifort I_MPI_F90=ifort
export EXTRAMPI=/trinity/shared/apps/tr17.10/x86_64/intel-2018.0.128/compilers_and_libraries_2018.0.128/linux/mpi/intel64
export HDF5_PATH=/trinity/shared/apps/tr17.10/x86_64/hdf5-icc18-impi-1.10.1
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/trinity/shared/apps/tr17.10/x86_64/hdf5-icc18-impi-1.10.1/lib
export LIBRARY_PATH=$LIBRARY_PATH:/trinity/shared/apps/tr17.10/x86_64/hdf5-icc18-impi-1.10.1/lib
export I_MPI_PMI_LIBRARY=/usr/lib64/libpmi.so

# echo of commands
set -x

# To compute in the submission directory
cd ${{SLURM_SUBMIT_DIR}}

# execution with 'ntasks' MPI processes
srun -n $SLURM_NTASKS /home/${{SLURM_JOB_USER}}/SEM/buildSEM/SEM3D/sem3d.exe > output.log'''


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Create all the files required for a simulation from a msh file.')

    parser.add_argument('source_msh', type=str, help='The msh file used for the simulation')
    parser.add_argument('simulation_name', type=str, help='Name of the simulation project')
    parser.add_argument('-n', dest='proc_count', type=int, help='Number of processors for the job (default=4)', default=4)
    parser.add_argument('-t', dest='sim_timeout', type=int, help='Timeout of the simulation (in min) (default=60)', default=60)

    args = parser.parse_args()


if __name__ == '__main__':
    main()
