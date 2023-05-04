#!/bin/bash -l
#SBATCH --time=6:00:00
#SBATCH --mem=80g
#SBATCH --tmp=10g
#SBATCH --ntasks-per-node=128
#SBATCH --nodes=2
#SBATCH -p shen
#
cd ${SLURM_SUBMIT_DIR}

# EXEC_PATH must be a path that is accessble from the container
IMAGE_PATH="hpcsdk_ompi.sif"
EXEC_PATH="/scratch.global/xuanx004/mpi_image/osu-micro-benchmarks-7.1-1/c/mpi/pt2pt/standard/"

module load ompi/4.1.5/gnu-11.3.0
module load singularity

# export OMP_NUM_THREADS=16
# export OMP_PROC_BIND=close
# export OMP_PLACES=cores

mpirun -n 2 --map-by node:PE=1 --bind-to core --report-bindings apptainer run --bind /scratch.global:/scratch.global $IMAGE_PATH ${EXEC_PATH}/osu_latency
mpirun -n 2 --map-by node:PE=1 --bind-to core --report-bindings apptainer run --bind /scratch.global:/scratch.global $IMAGE_PATH ${EXEC_PATH}/osu_bw

