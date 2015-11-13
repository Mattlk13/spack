from spack import *

class Hpctoolkit(Package):
    """hpctoolkit"""

    homepage = "http://www.example.com"

    version('2015.08.27', git='https://github.com/HPCToolkit/hpctoolkit.git',
            commit='c11eaf4a3e259664b96839c6c9b3d3a3b9466607')

    depends_on('mpi')
    depends_on('hpctoolkit-externals')
    depends_on('papi@4:')

    def install(self, spec, prefix):
        with working_dir('BUILD', create=True):
            configure = Executable('../configure')
            configure('CC=cc',
                      'CXX=c++',
                      'MPICXX=mpicxx',
                      '--prefix=%s' % prefix,
                      '--with-externals=%s' % spec['hpctoolkit-externals'].prefix,
                      '--with-papi=%s' % spec['papi'].prefix)
            make("install")


