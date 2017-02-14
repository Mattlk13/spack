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
import platform
from spack.architecture import Platform, Target
from spack.operating_systems.linux_distro import LinuxDistro
from llnl.util.cpu_name import get_cpu_name

class Linux(Platform):
    priority    = 90

    def __init__(self):
        super(Linux, self).__init__('linux')

        # Add "basic" architectures
        self.add_target('x86_64', Target('x86_64'))
        self.add_target('ppc64le', Target('ppc64le'))
        self.add_target('ppc64', Target('ppc64'))

        # Add Intel architectures
        self.add_target('haswell', Target('haswell'))
        self.add_target('broadwell', Target('broadwell'))
        self.add_target('ivybridge', Target('ivybridge'))
        self.add_target('sandybridge', Target('sandybridge'))
        self.add_target('knl', Target('knl'))

        # Add IBM architectures
        self.add_target('power7', Target('power7'))
        self.add_target('power8', Target('power8'))
        self.add_target('power8le', Target('power8le'))
        self.add_target('power9', Target('power9'))
        self.add_target('power9le', Target('power9le'))
        # Eternal TODO: Add more architectures as needed.

        # Get specific default
        self.default = get_cpu_name()
        self.front_end = self.default
        self.back_end = self.default

        if not self.default:
            # Fall back on more general name.
            # This will likely fall in "basic" architectures list
            self.default = platform.machine()
            self.front_end = self.default
            self.back_end = self.default

        if self.default not in self.targets:
            self.add_target(self.default, Target(self.default))

        linux_dist = LinuxDistro()
        self.default_os = str(linux_dist)
        self.front_os = self.default_os
        self.back_os = self.default_os
        self.add_operating_system(str(linux_dist), linux_dist)

    @classmethod
    def detect(self):
        return 'linux' in platform.system().lower()
