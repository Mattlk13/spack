from spack import *

class HpctoolkitExternals(Package):
    """HPCToolkit has many prerequisites.  Some, like libelf and
    libxml2 are commonly found on Linux systems, but not always.
    Others, like Open Analysis and SymtabAPI are almost never
    available.  And then there's binutils.  HPCToolkit uses a
    heavily-patched and incompatible version of binutils, so the only
    place you'll find it is in a Rice subversion repository.

    The externals tree is an attempt to deal with these prerequisites.
    It scans your system to identify which packages are available and
    attempts to build the ones that are missing.  It is still a work
    in progress."""

    homepage = "http://hpctoolkit.org"

    version('2015.08.27', git='https://github.com/HPCToolkit/hpctoolkit-externals.git',
            commit='dc16ac0e4ef8bf7787d26e5d0d5c0690ed0a27be')

    depends_on('cmake@2.8:')

    def install(self, spec, prefix):
        with working_dir('BUILD', create=True):
            configure = Executable('../configure')
            configure('CC=cc',
                      'CXX=c++',
                      '--prefix=%s' % prefix)
            make('install', parallel=False)
