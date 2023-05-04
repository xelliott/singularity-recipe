#!/bin/bash
## Required PBS Directives --------------------------------------
#PBS -q standard
#PBS -l select=2:ncpus=128:mpiprocs=128
#PBS -l walltime=0:15:00

## Optional PBS Directives --------------------------------------
#PBS -N test_singularity
#PBS -j oe
#PBS -S /bin/bash

# EXEC_PATH must be a path that is accessble from the container
IMAGE_PATH="${HOME}/local/hpcsdk-mpich-ubuntu20.04.sif"
EXEC_PATH="$WORKDIR/test/osu-micro-benchmarks-7.1-1/c/mpi/pt2pt/standard/"

## Execution Block ----------------------------------------------
# Environment Setup
module load singularity
module swap PrgEnv-cray PrgEnv-gnu
module swap cray-mpich cray-mpich-abi

# The dynamic libraries needed to be linked into the container are mainly
# referenced from:
# https://klust.github.io/LUMI-EasyBuild-docs/s/singularity-bindings/
local_craympich_version='8.1.19'
local_libfabric_version='1.11.0.4.125'

export SINGULARITYENV_LD_LIBRARY_PATH="/lib64:/opt/cray/pe/mpich/${local_craympich_version}/ofi/gnu/9.1/lib-abi-mpich:/opt/cray/pe/lib64:/opt/cray/pe:/opt/cray/libfabric/${local_libfabric_version}/lib64:/usr/lib64:/opt/cray/pe/gcc-libs"
echo $SINGULARITYENV_LD_LIBRARY_PATH

export SINGULARITY_BIND='/opt/cray'\
",/usr/lib64/libibverbs.so.1"\
",/usr/lib64/librdmacm.so.1"\
",/usr/lib64/libnl-3.so.200"\
",/usr/lib64/libnl-route-3.so.200"\
",/usr/lib64/libcurl.so.4"\
",/usr/lib64/libnghttp2.so.14"\
",/usr/lib64/libidn2.so.0"\
",/usr/lib64/libssh.so.4"\
",/usr/lib64/libpsl.so.5"\
",/usr/lib64/libssl.so.1.1"\
",/usr/lib64/libcrypto.so.1.1"\
",/usr/lib64/libgssapi_krb5.so.2"\
",/usr/lib64/libldap_r-2.4.so.2"\
",/usr/lib64/liblber-2.4.so.2"\
",/usr/lib64/libjson-c.so.3"\
",/usr/lib64/libunistring.so.2"\
",/usr/lib64/libkrb5.so.3"\
",/usr/lib64/libk5crypto.so.3"\
",/usr/lib64/libkrb5support.so.0"\
",/usr/lib64/libsasl2.so.3"\
",/usr/lib64/libkeyutils.so.1"\
",/usr/lib64/libibverbs/libmlx5-rdmav25.so"\
",/etc/libibverbs.d"\
",/var/run/palsd"\
",/var/opt/cray"

## Launching ----------------------------------------------------
mpiexec -n 2 -ppn 1 singularity exec --bind /p/work1 --bind /p/home --home ${HOME}:/home/$USER ${IMAGE_PATH} ${EXEC_PATH}/osu_latency
mpiexec -n 2 -ppn 1 singularity exec --bind /p/work1 --bind /p/home --home ${HOME}:/home/$USER ${IMAGE_PATH} ${EXEC_PATH}/osu_bw

