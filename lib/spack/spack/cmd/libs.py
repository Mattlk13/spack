##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import sys
import os
import re
import subprocess
from external import argparse

import spack
import spack.cmd
from spack import *

description = "Examine libraries and their dependencies."

acceptable = [
    '/lib64/ld-2.12.so',
    '/lib64/libc-2.12.so',
    '/lib64/libdl-2.12.so',
    '/lib64/libgcc_s-4.4.7-20120601.so.1',
    '/lib64/libm-2.12.so',
    '/lib64/libpthread-2.12.so',
    '/lib64/libutil-2.12.so',
    '/usr/lib64/libstdc++.so.6.0.13',
    '/lib64/librt-2.12.so',
    '/usr/lib64/libgfortran.so.3.0.0']


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='libs_command')

    list_parser = sp.add_parser('list', help=libs_list.__doc__)
    list_parser.add_argument('dirs', nargs=argparse.REMAINDER,
                             help="directories or files for which to list dependencies.")

    list_parser = sp.add_parser('deps', help=libs_deps.__doc__)
    list_parser.add_argument('dirs', nargs=argparse.REMAINDER,
                             help="directories or files to find dependencies in.")

    check_parser = sp.add_parser('check', help=libs_check.__doc__)
    check_parser.add_argument('dirs', nargs=argparse.REMAINDER,
                             help="directories or files to check for dependencies.")


def find_objects(directory):
    file_cmd = which('file', required=True)
    objs = set()

    # Add file to objs if it is, in fact, an object file.
    def handle_file(path):
        if os.path.islink(path):
            return

        if path.endswith('.so'):
            objs.add(path)

        elif os.path.isfile(path):
            if "ELF" in file_cmd(path, return_output=True):
                objs.add(path)

    # Raise an error if the file doesn't exist.
    if not os.path.exists(directory):
        raise spack.error.SpackError("No such file or directory: %s" % directory)

    # handle the path whether it's a file or a directory.
    if os.path.isdir(directory):
        for root, dirs, files in os.walk(directory):
            for f in files:
                handle_file(join_path(root, f))
    else:
        handle_file(directory)

    return objs


def find_deps(objs):
    ldd = which('ldd', required=True)

    deps = set()
    for o in objs:
        libs = ldd(o, return_output=True)
        for line in libs.split('\n'):
            if line.startswith('\t'):
                match = re.search(r'^\t(?:(.*) => )?(not found|[^\ ]*).*$', line)
                lib = match.group(2)
                if lib == "not found":
                    deps.add('NOT-FOUND %s' % match.group(1))
                else:
                    deps.add(os.path.realpath(lib))
    return deps


def libs_list(args):
    """List libraries and object files in the specified directories."""
    objs = [find_objects(d) for d in args.dirs]
    for o in sorted(set.union(*objs)):
        print o


def libs_deps(args):
    """List dpeendencies of libs and objects in the specified directories."""
    deps = [find_deps(find_objects(d)) for d in args.dirs]
    for lib in sorted(set.union(*deps)):
        print lib


def libs_check(args):
    """Check for libraries that are outside spack."""
    deps = [find_deps(find_objects(d)) for d in args.dirs]

    e = 0
    for lib in sorted(set.union(*deps)):
        if not lib.startswith(spack.install_layout.root) and not lib in acceptable:
            print lib
            e = 1
    sys.exit(e)


def libs(parser, args):
    if not args.dirs:
        tty.die("libs requires at least one directory as an argument")

    action = { 'list'  : libs_list,
               'deps'  : libs_deps,
               'check' : libs_check }

    action[args.libs_command](args)
