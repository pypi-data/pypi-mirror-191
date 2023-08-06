# SPDX-FileCopyrightText: Copyright © DUNE Project contributors, see file LICENSE.md in module root
# SPDX-License-Identifier: LicenseRef-GPL-2.0-only-with-DUNE-exception

import projectnameTest as iks
import numpy

import dune.grid


if __name__ == "__main__":
    lowerLeft = []
    upperRight = []
    elements = []
    for i in range(2):
        lowerLeft.append(-1)
        upperRight.append(1)
        elements.append(3)

    grid = dune.grid.structuredGrid(lowerLeft,upperRight,elements)
    nDofs1 = grid.size(2)
    nDofs2 = grid.size(2)
    for i in range(2):
        nDofs2 += grid.size(i)




