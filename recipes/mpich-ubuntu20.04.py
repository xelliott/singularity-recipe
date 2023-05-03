"""
HPC Base image

Contents:
  FFTW
  GNU compilers 11
  HDF5
  MPICH
  Python 2 and 3 (upstream)
"""
# pylint: disable=invalid-name, undefined-variable, used-before-assignment

# Choose between either Ubuntu 16.04 (default) or CentOS 7
# Add '--userarg centos=true' to the command line to select CentOS
devel_image = "nvidia/cuda:11.5.1-base-ubuntu20.04"
# runtime_image = 'nvcr.io/nvidia/cuda:10.1-runtime-ubuntu16.04'

######
# Devel stage
######

Stage0 += comment(__doc__, reformat=False)

Stage0 += baseimage(image=devel_image, _as="devel")

# Python
Stage0 += python()

# GNU compilers
compiler = gnu(version="11", extra_repository=True)
Stage0 += compiler
Stage0 += cmake(eula=True, version="3.20.6")

# MPICH
mpi = mpich(
    ldconfig=True,
    version="3.4.3",
    toolchain=compiler.toolchain,
    configure_opts=[
        "--with-device=ch4:ofi",
        f"FFLAGS='{compiler.toolchain.FFLAGS} -fallow-argument-mismatch'",
        f"FCFLAGS='{compiler.toolchain.FCFLAGS} -fallow-argument-mismatch'",
    ],  # mpich needs -fallow-argument-mismatch set for gfortran > 10
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
