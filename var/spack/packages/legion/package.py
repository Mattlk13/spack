from spack import *

class Legion(Package):
    """Description"""
    homepage = "http://legion.stanford.edu"
    url      = "http://www.example.com/legion-1.0.tar.gz"

    version('2014-12-08', git='https://github.com/chuckatkins/legion.git',
            commit='d1d89ea905e2bee7f148fb38ed0d2581fb10c023')

    depends_on('gasnet')

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake("..",
                  "-DLegion_USE_GASNet=ON",
                  "-DCMAKE_EXE_LINKER_FLAGS=-lrt",
                  *std_cmake_args)
            make()
            make("install")
