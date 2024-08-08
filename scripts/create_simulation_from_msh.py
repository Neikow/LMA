import os
from typing import List, Tuple

from seismic_data import create_seismic_data

# copernicus account
account = "b401"
# user email
email = "lysen@lma.cnrs-mrs.fr"
# mt_import_gmsh path
mt_import_gmsh_path = (
    "C:\\Users\\Vitaly\\OneDrive\\Bureau\\LMA\\scripts\\pysem\\mt_import_gmsh"
)
# h5 file name
h5_file = "output.h5"

# remote server
remote_server = "copernicus"
# remote server path
remote_server_path = "/scratch/vlysen/sims"


def format_timeout_str(timeout: int) -> str:
    """
    Format the timeout in minutes to a string
    :param timeout: timeout in minutes
    :return: formatted timeout string
    """
    return f'{timeout // 60}:{str(timeout % 60).ljust(2, "0")}:00'


def get_mesh_input(procs_count: int, msh_file: str) -> str:
    """
    Get the contents of the mesh.input file
    :param procs_count: number of processors for the job
    :param msh_file: name of the mesh file
    :return: contents of the mesh.input file
    """
    return f"""{procs_count}
4
1
{msh_file}
"""


def get_stations_txt(path: str):
    """
    Get the contents of the stations.txt file
    :param pts: a list of points
    :return: contents of the stations.txt file
    """
    with open(path, 'r') as f:
        return f.read()


def get_sources_from_ricker(source: Tuple[float, float, float]):
    return f"""source {{
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
}};"""


def get_sources_from_seismic_data(
    files: List[str],
    sources: List[Tuple[float, float, float]],
    direction: List[Tuple[float, float, float]],
):
    def get_source(
        file: str,
        source_point: Tuple[float, float, float],
        _direction: Tuple[float, float, float],
    ):
        return f"""source {{
    coords = {' '.join([f'{x:.2f}' for x in source_point])};
    type = impulse;
    dir = {' '.join([f'{x:.2f}' for x in _direction])};
    func = file;
    time_file = "{file}";
}};"""

    return "\n\n".join(
        [
            get_source(file, source, _dir)
            for file, source, _dir in zip(files, sources, direction)
        ]
    )


def get_selection(src_dir: str):
    selection_path = os.path.join(src_dir, 'selection.txt')
    if os.path.exists(selection_path):
        with open(selection_path, 'r') as f:
            selection = f.read()
            return selection
    else:
        return ''


def get_input_spec(
    job_name: str,
    sim_time: float,
    mat_file: str,
    source: Tuple[float, float, float],
    src_dir: str,
    use_ricker: bool = False,
) -> str:
    return f"""# -*- mode: perl -*-
run_name = "{job_name}";

# duration of the run
sim_time = {sim_time:.4f};
mesh_file = "mesh4spec"; # input mesh file
mat_file = "{mat_file}";
dim=3;
mpml_atn_param = 0.002;

snapshots {{
    save_snap = true;
    snap_interval = 0.05;
    
    {get_selection(src_dir)}
}};

# Description des capteurs
save_traces = true;
traces_format=hdf5;

# Fichier protection reprise
prorep=false;
prorep_iter=1000;
restart_iter=298000;

# sources
{get_sources_from_ricker(source) if use_ricker else get_sources_from_seismic_data(
    ["usds_th.csv", "ud_th.csv", "cross_str.csv"],
    [(300, 300, 300), (300, 300, 300), (300, 300, 300)],
    [(0, 0, 1), (0, 1, 0), (1, 0, 0)],
)}

time_scheme {{
    accel_scheme = false;  # Acceleration scheme for Newmark
    veloc_scheme = true;   # Velocity scheme for Newmark
    alpha = 0.5;           # alpha (Newmark parameter)
    beta = 0.5;            # beta (Newmark parameter)
    gamma = 1;             # gamma (Newmark parameter)
    courant = 0.5;
}};

ngll=5;

capteurs "UU" {{
    type = points;
    file = "stations.txt";
    period = 100;
}};

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
}};
"""


def get_prepro_sh(job_name: str, timeout: int):
    """
    Get the contents of the prepro.sh file
    :param job_name: name of the current job
    :param timeout: timeout in minutes
    :return: contents of the prepro.sh file
    """
    return f"""#!/bin/sh
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
"""


