# ***************************************************************************
# *   Copyright (c) 2019 Bernd Hahnebach <bernd@bimstatik.org>              *
# *   Copyright (c) 2020 Sudhanshu Dubey <sudhanshu.thethunder@gmail.com>   *
# *                                                                         *
# *   This file is part of the FreeCAD CAx development system.              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

# to run the example use:
"""
from femexamples.ccx_cantilever_nodeload import setup
setup()

"""

# import FreeCAD

import ObjectsFem

from .ccx_cantilever_faceload import setup_cantileverbase

mesh_name = "Mesh"  # needs to be Mesh to work with unit tests


def get_information():
    return {
        "name": "CCX cantilever node load",
        "meshtype": "solid",
        "meshelement": "Tet10",
        "constraints": ["fixed", "force"],
        "solvers": ["calculix", "z88", "elmer"],
        "material": "solid",
        "equation": "mechanical"
    }


def setup(doc=None, solvertype="ccxtools"):
    # setup CalculiX cantilever, apply 9 MN on the 4 nodes of the front end face

    doc = setup_cantileverbase(doc, solvertype)
    analysis = doc.Analysis
    geom_obj = doc.Box

    # constraint force
    con_force = ObjectsFem.makeConstraintForce(doc, "ConstraintForce")
    con_force.References = [
        (geom_obj, "Vertex5"),
        (geom_obj, "Vertex6"),
        (geom_obj, "Vertex7"),
        (geom_obj, "Vertex8")
    ]
    con_force.Force = 9000000.0
    con_force.Direction = (doc.Box, ["Edge5"])
    con_force.Reversed = True
    analysis.addObject(con_force)

    doc.recompute()
    return doc
