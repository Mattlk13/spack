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
from spack import *


class RMarkdown(Package):
    """Provides R bindings to the 'Sundown' 'Markdown' rendering library
    (https://github.com/vmg/sundown). 'Markdown' is a plain-text formatting
    syntax that can be converted to 'XHTML' or other formats. See
    http://en.wikipedia.org/wiki/Markdown for more information about
    'Markdown'."""

    homepage = "https://github.com/rstudio/markdown"
    url      = "https://cran.r-project.org/src/contrib/markdown_0.7.7.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/markdown"

    version('0.7.7', '72deca9c675c7cc9343048edbc29f7ff')

    extends('R')

    depends_on('r-mime', type=nolink)

    def install(self, spec, prefix):
        R('CMD', 'INSTALL', '--library={0}'.format(self.module.r_lib_dir),
          self.stage.source_path)