def get_run_sh(job_name: str, procs_count: int, timeout: int):
    return f"""#!/bin/sh
#SBATCH -J {job_name}_SEMRun
#SBATCH -p skylake
#SBATCH -n {procs_count}
#SBATCH -N 1
#SBATCH -A {account}
#SBATCH -t {format_timeout_str(timeout)}
#SBATCH -o ./%N.%x.out
#SBATCH -e ./%N.%x.err
#SBATCH --mail-type=BEGIN,END
#SBATCH --mail-user={email}
{'#SBATCH --exclusive' if procs_count >= 32 else ''}

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
srun -n $SLURM_NTASKS /home/${{SLURM_JOB_USER}}/SEM/buildSEM/SEM3D/sem3d.exe > output.log"""


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Create all the files required for a simulation from a msh file."
    )

    parser.add_argument(
        "simulation_name", type=str, help="Name of the simulation project"
    )
    parser.add_argument(
        "source_msh_path", type=str, help="The msh file used for the simulation"
    )
    parser.add_argument(
        "-n",
        dest="proc_count",
        type=int,
        help="Number of processors for the job (default=32)",
        default=32,
    )
    parser.add_argument(
        "-T",
        dest="sim_time",
        type=int,
        help="Simulation duration (in s) (default=5)",
        default=5,
    )
    parser.add_argument(
        "-t",
        dest="sim_timeout",
        type=int,
        help="Timeout of the simulation (in min) (default=48h)",
        default=48 * 60,
    )
    parser.add_argument(
        "-m",
        dest="material_file_name",
        help="The material file for the simulation in the same directory as the .msh file",
        default="material.input",
    )
    parser.add_argument(
        "-o",
        dest="output_dir",
        help="Output directory for the simulation files",
        default="Simulations",
    )

    parser.add_argument(
        "-c",
        dest="remote_copy",
        action="store_true",
        help="Copy the simulation files to the remote server using `scp`",
    )

    parser.add_argument(
        "-r",
        dest="use_ricker",
        action="store_true",
        help="Use Ricker source instead of the provided seismic data",
    )

    args = parser.parse_args()

    sim_dir = os.path.join(args.output_dir, args.simulation_name)

    material_file_path = os.path.join(
        os.path.dirname(args.source_msh_path), args.material_file_name
    )

    stations_file_path = os.path.join(
        os.path.dirname(args.source_msh_path), 'stations.txt'
    )

    try:
        os.mkdir(sim_dir)
    except FileExistsError:
        pass

    os.system(
        f"python {mt_import_gmsh_path} {args.source_msh_path} {os.path.join(sim_dir, h5_file)}"
    )

    with open(os.path.join(sim_dir, "mesh.input"), "w", newline="\n") as f:
        f.write(get_mesh_input(args.proc_count, h5_file))

    with open(os.path.join(sim_dir, "stations.txt"), "w", newline="\n") as f:
        f.write(get_stations_txt(stations_file_path))

    with open(os.path.join(sim_dir, "input.spec"), "w", newline="\n") as f:
        f.write(
            get_input_spec(
                args.simulation_name,
                args.sim_time,
                args.material_file_name,
                (300, 300, 300),
                os.path.dirname(args.source_msh_path),
                args.use_ricker,
            )
        )

    with open(os.path.join(sim_dir, "prepro.sh"), "w", newline="\n") as f:
        f.write(get_prepro_sh(args.simulation_name, args.sim_timeout))

    with open(os.path.join(sim_dir, "run.sh"), "w", newline="\n") as f:
        f.write(get_run_sh(args.simulation_name, args.proc_count, args.sim_timeout))

    if not args.use_ricker:
        create_seismic_data(sim_dir, args.sim_time, args.sim_time * 200)

    with open(material_file_path, "r", newline="\n") as f:
        with open(
            os.path.join(sim_dir, args.material_file_name), "w", newline="\n"
        ) as f2:
            f2.write(f.read())

    if args.remote_copy:
        os.system(
            f"scp -r {sim_dir}/. {remote_server}:{remote_server_path}/{args.simulation_name}"
        )


if __name__ == "__main__":
    main()
