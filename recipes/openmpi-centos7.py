"""
HPC Base image

Contents:
  FFTW
  GNU compilers 11
  HDF5
  Mellanox OFED version 5.8-1.1.2.1
  OpenMPI version 4.0.2
  Python 2 and 3 (upstream)
"""
# pylint: disable=invalid-name, undefined-variable, used-before-assignment

# Choose between either Ubuntu 16.04 (default) or CentOS 7
# Add '--userarg centos=true' to the command line to select CentOS
devel_image = "nvidia/cuda:11.5.1-base-centos7"
# runtime_image = 'nvcr.io/nvidia/cuda:10.1-runtime-ubuntu16.04'

######
# Devel stage
######

Stage0 += comment(__doc__, reformat=False)

Stage0 += baseimage(image=devel_image, _as="devel")

# Python
Stage0 += python()

# GNU compilers
compiler = gnu(version="11")
Stage0 += compiler
Stage0 += cmake(eula=True, version="3.20.6")

# Mellanox OFED
Stage0 += mlnx_ofed(version="5.8-1.1.2.1")

Stage0 += knem(ldconfig=True, version="1.1.4")

Stage0 += ucx(
    knem="/usr/local/knem",
    ldconfig=True,
    version=USERARG.get("ucx", "1.14.0"),
    cuda=False,
    toolchain=compiler.toolchain,
)

# OpenMPI
mpi = openmpi(
    ldconfig=True, toolchain=compiler.toolchain, cuda=False, ucx="/usr/local/ucx"
)
Stage0 += mpi

# FFTW
for fftw_type in ["double", "float"]:
    Stage0 += fftw(
        prefix=f"/usr/local/fftw-{fftw_type}",
        version="3.3.8",
        mpi=False,
        toolchain=compiler.toolchain,
        enable_avx=True,
        enable_avx2=True,
        enable_float=(fftw_type == "float"),
    )
    Stage0 += environment(
        variables={
            "CPATH": "/usr/local/fftw-{0}/include:$CPATH".format(fftw_type),
            "LIBRARY_PATH": "/usr/local/fftw-{0}/lib:$LIBRARY_PATH".format(fftw_type),
        }
    )

# HDF5
Stage0 += hdf5(
    configure_opts=["--enable-parallel", "--enable-fortran"], toolchain=mpi.toolchain
)

#######
## Runtime image
#######

# Stage1 += baseimage(image=runtime_image)

# Stage1 += Stage0.runtime(_from='devel')
