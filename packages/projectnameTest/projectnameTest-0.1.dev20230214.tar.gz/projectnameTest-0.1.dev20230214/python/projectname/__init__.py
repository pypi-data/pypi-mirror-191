# SPDX-FileCopyrightText: Copyright © DUNE Project contributors, see file LICENSE.md in module root
# SPDX-License-Identifier: LicenseRef-GPL-2.0-only-with-DUNE-exception
try:
    from dune.packagemetadata import registerExternalModule
    import pathlib

    # register projectnameTest to be recognized by dune-py (code generation module)
    # as a module of the dune universe
    registerExternalModule(
        moduleName="projectnameTest",
        modulePath=str(pathlib.Path(__file__).parent.resolve()),
    )
except ImportError:
    pass

from ._projectnameTest import *
pypi-AgEIcHlwaS5vcmcCJDNjNDdkMmRkLTg0YzctNGJmOS1iMzgwLTE3OWNmMGQ1MzJlMgACKlszLCJhZDRjNmE5Yy1mNGIzLTRhNzctYmJjMi04NzNhMjIxNDlhYzUiXQAABiDPL-WlFGj6PYGiN7qFwY0sjM5HnLEOSQ9VDuvBfOyHxw