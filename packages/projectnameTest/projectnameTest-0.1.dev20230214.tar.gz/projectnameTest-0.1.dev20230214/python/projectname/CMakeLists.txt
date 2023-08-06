# SPDX-FileCopyrightText: Copyright © DUNE Project contributors, see file LICENSE.md in module root
# SPDX-License-Identifier: LicenseRef-GPL-2.0-only-with-DUNE-exception

add_python_targets(projectnameTest
  __init__
)

dune_add_pybind11_module(NAME _projectnameTest)
set_property(TARGET _projectnameTest PROPERTY LINK_LIBRARIES dunecommon APPEND)
target_compile_features(_projectnameTest PRIVATE cxx_std_20)
if(SKBUILD)
  install(TARGETS _projectnameTest LIBRARY DESTINATION python/projectnameTest)
endif()
