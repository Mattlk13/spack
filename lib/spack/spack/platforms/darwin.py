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
from llnl.util.cpu_name import get_cpu_name
from spack.architecture import Platform, Target
from spack.operating_systems.mac_os import MacOs


class Darwin(Platform):
    priority    = 89

    def __init__(self):
        super(Darwin, self).__init__('darwin')

        # TODO: These are probably overkill
        # Add Intel architectures
        self.add_target('haswell', Target('haswell'))
        self.add_target('broadwell', Target('broadwell'))
        self.add_target('ivybridge', Target('ivybridge'))
        self.add_target('sandybridge', Target('sandybridge'))

        # Add "basic" architectures
        self.add_target('x86_64', Target('x86_64'))
        self.add_target('ppc64le', Target('ppc64le'))
        self.add_target('ppc64', Target('ppc64'))

        # Add IBM architectures
        self.add_target('power7', Target('power7'))
        self.add_target('power8', Target('power8'))
        self.add_target('power8le', Target('power8le'))
        self.add_target('power9', Target('power9'))
        self.add_target('power9le', Target('power9le'))

        self.default = get_cpu_name()
        self.front_end = self.default
        self.back_end = self.default

        if self.default not in self.targets:
            self.add_target(self.default, Target(self.default))

        mac_os = MacOs()

        self.default_os = str(mac_os)
        self.front_os   = str(mac_os)
        self.back_os    = str(mac_os)

        self.add_operating_system(str(mac_os), mac_os)

    @classmethod
    def detect(self):
        return 'darwin' in platform.system().lower()
