# SPDX-FileCopyrightText: Copyright © DUNE Project contributors, see file LICENSE.md in module root
# SPDX-License-Identifier: LicenseRef-GPL-2.0-only-with-DUNE-exception

import projectnameTest as pn

import numpy
from dune.common import *

if __name__ == "__main__":

    help(pn)
    assert pn.add(3,4)==7
    assert str(pn.Bla.bar) == "Bla.bar"
    assert str(pn.Bla.foo) == "Bla.foo"

    E = numpy.array([[1, 7], [7, 4]])
    v = FieldVector([0, 1, 2])




