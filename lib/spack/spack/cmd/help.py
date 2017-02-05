##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import sys
from llnl.util.tty.color import colorize

description = "get help on spack and its commands"


def setup_parser(subparser):
    help_cmd_group = subparser.add_mutually_exclusive_group()
    help_cmd_group.add_argument('help_command', nargs='?', default=None,
                                help='command to get help on')

    help_all_group = subparser.add_mutually_exclusive_group()
    help_all_group.add_argument('-a', '--all', action='store_true',
                                help='print all available commands')

    help_spec_group = subparser.add_mutually_exclusive_group()
    help_spec_group.add_argument('-s', '--spec', action='store_true',
                                 help='print help on the spec syntax.')


def help(parser, args):
    if args.help_command:
        parser.parse_args([args.help_command, '-h'])

    elif args.all:
        print parser.format_help_long()

    elif args.spec:
        print colorize(
            """\
spec expressions:
    <package>                                    package name
      @c{@<version>}                                 version
      @g{%<compiler>@<version>}                      compiler
      @B{+<name>}|@r{-<name>}|@r{~<name>}                    variants
      @m{platform=<name>} @m{os=<name>} @m{target=<name>}    architecture
      /<hash>                                    ref by hash
      ^<package> [...]                           dependency constraints
""", color=sys.stdout.isatty())
        # TODO: add some examples here.

    else:
        parser.print_help()
