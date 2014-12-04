from spack import *

class Legion(Package):
    """Description"""
    homepage = "http://legion.stanford.edu"
    url      = "http://www.example.com/legion-1.0.tar.gz"

    version('2014-11-13', git='https://github.com/StanfordLegion/legion.git',
            commit='bf1ff0b71d9a3a74bcfbc5d9bb6d64bfc7ddb6a7')

    depends_on('gasnet')

    def install(self, spec, prefix):
        with working_dir('runtime'):
            make('CONDUIT=udp',
                 'GASNET=%s' % spec['gasnet'].prefix,
                 'USE_CUDA=0',
                 'USE_MPI=0')

#            make("install")
